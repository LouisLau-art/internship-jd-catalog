#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import hmac
import json
import re
import shutil
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

import requests

try:
    from scripts.scrape_campus_jobs import write_csv, write_json
except ModuleNotFoundError:
    from scrape_campus_jobs import write_csv, write_json


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
)

KUAISHOU_LIST_URL = "https://zhaopin.kuaishou.cn/recruit/#/official/trainee/"
KUAISHOU_API_URL = "https://zhaopin.kuaishou.cn/recruit/e/api/v1/open/positions/simple"
KUAISHOU_SECRET = "652f962a-0575-4575-98d2-f04e2291bee2"
KUAISHOU_TECH_CATEGORY_CODES = {
    "J0011": "算法类",
    "J0012": "工程类",
}
KUAISHOU_EXCLUDED_TITLE_KEYWORDS = (
    "设计师",
    "剧情策划",
    "技术美术",
)
KUAISHOU_LOCATION_NAMES = {
    "Beijing": "北京",
    "Shanghai": "上海",
    "Guangzhou": "广州",
    "Shenzhen": "深圳",
    "Tianjin": "天津",
    "Hangzhou": "杭州",
    "Chengdu": "成都",
    "Shenyang": "沈阳",
    "Changchun": "长春",
    "Wuxi": "无锡",
    "Tongren": "铜仁",
    "Suzhou": "苏州",
    "LosAngeles": "洛杉矶",
}

HONOR_LIST_URL = "https://career.honor.com/SU61b9b9992f9d24431f5050a5/pb/interns.html"
HONOR_API_URL = (
    "https://career.honor.com/wecruit/positionInfo/listPosition/"
    "SU61b9b9992f9d24431f5050a5?iSaJAx=isAjax&request_locale=zh_CN&t={timestamp}"
)

BILIBILI_INTERN_URL = "https://jobs.bilibili.com/campus/positions?code=01&practiceTypes=1,2&type=0"
BILIBILI_JOB_COUNT_RE = re.compile(r"职位列表\s*[（(](\d+)[）)]")
BILIBILI_APP_KEY = "ops.ehr-api.auth"
BILIBILI_POSITION_LIST_URL = "https://jobs.bilibili.com/api/campus/position/positionList"
BILIBILI_POSITION_PAGE_URL = "https://jobs.bilibili.com/campus/positions/{position_id}"
BILIBILI_BOOTSTRAP_SELECTOR = ".space > a.bili-item-card"
BILIBILI_BOOTSTRAP_WAIT_MS = 15000

OPPO_LIST_URL = "https://careers.oppo.com/university/oppo/campus/post?recruitType=Intern"
OPPO_PROJECT_LIST_URL = "https://careers.oppo.com/openapi/position/project/list"
OPPO_POSITION_PAGE_URL = "https://careers.oppo.com/openapi/position/pageNew"
OPPO_TECH_POSITION_TYPES = {
    "AI/algorithm": "AI/算法类",
    "Standard_research": "标准研究类",
    "Software": "软件类",
    "Hardware_class": "硬件类",
    "Engineering_Technology": "工程技术类",
}


def request_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "user-agent": USER_AGENT,
            "accept-language": "zh-CN,zh;q=0.9",
        }
    )
    return session


def clean_line(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u00a0", " ").strip())


def canonicalize_kuaishou_params(params: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in sorted(params):
        value = params[key]
        if value in (None, "", []):
            continue
        if isinstance(value, (list, tuple)):
            values = sorted(str(item) for item in value if item not in (None, ""))
            if not values:
                continue
            value = ",".join(values)
        parts.append(f"{key}={quote_plus(str(value))}")
    return "&".join(parts)


def build_kuaishou_signature(
    *,
    secret: str,
    timestamp: str,
    params: dict[str, Any],
    body: str = "",
) -> str:
    canonical = canonicalize_kuaishou_params(params)
    message = f"{timestamp}{canonical}{body}{secret}"
    return hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()


def is_kuaishou_tech_job(job: dict[str, Any]) -> bool:
    category_code = str(job.get("positionCategoryCode") or "")
    if category_code not in KUAISHOU_TECH_CATEGORY_CODES:
        return False
    title = str(job.get("name") or "")
    return not any(keyword in title for keyword in KUAISHOU_EXCLUDED_TITLE_KEYWORDS)


def normalize_kuaishou_locations(job: dict[str, Any]) -> str:
    values = job.get("workLocationsCode") or []
    if not values and job.get("workLocationCode"):
        values = [job["workLocationCode"]]
    normalized = [KUAISHOU_LOCATION_NAMES.get(code, code) for code in values if code]
    return " | ".join(normalized)


def normalize_kuaishou_job(job: dict[str, Any]) -> dict[str, Any]:
    category_code = str(job.get("positionCategoryCode") or "")
    return {
        "source": "kuaishou",
        "company": "Kuaishou",
        "position_id": str(job.get("id") or ""),
        "position_name": job.get("name", ""),
        "position_url": KUAISHOU_LIST_URL,
        "batch_name": "日常实习",
        "category_name": KUAISHOU_TECH_CATEGORY_CODES.get(category_code, category_code),
        "work_locations": normalize_kuaishou_locations(job),
        "departments": job.get("departmentName") or job.get("departmentCode") or "",
        "feature_tags": "",
        "publish_time": job.get("updateTime") or job.get("releaseTime") or "",
        "description": job.get("description", ""),
        "requirement": job.get("positionDemand", ""),
    }


def honor_rows_from_page_data(page_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [normalize_honor_job(job) for job in page_data if job.get("postTypeName") == "研发类" and job.get("workTypeStr") == "实习"]


def normalize_honor_job(job: dict[str, Any]) -> dict[str, Any]:
    locations = [clean_line(part) for part in str(job.get("workPlaceStr") or "").split("、") if clean_line(part)]
    return {
        "source": "honor",
        "company": "Honor",
        "position_id": str(job.get("postId") or ""),
        "position_name": job.get("postName", ""),
        "position_url": HONOR_LIST_URL,
        "position_req_code": job.get("postCode", ""),
        "batch_name": job.get("projectName", ""),
        "category_name": job.get("postTypeName", ""),
        "work_locations": " | ".join(locations),
        "departments": job.get("company", ""),
        "feature_tags": job.get("educationStr", ""),
        "publish_time": job.get("publishDate", ""),
        "description": "",
        "requirement": job.get("educationStr", ""),
    }


def parse_bilibili_job_count(markdown: str) -> int:
    match = BILIBILI_JOB_COUNT_RE.search(markdown)
    if not match:
        raise ValueError("Could not find Bilibili job count in markdown")
    return int(match.group(1))


def normalize_bilibili_locations(value: str) -> str:
    parts = [clean_line(part) for part in re.split(r"[\\/]", value or "") if clean_line(part)]
    return " | ".join(parts)


def normalize_bilibili_description_text(value: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", "", value or ""))
    lines = [clean_line(line) for line in text.replace("\r", "\n").split("\n")]
    return "\n".join(line for line in lines if line)


def split_bilibili_position_description(value: str) -> tuple[str, str]:
    text = normalize_bilibili_description_text(value)
    match = re.search(r"工作职责[:：]\s*(.*?)\s*工作要求[:：]\s*(.*)$", text, flags=re.S)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    requirement_match = re.search(r"工作要求[:：]\s*(.*)$", text, flags=re.S)
    if requirement_match:
        return "", requirement_match.group(1).strip()
    return text, ""


def normalize_bilibili_job(job: dict[str, Any]) -> dict[str, Any]:
    position_id = str(job.get("id") or "")
    description, requirement = split_bilibili_position_description(str(job.get("positionDescription") or ""))
    feature_tags = []
    if job.get("hotRecruit"):
        feature_tags.append("热门职位")
    if job.get("campusProjectId"):
        feature_tags.append(f"campusProjectId={job['campusProjectId']}")
    return {
        "source": "bilibili",
        "company": "Bilibili",
        "position_id": position_id,
        "position_name": job.get("positionName", ""),
        "position_url": BILIBILI_POSITION_PAGE_URL.format(position_id=position_id),
        "batch_name": "实习生招聘",
        "category_name": job.get("postCodeName", ""),
        "work_locations": normalize_bilibili_locations(str(job.get("workLocation") or job.get("workCity") or "")),
        "departments": "",
        "feature_tags": " | ".join(feature_tags),
        "publish_time": job.get("pushTime") or job.get("ctime") or "",
        "description": description,
        "requirement": requirement,
        "hot_recruit": bool(job.get("hotRecruit")),
        "campus_project_id": str(job.get("campusProjectId") or ""),
        "recruit_type": str(job.get("recruitType") or ""),
    }


def bootstrap_bilibili_api_context() -> tuple[dict[str, str], dict[str, str]]:
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Playwright is required to bootstrap the Bilibili anti-bot session. "
            "Install it in the Python environment used to run this script."
        ) from exc

    captured_headers: dict[str, str] = {}
    cookies: dict[str, str] = {}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        def on_request(request: Any) -> None:
            if request.url == BILIBILI_POSITION_LIST_URL and not captured_headers:
                captured_headers.update(dict(request.headers))

        page.on("request", on_request)
        page.goto(BILIBILI_INTERN_URL, wait_until="domcontentloaded")
        page.wait_for_selector(BILIBILI_BOOTSTRAP_SELECTOR, timeout=BILIBILI_BOOTSTRAP_WAIT_MS)
        page.wait_for_timeout(1000)
        for cookie in page.context.cookies():
            domain = str(cookie.get("domain") or "")
            if "bilibili.com" not in domain:
                continue
            name = str(cookie.get("name") or "")
            value = str(cookie.get("value") or "")
            if name and value:
                cookies[name] = value
        browser.close()

    if not captured_headers:
        raise RuntimeError("Could not capture Bilibili positionList request headers from the browser bootstrap")
    if "x-csrf" not in captured_headers:
        raise RuntimeError("Could not capture Bilibili x-csrf header from the browser bootstrap")

    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://jobs.bilibili.com",
        "user-agent": captured_headers.get("user-agent", USER_AGENT),
        "x-appkey": captured_headers.get("x-appkey", BILIBILI_APP_KEY),
        "x-channel": captured_headers.get("x-channel", "campus"),
        "x-csrf": captured_headers["x-csrf"],
        "x-usertype": captured_headers.get("x-usertype", "2"),
        "lunar-id": f"lunar-scrape-{uuid.uuid4()}",
    }
    for key in ("sec-ch-ua", "sec-ch-ua-mobile", "sec-ch-ua-platform"):
        value = captured_headers.get(key)
        if value:
            headers[key] = value
    return headers, cookies


def build_bilibili_session() -> requests.Session:
    session = request_session()
    headers, cookies = bootstrap_bilibili_api_context()
    session.headers.update(headers)
    for name, value in cookies.items():
        session.cookies.set(name, value, domain=".bilibili.com", path="/")
    return session


def build_bilibili_position_list_payload(*, page_num: int, page_size: int) -> dict[str, Any]:
    return {
        "pageSize": page_size,
        "pageNum": page_num,
        "positionName": "",
        "postCode": ["01"],
        "postCodeList": ["01"],
        "workLocationList": [],
        "workTypeList": ["0"],
        "positionTypeList": ["0"],
        "deptCodeList": [],
        "recruitType": None,
        "practiceTypes": ["1", "2"],
        "onlyHotRecruit": 0,
    }


def fetch_bilibili_page(session: requests.Session, *, page_num: int, page_size: int = 100) -> dict[str, Any]:
    response = session.post(
        BILIBILI_POSITION_LIST_URL,
        json=build_bilibili_position_list_payload(page_num=page_num, page_size=page_size),
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("code") != 0:
        raise RuntimeError(f"Bilibili positionList request failed: {payload}")
    data = payload.get("data") or {}
    if not isinstance(data, dict):
        raise RuntimeError("Bilibili positionList response data is not an object")
    return data


def is_oppo_tech_job(job: dict[str, Any]) -> bool:
    return str(job.get("positionType") or "") in OPPO_TECH_POSITION_TYPES


def normalize_oppo_job(job: dict[str, Any]) -> dict[str, Any]:
    cities = [clean_line(part) for part in str(job.get("workCityName") or "").split(",") if clean_line(part)]
    position_type = str(job.get("positionType") or "")
    return {
        "source": "oppo",
        "company": "OPPO",
        "position_id": str(job.get("idRecruitPosition") or ""),
        "position_name": job.get("positionName", ""),
        "position_url": OPPO_LIST_URL,
        "batch_name": job.get("projectName", ""),
        "category_name": job.get("positionTypeName") or OPPO_TECH_POSITION_TYPES.get(position_type, position_type),
        "work_locations": " | ".join(cities),
        "feature_tags": job.get("specialRecruitment", ""),
        "publish_time": job.get("releaseTime", ""),
        "description": job.get("positionDesc", ""),
        "requirement": job.get("positionRequire", ""),
    }


def scrape_with_firecrawl(url: str, output_path: Path, wait_for_ms: int = 3000) -> str:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    firecrawl = shutil.which("firecrawl")
    if not firecrawl:
        raise RuntimeError("firecrawl CLI not found")
    subprocess.run(
        [
            firecrawl,
            "scrape",
            url,
            "--wait-for",
            str(wait_for_ms),
            "-o",
            str(output_path),
        ],
        check=True,
        text=True,
    )
    return output_path.read_text(encoding="utf-8")


def fetch_kuaishou_rows(page_size: int = 100) -> list[dict[str, Any]]:
    session = request_session()
    page_num = 1
    total_pages = 1
    deduped: dict[str, dict[str, Any]] = {}

    while page_num <= total_pages:
        params = {
            "pageNum": page_num,
            "pageSize": page_size,
            "positionNatureCode": "C002",
            "workLocationCode": "domestic",
        }
        timestamp = str(int(time.time() * 1000))
        sign = build_kuaishou_signature(
            secret=KUAISHOU_SECRET,
            timestamp=timestamp,
            params=params,
        )
        headers = {
            "signTimestamp": timestamp,
            "sign": sign,
            "referer": "https://zhaopin.kuaishou.cn/recruit/",
            "accept": "application/json, text/plain, */*",
        }
        response = session.get(KUAISHOU_API_URL, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        payload = response.json()["result"]
        total_pages = int(payload.get("pages") or 1)
        for job in payload.get("list") or []:
            if not is_kuaishou_tech_job(job):
                continue
            row = normalize_kuaishou_job(job)
            deduped[row["position_id"]] = row
        page_num += 1

    return sorted(deduped.values(), key=lambda row: (row["category_name"], row["position_name"]))


def fetch_honor_rows(page_size: int = 15) -> list[dict[str, Any]]:
    session = request_session()
    page = 1
    total_pages = 1
    deduped: dict[str, dict[str, Any]] = {}

    while page <= total_pages:
        response = session.post(
            HONOR_API_URL.format(timestamp=int(time.time() * 1000)),
            data={
                "isFrompb": "true",
                "recruitType": "12",
                "pageSize": str(page_size),
                "currentPage": str(page),
            },
            headers={"content-type": "application/x-www-form-urlencoded; charset=UTF-8"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()["data"]["pageForm"]
        total_pages = int(data.get("totalPage") or 1)
        for row in honor_rows_from_page_data(data.get("pageData") or []):
            deduped[row["position_id"]] = row
        page += 1

    return sorted(deduped.values(), key=lambda row: row["position_name"])


def fetch_bilibili_rows(firecrawl_dir: Path, use_cached_firecrawl: bool) -> tuple[list[dict[str, Any]], int]:
    try:
        session = build_bilibili_session()
        page_num = 1
        total_pages = 1
        reported_total_count = 0
        deduped: dict[str, dict[str, Any]] = {}

        while page_num <= total_pages:
            data = fetch_bilibili_page(session, page_num=page_num, page_size=100)
            total_pages = int(data.get("pages") or 1)
            reported_total_count = int(data.get("total") or reported_total_count)
            for job in data.get("list") or []:
                row = normalize_bilibili_job(job)
                deduped[row["position_id"]] = row
            page_num += 1

        rows = sorted(deduped.values(), key=lambda row: row["position_name"])
        if reported_total_count and len(rows) != reported_total_count:
            raise RuntimeError(
                f"Bilibili position count mismatch: expected {reported_total_count}, got {len(rows)}"
            )
        return rows, reported_total_count or len(rows)
    except Exception:
        if not use_cached_firecrawl:
            raise
        path = firecrawl_dir / "bilibili-tech-intern.md"
        if not path.exists():
            raise
        markdown = path.read_text(encoding="utf-8")
        count = parse_bilibili_job_count(markdown)
        return [], count


def resolve_oppo_intern_project(session: requests.Session) -> dict[str, Any]:
    response = session.get(
        OPPO_PROJECT_LIST_URL,
        headers={"accept": "application/json, text/plain, */*", "referer": OPPO_LIST_URL},
        timeout=30,
    )
    response.raise_for_status()
    projects = response.json()["data"] or []
    intern_projects = [project for project in projects if project.get("recruitmentType") == "Intern"]
    if not intern_projects:
        raise RuntimeError("Could not find OPPO internship project")
    project = max(intern_projects, key=lambda item: int(item.get("idRecruitProject") or 0))
    return {
        "projectId": project["idRecruitProject"],
        "recruitmentType": project["recruitmentType"],
        "isAllNode": "Y",
        "themeList": [],
    }


def fetch_oppo_rows(page_size: int = 100) -> list[dict[str, Any]]:
    session = request_session()
    project = resolve_oppo_intern_project(session)
    page = 1
    total_pages = 1
    deduped: dict[str, dict[str, Any]] = {}

    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json;charset=UTF-8",
        "referer": OPPO_LIST_URL,
    }

    while page <= total_pages:
        payload = {
            "pageNum": page,
            "pageSize": page_size,
            "positionName": "",
            "projectList": [project],
            "positionTypeList": [],
            "workCityCodeList": [],
            "shareId": "",
        }
        response = session.post(OPPO_POSITION_PAGE_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()["data"]
        total_pages = int(data.get("pages") or 1)
        for job in data.get("records") or []:
            if not is_oppo_tech_job(job):
                continue
            row = normalize_oppo_job(job)
            deduped[row["position_id"]] = row
        page += 1

    return sorted(deduped.values(), key=lambda row: (row["category_name"], row["position_name"]))


def export_company(
    output_dir: Path,
    file_prefix: str,
    *,
    source: str,
    company: str,
    rows: list[dict[str, Any]],
    generated_at: str,
    reported_total_count: int | None = None,
    **metadata: Any,
) -> None:
    payload = {
        "generated_at": generated_at,
        "source": source,
        "company": company,
        "total_count": reported_total_count if reported_total_count is not None else len(rows),
        "jobs": rows,
    }
    payload.update(metadata)
    write_json(output_dir / f"{file_prefix}.json", payload)
    write_csv(output_dir / f"{file_prefix}.csv", rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Kuaishou, Honor, OPPO, and Bilibili tech internship exports.")
    parser.add_argument("--output-dir", default="data", help="Directory for exported files.")
    parser.add_argument("--firecrawl-dir", default=".firecrawl", help="Directory for cached firecrawl markdown.")
    parser.add_argument("--use-cached-firecrawl", action="store_true", help="Reuse existing firecrawl markdown if present.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    firecrawl_dir = Path(args.firecrawl_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    firecrawl_dir.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).isoformat()

    kuaishou_rows = fetch_kuaishou_rows()
    honor_rows = fetch_honor_rows()
    oppo_rows = fetch_oppo_rows()
    bilibili_rows, bilibili_count = fetch_bilibili_rows(
        firecrawl_dir,
        use_cached_firecrawl=args.use_cached_firecrawl,
    )

    export_company(
        output_dir,
        "kuaishou_positions_intern_tech",
        source="kuaishou",
        company="Kuaishou",
        rows=kuaishou_rows,
        generated_at=generated_at,
        filters={"positionNatureCode": "C002", "positionCategoryCodes": KUAISHOU_TECH_CATEGORY_CODES},
    )
    export_company(
        output_dir,
        "honor_positions_intern_tech",
        source="honor",
        company="Honor",
        rows=honor_rows,
        generated_at=generated_at,
        filters={"recruitType": 12, "postTypeName": "研发类"},
    )
    export_company(
        output_dir,
        "oppo_positions_intern_tech",
        source="oppo",
        company="OPPO",
        rows=oppo_rows,
        generated_at=generated_at,
        filters={"positionTypes": OPPO_TECH_POSITION_TYPES, "recruitmentType": "Intern"},
    )
    export_company(
        output_dir,
        "bilibili_positions_intern_tech",
        source="bilibili",
        company="Bilibili",
        rows=bilibili_rows,
        generated_at=generated_at,
        reported_total_count=bilibili_count,
        filters={"code": "01", "practiceTypes": [1, 2], "type": 0},
        note=(
            "Structured export is sourced from the Bilibili campus position API under "
            "code=01 + practiceTypes=1,2, using a browser-bootstrapped anti-bot session "
            "captured on 2026-03-29."
        ),
    )

    combined_rows = sorted(
        kuaishou_rows + honor_rows + oppo_rows + bilibili_rows,
        key=lambda row: (row["source"], row["category_name"], row["position_name"]),
    )
    export_company(
        output_dir,
        "more_bigtech_positions",
        source="more_bigtech",
        company="More Big Tech",
        rows=combined_rows,
        generated_at=generated_at,
        sources=[
            {"source": "kuaishou", "count": len(kuaishou_rows)},
            {"source": "honor", "count": len(honor_rows)},
            {"source": "oppo", "count": len(oppo_rows)},
            {"source": "bilibili", "count": bilibili_count},
        ],
    )

    print(
        json.dumps(
            {
                "generated_at": generated_at,
                "kuaishou": len(kuaishou_rows),
                "honor": len(honor_rows),
                "oppo": len(oppo_rows),
                "bilibili": bilibili_count,
                "combined": len(combined_rows),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
