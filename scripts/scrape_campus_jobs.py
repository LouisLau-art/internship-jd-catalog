from __future__ import annotations

import argparse
import csv
import html
import json
import re
import ssl
import time
from datetime import datetime, timezone
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener


ANT_BATCH_ID = "26022600074513"
ANT_EXTRA_BATCH_IDS = ("25051200066269",)
ALI_BATCH_ID = "100000540002"
ALI_CIRCLE_CODE = "60000"
ALI_DAILY_BATCH_ID = "100000560002"
ALI_DAILY_CATEGORY_NAME = "技术类"
ALI_DAILY_OUTPUT_SUFFIX = "tech"
BYTEDANCE_EXPORT_GLOB = "bytedance_positions_*.json"
MEITUAN_EXPORT_GLOB = "meituan_positions.json"
JD_EXPORT_GLOB = "jd_positions.json"
HUAWEI_JOB_TYPE = "0"
HUAWEI_JOB_TYPES = "0"
HUAWEI_LANGUAGE = "zh_CN"
HUAWEI_RD_FAMILY_CODE = "JFC1"
HUAWEI_WUHAN_CITY_CODE = "Wuhan"
DEFAULT_PAGE_SIZE = 100
ANT_MAX_PAGE_SIZE = 40
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
REQUEST_RETRY_ATTEMPTS = 5
RETRYABLE_HTTP_CODES = {429, 500, 502, 503, 504}

CSV_COLUMNS = [
    "source",
    "company",
    "position_id",
    "parent_position_id",
    "job_requirement_id",
    "position_intention_id",
    "position_intention_name",
    "position_name",
    "position_url",
    "position_req_code",
    "batch_id",
    "batch_name",
    "category_name",
    "family_code",
    "family_name",
    "data_source",
    "work_locations",
    "interview_locations",
    "departments",
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

HTML_TAG_RE = re.compile(r"<[^>]+>")
HTML_BREAK_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)


def build_ant_position_url(position_id: int, tid: str | None) -> str:
    base = f"https://talent.antgroup.com/campus-position?positionId={position_id}"
    return f"{base}&tid={tid}" if tid else base


def build_alibaba_position_url(position_id: int) -> str:
    return f"https://campus-talent.alibaba.com/campus/position/{position_id}"


def build_huawei_position_url(job_id: int | str, data_source: int | str) -> str:
    return f"https://career.huawei.com/reccampportal/portal5/campus-recruitment-detail.html?jobId={job_id}&dataSource={data_source}"


def clamp_ant_page_size(page_size: int) -> int:
    return min(page_size, ANT_MAX_PAGE_SIZE)


def join_values(values: Any) -> str:
    if not values:
        return ""
    if isinstance(values, (list, tuple)):
        return " | ".join(str(value) for value in values if value not in (None, ""))
    return str(values)


def split_delimited_values(values: Any, delimiter: str = ",") -> list[str]:
    if not values:
        return []
    if isinstance(values, (list, tuple)):
        raw_values = values
    else:
        raw_values = str(values).split(delimiter)
    return [str(value).strip() for value in raw_values if str(value).strip()]


def normalize_huawei_locations(values: Any) -> str:
    return " | ".join(value.replace("\\", "/") for value in split_delimited_values(values))


def clean_html_text(value: Any) -> str:
    if not value:
        return ""
    text = HTML_BREAK_RE.sub("\n", str(value))
    text = HTML_TAG_RE.sub("", text)
    return html.unescape(text).strip()


def normalize_ant_job(job: dict[str, Any]) -> dict[str, Any]:
    graduation = job.get("graduationTime") or {}
    return {
        "source": "antgroup",
        "company": "Ant Group",
        "position_id": job.get("id"),
        "parent_position_id": "",
        "job_requirement_id": "",
        "position_intention_id": "",
        "position_intention_name": "",
        "position_name": job.get("name", ""),
        "position_url": build_ant_position_url(job.get("id"), job.get("tid")),
        "position_req_code": "",
        "batch_id": job.get("batchId", ""),
        "batch_name": job.get("batchName", ""),
        "category_name": job.get("categoryName", ""),
        "family_code": "",
        "family_name": "",
        "data_source": "",
        "work_locations": join_values(job.get("workLocations")),
        "interview_locations": join_values(job.get("interviewLocations")),
        "departments": "",
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


def build_ant_batch_id_list(primary_batch_id: str, extra_batch_ids: Any) -> list[str]:
    batch_ids = [str(primary_batch_id), *split_delimited_values(extra_batch_ids)]
    ordered: list[str] = []
    seen: set[str] = set()
    for batch_id in batch_ids:
        normalized = str(batch_id).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def normalize_alibaba_job(job: dict[str, Any]) -> dict[str, Any]:
    graduation = job.get("graduationTime") or {}
    return {
        "source": "alibaba",
        "company": "Alibaba",
        "position_id": job.get("id"),
        "parent_position_id": "",
        "job_requirement_id": "",
        "position_intention_id": "",
        "position_intention_name": "",
        "position_name": job.get("name", ""),
        "position_url": build_alibaba_position_url(job.get("id")),
        "position_req_code": "",
        "batch_id": job.get("batchId", ""),
        "batch_name": job.get("batchName", ""),
        "category_name": job.get("categoryName", ""),
        "family_code": "",
        "family_name": "",
        "data_source": "",
        "work_locations": join_values(job.get("workLocations")),
        "interview_locations": join_values(job.get("interviewLocations")),
        "departments": "",
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


def filter_jobs_by_category_name(rows: list[dict[str, Any]], category_name: str) -> list[dict[str, Any]]:
    if not category_name:
        return list(rows)
    return [row for row in rows if row.get("category_name") == category_name]


def resolve_huawei_graduate_item(job: dict[str, Any], detail: dict[str, Any]) -> str:
    job_type = str(detail.get("jobType") or job.get("jobType") or "")
    graduate_item = detail.get("graduateItem")
    if graduate_item in (None, ""):
        graduate_item = job.get("graduateItem")
    if job_type == "2":
        return "0"
    if graduate_item in (None, ""):
        return "2"
    return str(graduate_item)


def make_huawei_position_id(job_id: Any, position_intention_id: Any) -> str:
    if position_intention_id in (None, ""):
        return str(job_id)
    return f"{job_id}:{position_intention_id}"


def normalize_huawei_job(
    job: dict[str, Any],
    detail: dict[str, Any],
    intent: dict[str, Any] | None,
) -> dict[str, Any]:
    job_id = detail.get("jobId") or job.get("jobId")
    data_source = detail.get("dataSource") or job.get("dataSource") or 1
    intention_id = intent.get("positionIntentionId") if intent else ""
    intention_name = (intent.get("positionIntention") if intent else "") or ""
    base_name = detail.get("jobname") or job.get("jobname") or job.get("nameCn") or ""
    position_name = f"{base_name} - {intention_name}" if intention_name else base_name
    requirement = clean_html_text((intent or {}).get("jobDemand") or detail.get("jobRequire") or job.get("jobRequire"))
    description = clean_html_text((intent or {}).get("jobResponsibilities") or detail.get("mainBusiness") or job.get("mainBusiness"))
    work_locations = normalize_huawei_locations((intent or {}).get("jobPlaceName") or detail.get("jobArea") or job.get("jobArea"))
    family_code = detail.get("jobFamClsCode") or job.get("jobFamClsCode") or ""
    family_name = detail.get("jobFamilyName") or job.get("jobFamilyName") or ""
    return {
        "source": "huawei",
        "company": "Huawei",
        "position_id": make_huawei_position_id(job_id, intention_id),
        "parent_position_id": str(job_id),
        "job_requirement_id": detail.get("jobRequirementId", ""),
        "position_intention_id": intention_id,
        "position_intention_name": intention_name,
        "position_name": position_name,
        "position_url": build_huawei_position_url(job_id, data_source),
        "position_req_code": job.get("positionReqCode", ""),
        "batch_id": "",
        "batch_name": "Huawei Campus Internship",
        "category_name": family_code,
        "family_code": family_code,
        "family_name": family_name,
        "data_source": data_source,
        "work_locations": work_locations,
        "interview_locations": "",
        "departments": join_values(split_delimited_values((intent or {}).get("deptName"))),
        "circles": "",
        "circle_codes": "",
        "channels": "",
        "feature_tags": "",
        "publish_time": detail.get("effectiveDate") or job.get("effectiveDate", ""),
        "modify_time": detail.get("lastUpdateDate") or detail.get("issuanceStartDate") or job.get("lastUpdateDate", ""),
        "graduation_from": "",
        "graduation_to": "",
        "requirement": requirement,
        "description": description,
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
    last_error: Exception | None = None
    for attempt in range(1, REQUEST_RETRY_ATTEMPTS + 1):
        try:
            with opener.open(request, timeout=30) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset)
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code not in RETRYABLE_HTTP_CODES or attempt == REQUEST_RETRY_ATTEMPTS:
                raise RuntimeError(f"request failed for {request.full_url}: {exc.code} {detail}") from exc
            last_error = RuntimeError(f"request failed for {request.full_url}: {exc.code} {detail}")
        except (URLError, TimeoutError, ssl.SSLError) as exc:
            if attempt == REQUEST_RETRY_ATTEMPTS:
                raise RuntimeError(f"request failed for {request.full_url}: {exc}") from exc
            last_error = exc
        time.sleep(min(2 ** (attempt - 1), 4))
    if last_error is not None:
        raise RuntimeError(f"request failed for {request.full_url}: {last_error}") from last_error
    raise RuntimeError(f"request failed for {request.full_url}: unknown error")


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str], opener: Any) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    body = read_text(request, opener)
    return json.loads(body)


def get_json(url: str, headers: dict[str, str], opener: Any) -> Any:
    request = Request(url, headers=headers, method="GET")
    return json.loads(read_text(request, opener))


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


def fetch_huawei_page(page_index: int, page_size: int, opener: Any) -> dict[str, Any]:
    query = urlencode(
        {
            "curPage": page_index,
            "pageSize": page_size,
            "language": HUAWEI_LANGUAGE,
            "orderBy": "ISS_STARTDATE_DESC_AND_IS_HOT_JOB",
            "jobType": HUAWEI_JOB_TYPE,
            "jobTypes": HUAWEI_JOB_TYPES,
        }
    )
    response = get_json(
        f"https://career.huawei.com/reccampportal/services/portal/portalpub/getJob/newHr/page/{page_size}/{page_index}?{query}",
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "Referer": "https://career.huawei.com/reccampportal/portal5/campus-recruitment.html?jobTypes=0#jobRecommendBox",
        },
        opener,
    )
    return {"items": response["result"], "total": response["pageVO"]["totalRows"]}


def fetch_huawei_job_detail(job_id: Any, data_source: Any, opener: Any) -> dict[str, Any]:
    return get_json(
        f"https://career.huawei.com/reccampportal/services/portal/portalpub/getJobDetail/newHr?jobId={job_id}&dataSource={data_source}",
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "Referer": build_huawei_position_url(job_id, data_source),
        },
        opener,
    )


def fetch_huawei_intents(
    job_id: Any,
    job_requirement_id: Any,
    graduate_item: str,
    data_source: Any,
    opener: Any,
) -> list[dict[str, Any]]:
    query = urlencode({"dataSource": data_source, "jobId": job_id})
    return get_json(
        "https://career.huawei.com/reccampportal/services/portal/portaluser/"
        f"findIntentListByJobRequirementId/newHr/{HUAWEI_LANGUAGE}/{job_requirement_id}/{graduate_item}?{query}",
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "Referer": build_huawei_position_url(job_id, data_source),
        },
        opener,
    )


def expand_huawei_jobs(jobs: list[dict[str, Any]], opener: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for job in jobs:
        data_source = job.get("dataSource") or 1
        detail = fetch_huawei_job_detail(job["jobId"], data_source, opener)
        graduate_item = resolve_huawei_graduate_item(job, detail)
        intents: list[dict[str, Any]] = []
        if detail.get("jobRequirementId"):
            intents = fetch_huawei_intents(job["jobId"], detail["jobRequirementId"], graduate_item, data_source, opener)
        if intents:
            rows.extend(normalize_huawei_job(job, detail, intent) for intent in intents)
        else:
            rows.append(normalize_huawei_job(job, detail, None))
    return rows


def is_huawei_wuhan_rd_job(row: dict[str, Any]) -> bool:
    return row.get("source") == "huawei" and row.get("family_code") == HUAWEI_RD_FAMILY_CODE and "武汉" in row.get("work_locations", "")


def build_export_source_entry(payload: dict[str, Any], file_name: str) -> dict[str, Any]:
    entry = {
        "source": payload.get("source", ""),
        "file": file_name,
    }
    for key in (
        "company",
        "batch_id",
        "project_id",
        "project_name",
        "category_id",
        "category_name",
        "circle_code",
        "job_type",
        "job_types",
        "position_card_count",
        "expanded_intent_count",
        "source_total_count",
        "total_count",
        "generated_at",
    ):
        if key in payload and payload.get(key) not in (None, ""):
            entry[key] = payload.get(key)
    filters = payload.get("filters")
    if filters:
        entry["filters"] = filters
    return entry


def load_maintained_exports(output_dir: Path, glob_pattern: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_entries: list[dict[str, Any]] = []
    jobs: list[dict[str, Any]] = []
    for path in sorted(output_dir.glob(glob_pattern)):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload_jobs = payload.get("jobs") or []
        if not isinstance(payload_jobs, list):
            raise ValueError(f"jobs payload must be a list in {path}")
        source_entries.append(build_export_source_entry(payload, path.name))
        jobs.extend(payload_jobs)
    return source_entries, jobs


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in CSV_COLUMNS})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Scrape Alibaba, Ant Group, and Huawei campus job listings into JSON and CSV, "
            "then rebuild the combined export with maintained ByteDance raw snapshots."
        )
    )
    parser.add_argument("--output-dir", default="data", help="Directory for exported files.")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE, help="Page size for list requests.")
    parser.add_argument("--ant-batch-id", default=ANT_BATCH_ID)
    parser.add_argument("--ant-extra-batch-ids", default=",".join(ANT_EXTRA_BATCH_IDS))
    parser.add_argument("--ali-batch-id", default=ALI_BATCH_ID)
    parser.add_argument("--ali-circle-code", default=ALI_CIRCLE_CODE)
    parser.add_argument("--ali-daily-batch-id", default=ALI_DAILY_BATCH_ID)
    parser.add_argument("--ali-daily-circle-code", default=ALI_CIRCLE_CODE)
    parser.add_argument("--ali-daily-category-name", default=ALI_DAILY_CATEGORY_NAME)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ant_page_size = clamp_ant_page_size(args.page_size)
    ant_exports: list[dict[str, Any]] = []
    ant_jobs: list[dict[str, Any]] = []
    ant_source_entries: list[dict[str, Any]] = []
    for ant_batch_id in build_ant_batch_id_list(args.ant_batch_id, args.ant_extra_batch_ids):
        ant_opener, _ = create_cookie_opener()
        ant_jobs_raw, ant_total = collect_paginated(
            lambda page_index, page_size, batch_id=ant_batch_id: fetch_ant_page(page_index, page_size, batch_id, ant_opener),
            page_size=ant_page_size,
        )
        ant_batch_jobs = [normalize_ant_job(job) for job in ant_jobs_raw]
        ant_jobs.extend(ant_batch_jobs)
        ant_payload = {
            "generated_at": "",
            "source": "antgroup",
            "company": "Ant Group",
            "batch_id": ant_batch_id,
            "total_count": ant_total,
            "jobs": ant_batch_jobs,
        }
        ant_source_entries.append(build_export_source_entry(ant_payload, f"antgroup_positions_{ant_batch_id}.json"))
        ant_exports.append(
            {
                "batch_id": ant_batch_id,
                "total_count": ant_total,
                "jobs": ant_batch_jobs,
                "json_path": output_dir / f"antgroup_positions_{ant_batch_id}.json",
                "csv_path": output_dir / f"antgroup_positions_{ant_batch_id}.csv",
            }
        )

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

    ali_daily_total = 0
    ali_daily_source_total = 0
    ali_daily_jobs: list[dict[str, Any]] = []
    if args.ali_daily_batch_id:
        ali_daily_opener, ali_daily_xsrf_token = init_alibaba_session(args.ali_daily_batch_id, args.ali_daily_circle_code)
        ali_daily_jobs_raw, ali_daily_source_total = collect_paginated(
            lambda page_index, page_size: fetch_alibaba_page(
                page_index,
                page_size,
                args.ali_daily_batch_id,
                args.ali_daily_circle_code,
                ali_daily_opener,
                ali_daily_xsrf_token,
            ),
            page_size=args.page_size,
        )
        ali_daily_jobs = filter_jobs_by_category_name(
            [normalize_alibaba_job(job) for job in ali_daily_jobs_raw],
            args.ali_daily_category_name,
        )
        ali_daily_total = len(ali_daily_jobs)

    huawei_opener, _ = create_cookie_opener()
    huawei_jobs_raw, huawei_total = collect_paginated(
        lambda page_index, page_size: fetch_huawei_page(page_index, page_size, huawei_opener),
        page_size=args.page_size,
    )
    huawei_jobs = expand_huawei_jobs(huawei_jobs_raw, huawei_opener)
    huawei_wuhan_rd_jobs = [row for row in huawei_jobs if is_huawei_wuhan_rd_job(row)]
    bytedance_source_entries, bytedance_jobs = load_maintained_exports(output_dir, BYTEDANCE_EXPORT_GLOB)
    meituan_source_entries, meituan_jobs = load_maintained_exports(output_dir, MEITUAN_EXPORT_GLOB)
    jd_source_entries, jd_jobs = load_maintained_exports(output_dir, JD_EXPORT_GLOB)

    generated_at = datetime.now(timezone.utc).isoformat()
    combined = sorted(
        ali_jobs + ali_daily_jobs + ant_jobs + bytedance_jobs + huawei_jobs + meituan_jobs + jd_jobs,
        key=lambda row: (row["source"], str(row.get("batch_id", "")), str(row["position_id"])),
    )

    ali_json = output_dir / f"alibaba_positions_{args.ali_batch_id}.json"
    ali_csv = output_dir / f"alibaba_positions_{args.ali_batch_id}.csv"
    ali_daily_json = output_dir / f"alibaba_positions_{args.ali_daily_batch_id}_{ALI_DAILY_OUTPUT_SUFFIX}.json"
    ali_daily_csv = output_dir / f"alibaba_positions_{args.ali_daily_batch_id}_{ALI_DAILY_OUTPUT_SUFFIX}.csv"
    huawei_json = output_dir / "huawei_positions_intern.json"
    huawei_csv = output_dir / "huawei_positions_intern.csv"
    huawei_wuhan_rd_json = output_dir / "huawei_positions_wuhan_rd.json"
    huawei_wuhan_rd_csv = output_dir / "huawei_positions_wuhan_rd.csv"
    combined_json = output_dir / "campus_positions_combined.json"
    combined_csv = output_dir / "campus_positions_combined.csv"

    for ant_export in ant_exports:
        write_json(
            ant_export["json_path"],
            {
                "generated_at": generated_at,
                "source": "antgroup",
                "company": "Ant Group",
                "batch_id": ant_export["batch_id"],
                "total_count": ant_export["total_count"],
                "jobs": ant_export["jobs"],
            },
        )
        write_csv(ant_export["csv_path"], ant_export["jobs"])

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

    if args.ali_daily_batch_id:
        write_json(
            ali_daily_json,
            {
                "generated_at": generated_at,
                "source": "alibaba",
                "batch_id": args.ali_daily_batch_id,
                "circle_code": args.ali_daily_circle_code,
                "source_total_count": ali_daily_source_total,
                "total_count": ali_daily_total,
                "filters": {
                    "category_name": args.ali_daily_category_name,
                },
                "jobs": ali_daily_jobs,
            },
        )
        write_csv(ali_daily_csv, ali_daily_jobs)

    write_json(
        huawei_json,
        {
            "generated_at": generated_at,
            "source": "huawei",
            "job_type": HUAWEI_JOB_TYPE,
            "job_types": HUAWEI_JOB_TYPES,
            "position_card_count": huawei_total,
            "expanded_intent_count": len(huawei_jobs),
            "jobs": huawei_jobs,
        },
    )
    write_csv(huawei_csv, huawei_jobs)

    write_json(
        huawei_wuhan_rd_json,
        {
            "generated_at": generated_at,
            "source": "huawei",
            "filters": {
                "family_code": HUAWEI_RD_FAMILY_CODE,
                "city_code_contains": HUAWEI_WUHAN_CITY_CODE,
            },
            "total_count": len(huawei_wuhan_rd_jobs),
            "jobs": huawei_wuhan_rd_jobs,
        },
    )
    write_csv(huawei_wuhan_rd_csv, huawei_wuhan_rd_jobs)

    write_json(
        combined_json,
        {
            "generated_at": generated_at,
            "sources": [
                {"source": "alibaba", "batch_id": args.ali_batch_id, "total_count": ali_total},
                {
                    "source": "alibaba",
                    "batch_id": args.ali_daily_batch_id,
                    "source_total_count": ali_daily_source_total,
                    "total_count": ali_daily_total,
                    "filters": {"category_name": args.ali_daily_category_name},
                },
                *ant_source_entries,
                *bytedance_source_entries,
                *meituan_source_entries,
                *jd_source_entries,
                {
                    "source": "huawei",
                    "job_type": HUAWEI_JOB_TYPE,
                    "job_types": HUAWEI_JOB_TYPES,
                    "position_card_count": huawei_total,
                    "expanded_intent_count": len(huawei_jobs),
                },
            ],
            "jobs": combined,
        },
    )
    write_csv(combined_csv, combined)

    print(f"Alibaba positions: {ali_total}")
    if args.ali_daily_batch_id:
        print(
            "Alibaba daily positions: "
            f"{ali_daily_total} filtered rows from {ali_daily_source_total} total rows"
        )
    for ant_export in ant_exports:
        print(f"Ant Group positions ({ant_export['batch_id']}): {ant_export['total_count']}")
    for bytedance_source_entry in bytedance_source_entries:
        print(
            "ByteDance positions "
            f"({bytedance_source_entry.get('project_name', bytedance_source_entry['file'])}): "
            f"{bytedance_source_entry.get('total_count', 0)}"
        )
    print(f"Huawei position cards: {huawei_total}")
    print(f"Huawei expanded intent rows: {len(huawei_jobs)}")
    print(f"Huawei Wuhan R&D intent rows: {len(huawei_wuhan_rd_jobs)}")
    print(f"Combined positions: {len(combined)}")
    print(f"Wrote {ali_json}")
    print(f"Wrote {ali_csv}")
    if args.ali_daily_batch_id:
        print(f"Wrote {ali_daily_json}")
        print(f"Wrote {ali_daily_csv}")
    for ant_export in ant_exports:
        print(f"Wrote {ant_export['json_path']}")
        print(f"Wrote {ant_export['csv_path']}")
    print(f"Wrote {huawei_json}")
    print(f"Wrote {huawei_csv}")
    print(f"Wrote {huawei_wuhan_rd_json}")
    print(f"Wrote {huawei_wuhan_rd_csv}")
    print(f"Wrote {combined_json}")
    print(f"Wrote {combined_csv}")


if __name__ == "__main__":
    main()
