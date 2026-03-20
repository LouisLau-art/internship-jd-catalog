from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener


ANT_BATCH_ID = "26022600074513"
ALI_BATCH_ID = "100000540002"
ALI_CIRCLE_CODE = "60000"
DEFAULT_PAGE_SIZE = 100
ANT_MAX_PAGE_SIZE = 40
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

CSV_COLUMNS = [
    "source",
    "company",
    "position_id",
    "position_name",
    "position_url",
    "batch_id",
    "batch_name",
    "category_name",
    "work_locations",
    "interview_locations",
    "circles",
    "circle_codes",
    "channels",
    "feature_tags",
    "publish_time",
    "modify_time",
    "graduation_from",
    "graduation_to",
    "requirement",
    "description",
]


def build_ant_position_url(position_id: int, tid: str | None) -> str:
    base = f"https://talent.antgroup.com/campus-position?positionId={position_id}"
    return f"{base}&tid={tid}" if tid else base


def build_alibaba_position_url(position_id: int) -> str:
    return f"https://campus-talent.alibaba.com/campus/position/{position_id}"


def clamp_ant_page_size(page_size: int) -> int:
    return min(page_size, ANT_MAX_PAGE_SIZE)


def join_values(values: Any) -> str:
    if not values:
        return ""
    if isinstance(values, (list, tuple)):
        return " | ".join(str(value) for value in values if value not in (None, ""))
    return str(values)


def normalize_ant_job(job: dict[str, Any]) -> dict[str, Any]:
    graduation = job.get("graduationTime") or {}
    return {
        "source": "antgroup",
        "company": "Ant Group",
        "position_id": job.get("id"),
        "position_name": job.get("name", ""),
        "position_url": build_ant_position_url(job.get("id"), job.get("tid")),
        "batch_id": job.get("batchId", ""),
        "batch_name": job.get("batchName", ""),
        "category_name": job.get("categoryName", ""),
        "work_locations": join_values(job.get("workLocations")),
        "interview_locations": join_values(job.get("interviewLocations")),
        "circles": "",
        "circle_codes": "",
        "channels": "",
        "feature_tags": join_values(job.get("featureTagList")),
        "publish_time": job.get("publishTime", ""),
        "modify_time": "",
        "graduation_from": graduation.get("from", ""),
        "graduation_to": graduation.get("to", ""),
        "requirement": job.get("requirement", ""),
        "description": job.get("description", ""),
    }


def normalize_alibaba_job(job: dict[str, Any]) -> dict[str, Any]:
    graduation = job.get("graduationTime") or {}
    return {
        "source": "alibaba",
        "company": "Alibaba",
        "position_id": job.get("id"),
        "position_name": job.get("name", ""),
        "position_url": build_alibaba_position_url(job.get("id")),
        "batch_id": job.get("batchId", ""),
        "batch_name": job.get("batchName", ""),
        "category_name": job.get("categoryName", ""),
        "work_locations": join_values(job.get("workLocations")),
        "interview_locations": join_values(job.get("interviewLocations")),
        "circles": join_values(job.get("circleNames")),
        "circle_codes": join_values(job.get("circleCodeList")),
        "channels": join_values(job.get("channels")),
        "feature_tags": join_values(job.get("featureTagList")),
        "publish_time": job.get("publishTime", ""),
        "modify_time": job.get("modifyTime", ""),
        "graduation_from": graduation.get("from", ""),
        "graduation_to": graduation.get("to", ""),
        "requirement": job.get("requirement", ""),
        "description": job.get("description", ""),
    }


def collect_paginated(
    fetch_page: Callable[[int, int], dict[str, Any]],
    page_size: int,
) -> tuple[list[dict[str, Any]], int]:
    page_index = 1
    total = 0
    items: list[dict[str, Any]] = []

    while True:
        page = fetch_page(page_index, page_size)
        page_items = page["items"] or []
        total = int(page["total"])
        if not page_items:
            break
        items.extend(page_items)
        if len(items) >= total:
            break
        page_index += 1

    return items, total


def create_cookie_opener() -> tuple[Any, CookieJar]:
    jar = CookieJar()
    opener = build_opener(HTTPCookieProcessor(jar))
    return opener, jar


def read_text(request: Request, opener: Any) -> str:
    with opener.open(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset)


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str], opener: Any) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        body = read_text(request, opener)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"request failed for {url}: {exc.code} {detail}") from exc
    return json.loads(body)


def get_cookie_value(cookie_jar: CookieJar, name: str) -> str | None:
    for cookie in cookie_jar:
        if cookie.name == name:
            return cookie.value
    return None


def init_alibaba_session(batch_id: str, circle_code: str) -> tuple[Any, str]:
    opener, cookie_jar = create_cookie_opener()
    query = urlencode({"batchId": batch_id, "circleCode": circle_code})
    page_url = f"https://campus-talent.alibaba.com/campus/position?{query}"
    request = Request(
        page_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Encoding": "identity",
        },
        method="GET",
    )
    html = read_text(request, opener)
    xsrf_token = get_cookie_value(cookie_jar, "XSRF-TOKEN")
    if xsrf_token:
        return opener, xsrf_token

    match = re.search(r'__token__:\s*"([^"]+)"', html)
    if match:
        return opener, match.group(1)

    raise RuntimeError("could not initialize Alibaba session token")


def fetch_alibaba_page(
    page_index: int,
    page_size: int,
    batch_id: str,
    circle_code: str,
    opener: Any,
    xsrf_token: str,
) -> dict[str, Any]:
    payload = {
        "batchId": int(batch_id),
        "pageIndex": page_index,
        "pageSize": page_size,
        "searchKey": "",
    }
    response = post_json(
        "https://campus-talent.alibaba.com/position/search",
        payload,
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "Content-Type": "application/json",
            "Origin": "https://campus-talent.alibaba.com",
            "Referer": f"https://campus-talent.alibaba.com/campus/position?batchId={batch_id}&circleCode={circle_code}",
            "x-xsrf-token": xsrf_token,
        },
        opener,
    )
    content = response["content"]
    return {"items": content["datas"], "total": content["totalCount"]}


def fetch_ant_page(page_index: int, page_size: int, batch_id: str, opener: Any) -> dict[str, Any]:
    payload = {
        "channel": "campus_group_official_site",
        "language": "zh",
        "pageIndex": page_index,
        "pageSize": page_size,
        "key": "",
        "batchIds": [str(batch_id)],
    }
    response = post_json(
        "https://hrcareersweb.antgroup.com/api/campus/position/search",
        payload,
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "Content-Type": "application/json",
            "Origin": "https://talent.antgroup.com",
            "Referer": f"https://talent.antgroup.com/campus-full-list?type=campus_intern&batchId={batch_id}",
        },
        opener,
    )
    return {"items": response["content"], "total": response["totalCount"]}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in CSV_COLUMNS})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Alibaba and Ant Group campus job listings into JSON and CSV.")
    parser.add_argument("--output-dir", default="data", help="Directory for exported files.")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE, help="Page size for list requests.")
    parser.add_argument("--ant-batch-id", default=ANT_BATCH_ID)
    parser.add_argument("--ali-batch-id", default=ALI_BATCH_ID)
    parser.add_argument("--ali-circle-code", default=ALI_CIRCLE_CODE)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ant_opener, _ = create_cookie_opener()
    ant_page_size = clamp_ant_page_size(args.page_size)
    ant_jobs_raw, ant_total = collect_paginated(
        lambda page_index, page_size: fetch_ant_page(page_index, page_size, args.ant_batch_id, ant_opener),
        page_size=ant_page_size,
    )
    ant_jobs = [normalize_ant_job(job) for job in ant_jobs_raw]

    ali_opener, xsrf_token = init_alibaba_session(args.ali_batch_id, args.ali_circle_code)
    ali_jobs_raw, ali_total = collect_paginated(
        lambda page_index, page_size: fetch_alibaba_page(
            page_index,
            page_size,
            args.ali_batch_id,
            args.ali_circle_code,
            ali_opener,
            xsrf_token,
        ),
        page_size=args.page_size,
    )
    ali_jobs = [normalize_alibaba_job(job) for job in ali_jobs_raw]

    generated_at = datetime.now(timezone.utc).isoformat()
    combined = sorted(ali_jobs + ant_jobs, key=lambda row: (row["source"], str(row["position_id"])))

    ant_json = output_dir / f"antgroup_positions_{args.ant_batch_id}.json"
    ant_csv = output_dir / f"antgroup_positions_{args.ant_batch_id}.csv"
    ali_json = output_dir / f"alibaba_positions_{args.ali_batch_id}.json"
    ali_csv = output_dir / f"alibaba_positions_{args.ali_batch_id}.csv"
    combined_json = output_dir / "campus_positions_combined.json"
    combined_csv = output_dir / "campus_positions_combined.csv"

    write_json(
        ant_json,
        {
            "generated_at": generated_at,
            "source": "antgroup",
            "batch_id": args.ant_batch_id,
            "total_count": ant_total,
            "jobs": ant_jobs,
        },
    )
    write_csv(ant_csv, ant_jobs)

    write_json(
        ali_json,
        {
            "generated_at": generated_at,
            "source": "alibaba",
            "batch_id": args.ali_batch_id,
            "circle_code": args.ali_circle_code,
            "total_count": ali_total,
            "jobs": ali_jobs,
        },
    )
    write_csv(ali_csv, ali_jobs)

    write_json(
        combined_json,
        {
            "generated_at": generated_at,
            "sources": [
                {"source": "alibaba", "batch_id": args.ali_batch_id, "total_count": ali_total},
                {"source": "antgroup", "batch_id": args.ant_batch_id, "total_count": ant_total},
            ],
            "jobs": combined,
        },
    )
    write_csv(combined_csv, combined)

    print(f"Alibaba positions: {ali_total}")
    print(f"Ant Group positions: {ant_total}")
    print(f"Combined positions: {len(combined)}")
    print(f"Wrote {ali_json}")
    print(f"Wrote {ali_csv}")
    print(f"Wrote {ant_json}")
    print(f"Wrote {ant_csv}")
    print(f"Wrote {combined_json}")
    print(f"Wrote {combined_csv}")


if __name__ == "__main__":
    main()
