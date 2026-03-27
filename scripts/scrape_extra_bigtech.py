#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import requests

try:
    from scripts.scrape_campus_jobs import write_csv, write_json
except ModuleNotFoundError:
    from scrape_campus_jobs import write_csv, write_json


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
)

NETEASE_QUERY_URL = "https://hr.163.com/api/hr163/position/queryPage"
NETEASE_TECH_CATEGORIES = {"技术", "游戏程序", "人工智能"}
NETEASE_DETAIL_URL = "https://hr.163.com/job-detail.html?postId={position_id}"

PDD_INTERN_URL = "https://careers.pddglobalhr.com/campus/intern"
DIDI_TECH_URL_TEMPLATE = (
    "https://app.mokahr.com/apply/didiglobal/6222#/jobs"
    "?zhineng=48460&commitment=%E5%AE%9E%E4%B9%A0&page={page}"
)

XIAOMI_PORTAL_URL = "https://xiaomi.jobs.f.mioffice.cn/internship/"
XIAOMI_CSRF_URL = "https://xiaomi.jobs.f.mioffice.cn/api/v1/csrf/token"
XIAOMI_SEARCH_URL = "https://xiaomi.jobs.f.mioffice.cn/api/v1/search/job/posts"
XIAOMI_TECH_FUNCTIONS = {
    "软件研发类": "7178759516879405165",
    "硬件研发类": "7178830559051874412",
    "算法类": "7467761476330340460",
    "芯片类": "7542849286137479277",
    "测试类": "7467761529010634860",
    "运维类": "7467761246949179500",
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DIDI_JOB_RE = re.compile(
    r"\[([^\]]*?发布时间：\d{4}-\d{2}-\d{2})\]\((https://app\.mokahr\.com/apply/didiglobal/6222#/job/[^)]+)\)",
    re.DOTALL,
)
PDD_METADATA_LINES = {"技术专场", "技术"}
PDD_TAG_LINES = {"紧缺"}
JOB_TITLE_HINTS = ("实习", "工程师", "研发", "算法", "开发", "Agent", "AI")


def clean_line(value: str) -> str:
    value = value.replace("\\", " ").replace("\u00a0", " ").strip()
    if value.startswith("- "):
        value = value[2:].strip()
    return re.sub(r"\s+", " ", value)


def looks_like_job_title(value: str) -> bool:
    return any(token in value for token in JOB_TITLE_HINTS)


def request_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "user-agent": USER_AGENT,
            "accept-language": "zh-CN,zh;q=0.9",
        }
    )
    return session


def parse_pdd_markdown(markdown: str) -> list[dict[str, Any]]:
    lines = [clean_line(line) for line in markdown.splitlines()]
    lines = [line for line in lines if line]

    jobs: list[dict[str, Any]] = []
    buffer: list[str] = []
    in_listing = False

    for line in lines:
        if line == "职位标签":
            in_listing = True
            buffer = []
            continue
        if not in_listing:
            continue
        if line.startswith("共") and "岗位" in line:
            break

        buffer.append(line)
        if not DATE_RE.fullmatch(line):
            continue

        if len(buffer) < 5:
            buffer = []
            continue

        batch_name = buffer[-4]
        category = buffer[-3]
        location = buffer[-2]
        publish_date = buffer[-1]
        lead = buffer[:-4]
        title = next((item for item in lead if looks_like_job_title(item)), lead[0])
        feature_tags = list(dict.fromkeys(item for item in lead if item != title and item in PDD_TAG_LINES))

        if batch_name not in PDD_METADATA_LINES or category != "技术":
            buffer = []
            continue

        jobs.append(
            {
                "title": title,
                "batch_name": batch_name,
                "category": category,
                "location": location,
                "publish_date": publish_date,
                "feature_tags": feature_tags,
                "position_url": PDD_INTERN_URL,
            }
        )
        buffer = []

    return jobs


def parse_didi_markdown(markdown: str) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    for match in DIDI_JOB_RE.finditer(markdown):
        block = match.group(1).replace("\\", "\n")
        lines = [clean_line(line) for line in block.splitlines()]
        lines = [line for line in lines if line]
        if len(lines) < 4:
            continue
        title = lines[0].lstrip("急").strip()
        publish_date = lines[3].replace("发布时间：", "").strip()
        jobs.append(
            {
                "title": title,
                "batch_name": lines[1],
                "category": "技术类" if "技术类" in lines[1] else "",
                "location": lines[2],
                "publish_date": publish_date,
                "position_url": match.group(2),
            }
        )
    return jobs


def normalize_netease_job(job: dict[str, Any]) -> dict[str, Any]:
    position_id = str(job.get("id", ""))
    return {
        "source": "netease",
        "company": "NetEase",
        "position_id": position_id,
        "position_name": job.get("name", ""),
        "position_url": NETEASE_DETAIL_URL.format(position_id=position_id),
        "batch_name": "实习生招聘",
        "category_name": job.get("firstPostTypeName", ""),
        "departments": job.get("firstDepName", ""),
        "work_locations": " | ".join(job.get("workPlaceNameList") or []),
        "feature_tags": "GeekPassionateTalent" if job.get("geekPassionateTalentFlag") else "",
        "publish_time": job.get("updateTime", ""),
        "description": job.get("description", ""),
        "requirement": job.get("requirement", ""),
    }


def normalize_xiaomi_job(job: dict[str, Any]) -> dict[str, Any]:
    position_id = str(job.get("id", ""))
    cities = [city.get("name", "") for city in (job.get("city_list") or []) if city.get("name")]
    if not cities and (job.get("city_info") or {}).get("name"):
        cities = [job["city_info"]["name"]]

    recruit_type = job.get("recruit_type") or {}
    recruit_parent = recruit_type.get("parent") or {}
    feature_tags = [item for item in [(job.get("job_hot_flag") or {}).get("name")] if item]

    batch_bits = [recruit_parent.get("name", ""), recruit_type.get("name", "")]
    batch_name = " / ".join(bit for bit in batch_bits if bit)

    return {
        "source": "xiaomi",
        "company": "Xiaomi",
        "position_id": position_id,
        "position_name": job.get("title", ""),
        "position_url": f"https://xiaomi.jobs.f.mioffice.cn/internship/position/{position_id}/detail",
        "batch_name": batch_name,
        "category_name": (job.get("job_function") or {}).get("name", ""),
        "work_locations": " | ".join(cities),
        "feature_tags": " | ".join(feature_tags),
        "publish_time": job.get("publish_time", ""),
        "description": job.get("description", ""),
        "requirement": job.get("requirement", ""),
    }


def normalize_pdd_job(job: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "pinduoduo",
        "company": "Pinduoduo",
        "position_id": job["title"],
        "position_name": job["title"],
        "position_url": job["position_url"],
        "batch_name": job["batch_name"],
        "category_name": job["category"],
        "work_locations": job["location"],
        "feature_tags": " | ".join(job["feature_tags"]),
        "publish_time": job["publish_date"],
        "description": "拼多多技术专场实习生招聘",
        "requirement": "请通过官网岗位列表查看详情",
    }


def normalize_didi_job(job: dict[str, Any]) -> dict[str, Any]:
    position_id = job["position_url"].rsplit("/", 1)[-1]
    return {
        "source": "didi",
        "company": "Didi",
        "position_id": position_id,
        "position_name": job["title"],
        "position_url": job["position_url"],
        "batch_name": job["batch_name"],
        "category_name": job["category"],
        "work_locations": job["location"],
        "publish_time": job["publish_date"],
        "description": "滴滴技术类实习岗位",
        "requirement": "请通过岗位详情页查看完整 JD",
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


def extract_didi_max_page(markdown: str) -> int:
    lines = [clean_line(line) for line in markdown.splitlines()]
    lines = [line for line in lines if line]
    for line in reversed(lines):
        if line.isdigit() and len(line) > 1:
            return max(int(char) for char in line)
    return 1


def fetch_netease_rows(page_size: int = 100) -> list[dict[str, Any]]:
    session = request_session()
    page_no = 1
    deduped: dict[str, dict[str, Any]] = {}
    total_pages = 1

    while page_no <= total_pages:
        response = session.post(
            NETEASE_QUERY_URL,
            json={"currentPage": page_no, "pageSize": page_size, "workType": "1"},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()["data"]
        total_count = int(payload.get("total") or 0)
        total_pages = max(1, (total_count + page_size - 1) // page_size)
        for job in payload.get("list") or []:
            if job.get("firstPostTypeName") not in NETEASE_TECH_CATEGORIES:
                continue
            row = normalize_netease_job(job)
            deduped[row["position_id"]] = row
        page_no += 1

    return sorted(deduped.values(), key=lambda row: (row["category_name"], row["position_name"]))


def bootstrap_xiaomi_session() -> tuple[requests.Session, dict[str, str]]:
    session = request_session()
    session.get(XIAOMI_PORTAL_URL, timeout=30)
    csrf_headers = {
        "website-path": "internship",
        "portal-channel": "saas-career",
        "portal-platform": "pc",
        "content-type": "application/json",
        "referer": XIAOMI_PORTAL_URL,
    }
    response = session.post(
        XIAOMI_CSRF_URL,
        headers=csrf_headers,
        json={"portal_entrance": 1},
        timeout=30,
    )
    response.raise_for_status()
    csrf_token = response.json()["data"]["token"]
    search_headers = {
        "website-path": "internship",
        "portal-channel": "saas-career",
        "portal-platform": "pc",
        "content-type": "application/json",
        "accept": "application/json, text/plain, */*",
        "referer": XIAOMI_PORTAL_URL,
        "x-csrf-token": unquote(csrf_token),
        "env": "undefined",
    }
    return session, search_headers


def build_xiaomi_search_params(limit: int, offset: int, job_function_id: str) -> dict[str, Any]:
    return {
        "keyword": "",
        "limit": limit,
        "offset": offset,
        "job_category_id_list": "",
        "tag_id_list": "",
        "location_code_list": "",
        "subject_id_list": "",
        "recruitment_id_list": "",
        "portal_type": 6,
        "job_function_id_list": job_function_id,
        "storefront_id_list": "",
        "portal_entrance": 1,
        "_signature": "",
    }


def fetch_xiaomi_rows(page_size: int = 100) -> list[dict[str, Any]]:
    session, headers = bootstrap_xiaomi_session()
    deduped: dict[str, dict[str, Any]] = {}

    for _, function_id in XIAOMI_TECH_FUNCTIONS.items():
        offset = 0
        total = None
        while total is None or offset < total:
            payload = {
                "keyword": "",
                "limit": page_size,
                "offset": offset,
                "job_category_id_list": [],
                "tag_id_list": [],
                "location_code_list": [],
                "subject_id_list": [],
                "recruitment_id_list": [],
                "portal_type": 6,
                "job_function_id_list": [function_id],
                "storefront_id_list": [],
                "portal_entrance": 1,
            }
            response = session.post(
                XIAOMI_SEARCH_URL,
                params=build_xiaomi_search_params(page_size, offset, function_id),
                headers=headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()["data"]
            total = int(data.get("count") or 0)
            jobs = data.get("job_post_list") or []
            if not jobs:
                break
            for job in jobs:
                row = normalize_xiaomi_job(job)
                deduped[row["position_id"]] = row
            offset += page_size

    return sorted(deduped.values(), key=lambda row: (row["category_name"], row["position_name"]))


def fetch_pdd_rows(firecrawl_dir: Path, use_cached_firecrawl: bool) -> list[dict[str, Any]]:
    path = firecrawl_dir / "pdd-intern.md"
    markdown = path.read_text(encoding="utf-8") if use_cached_firecrawl and path.exists() else scrape_with_firecrawl(PDD_INTERN_URL, path)
    return [normalize_pdd_job(job) for job in parse_pdd_markdown(markdown)]


def fetch_didi_rows(firecrawl_dir: Path, use_cached_firecrawl: bool) -> list[dict[str, Any]]:
    page_one_path = firecrawl_dir / "didi-intern-page-1.md"
    page_one_url = DIDI_TECH_URL_TEMPLATE.format(page=1)
    page_one_markdown = (
        page_one_path.read_text(encoding="utf-8")
        if use_cached_firecrawl and page_one_path.exists()
        else scrape_with_firecrawl(page_one_url, page_one_path)
    )

    max_page = extract_didi_max_page(page_one_markdown)
    deduped: dict[str, dict[str, Any]] = {}
    for job in parse_didi_markdown(page_one_markdown):
        normalized = normalize_didi_job(job)
        deduped[normalized["position_id"]] = normalized

    for page in range(2, max_page + 1):
        path = firecrawl_dir / f"didi-intern-page-{page}.md"
        markdown = path.read_text(encoding="utf-8") if use_cached_firecrawl and path.exists() else scrape_with_firecrawl(
            DIDI_TECH_URL_TEMPLATE.format(page=page),
            path,
        )
        jobs = parse_didi_markdown(markdown)
        if not jobs:
            break
        for job in jobs:
            normalized = normalize_didi_job(job)
            deduped[normalized["position_id"]] = normalized

    return sorted(deduped.values(), key=lambda row: row["position_name"])


def export_company(
    output_dir: Path,
    file_prefix: str,
    company: str,
    rows: list[dict[str, Any]],
    generated_at: str,
    **metadata: Any,
) -> None:
    json_path = output_dir / f"{file_prefix}.json"
    csv_path = output_dir / f"{file_prefix}.csv"
    payload = {
        "generated_at": generated_at,
        "source": rows[0]["source"] if rows else file_prefix,
        "company": company,
        "total_count": len(rows),
        "jobs": rows,
    }
    payload.update(metadata)
    write_json(json_path, payload)
    write_csv(csv_path, rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape NetEase, Xiaomi, Pinduoduo, and Didi tech internships.")
    parser.add_argument("--output-dir", default="data", help="Directory for exported files.")
    parser.add_argument("--firecrawl-dir", default=".firecrawl", help="Directory for cached firecrawl markdown.")
    parser.add_argument("--use-cached-firecrawl", action="store_true", help="Reuse existing firecrawl markdown if present.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    firecrawl_dir = Path(args.firecrawl_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    firecrawl_dir.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).isoformat()

    netease_rows = fetch_netease_rows()
    xiaomi_rows = fetch_xiaomi_rows()
    pdd_rows = fetch_pdd_rows(firecrawl_dir, use_cached_firecrawl=args.use_cached_firecrawl)
    didi_rows = fetch_didi_rows(firecrawl_dir, use_cached_firecrawl=args.use_cached_firecrawl)

    export_company(
        output_dir,
        "netease_positions_intern_tech",
        "NetEase",
        netease_rows,
        generated_at,
        filters={"first_post_type_name": sorted(NETEASE_TECH_CATEGORIES)},
    )
    export_company(
        output_dir,
        "xiaomi_positions_intern_tech",
        "Xiaomi",
        xiaomi_rows,
        generated_at,
        filters={"job_function_ids": XIAOMI_TECH_FUNCTIONS},
    )
    export_company(
        output_dir,
        "pinduoduo_positions_intern_tech",
        "Pinduoduo",
        pdd_rows,
        generated_at,
        filters={"category_name": "技术"},
    )
    export_company(
        output_dir,
        "didi_positions_intern_tech",
        "Didi",
        didi_rows,
        generated_at,
        filters={"zhineng": "48460", "commitment": "实习"},
    )

    combined_rows = sorted(
        netease_rows + xiaomi_rows + pdd_rows + didi_rows,
        key=lambda row: (row["source"], row["category_name"], row["position_name"]),
    )
    export_company(
        output_dir,
        "extra_bigtech_positions",
        "Extra Big Tech",
        combined_rows,
        generated_at,
        sources=[
            {"source": "netease", "count": len(netease_rows)},
            {"source": "xiaomi", "count": len(xiaomi_rows)},
            {"source": "pinduoduo", "count": len(pdd_rows)},
            {"source": "didi", "count": len(didi_rows)},
        ],
    )

    print(
        json.dumps(
            {
                "generated_at": generated_at,
                "netease": len(netease_rows),
                "xiaomi": len(xiaomi_rows),
                "pinduoduo": len(pdd_rows),
                "didi": len(didi_rows),
                "combined": len(combined_rows),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
