#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.company_registry import (
    REPO_ROOT,
    CompanyConfig,
    count_company_jobs,
    get_company_config,
    group_companies_by_scrape_group,
    parse_company_keys,
)


SCRAPE_GROUP_SCRIPTS = {
    "campus_core": REPO_ROOT / "scripts" / "scrape_campus_jobs.py",
    "extra_bigtech": REPO_ROOT / "scripts" / "scrape_extra_bigtech.py",
    "more_bigtech": REPO_ROOT / "scripts" / "scrape_more_bigtech.py",
}


@dataclass(frozen=True)
class ScrapeExecutionJob:
    group_key: str
    script_path: Path
    companies: tuple[CompanyConfig, ...]
    command: tuple[str, ...]


def build_status_doc_path(group_key: str, on_date: date | None = None) -> Path:
    current = on_date or date.today()
    return REPO_ROOT / "docs" / "temp" / f"{current.isoformat()}-{group_key.replace('_', '-')}-crawl-status.md"


def build_scrape_execution_plan(company_keys: list[str], refresh_mode: str = "live") -> list[ScrapeExecutionJob]:
    grouped = group_companies_by_scrape_group(company_keys)
    jobs: list[ScrapeExecutionJob] = []
    for group_key, companies in grouped.items():
        script_path = SCRAPE_GROUP_SCRIPTS[group_key]
        command = [sys.executable, str(script_path)]
        if refresh_mode == "cached" and group_key in {"extra_bigtech", "more_bigtech"}:
            command.append("--use-cached-firecrawl")
        jobs.append(
            ScrapeExecutionJob(
                group_key=group_key,
                script_path=script_path,
                companies=tuple(companies),
                command=tuple(command),
            )
        )
    return jobs


def load_company_summary(company: CompanyConfig) -> dict[str, object]:
    payload = json.loads(company.data_json.read_text(encoding="utf-8"))
    return {
        "company": company.display_name,
        "source_label": company.source_label,
        "count": count_company_jobs(payload, company),
        "data_json": str(company.data_json),
    }


def write_group_status_doc(group_key: str, companies: tuple[CompanyConfig, ...], refresh_mode: str, on_date: date | None = None) -> Path:
    current = on_date or date.today()
    path = build_status_doc_path(group_key, current)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# {group_key.replace('_', ' ').title()} Crawl Status",
        "",
        f"更新时间：`{current.isoformat()}`",
        f"刷新模式：`{refresh_mode}`",
        "",
        "| 公司 | 状态 | 岗位数量 | 数据文件 |",
        "| --- | --- | ---: | --- |",
    ]

    for company in companies:
        summary = load_company_summary(company)
        lines.append(
            f"| {summary['company']} | refreshed | {summary['count']} | `{Path(summary['data_json']).name}` |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def run_scrape_jobs(jobs: list[ScrapeExecutionJob], refresh_mode: str) -> list[Path]:
    written_docs: list[Path] = []
    for job in jobs:
        subprocess.run(list(job.command), cwd=REPO_ROOT, check=True)
        written_docs.append(write_group_status_doc(job.group_key, job.companies, refresh_mode))
    return written_docs


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh selected internship company exports by scrape family.")
    parser.add_argument("--companies", required=True, help="Comma-separated company keys, e.g. netease,pinduoduo,didi")
    parser.add_argument("--refresh-mode", choices=("live", "cached"), default="live", help="Use live scraping or cached firecrawl inputs.")
    args = parser.parse_args()

    company_keys = parse_company_keys(args.companies)
    for key in company_keys:
        get_company_config(key)

    jobs = build_scrape_execution_plan(company_keys, refresh_mode=args.refresh_mode)
    docs = run_scrape_jobs(jobs, args.refresh_mode)
    for path in docs:
        print(path)


if __name__ == "__main__":
    main()
