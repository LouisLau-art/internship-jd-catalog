#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.audit_resume_coverage import (
    DEFAULT_EXPORT_DIR,
    DEFAULT_SCRIPTS_DIR,
    audit_targets,
    collect_resume_templates,
    extract_target_roles,
    sync_resume_sections,
)
from scripts.company_fit_profiles import CompanyFitProfile, TargetRoleProfile, get_fit_profile
from scripts.company_registry import (
    REPO_ROOT,
    CompanyConfig,
    count_company_jobs,
    filter_company_jobs,
    get_company_config,
    parse_company_keys,
)


DEFAULT_PROGRESS_DOC = REPO_ROOT / "docs" / "job-search-progress.md"
DEFAULT_SHORTLIST_DOC = REPO_ROOT / "docs" / "temp"
DEFAULT_PHOTO_CANDIDATES = (
    REPO_ROOT / "resumes" / "scripts" / "louis-profile-photo.png",
    Path("/home/louis/Downloads/Image_1755245899996.png"),
)


@dataclass(frozen=True)
class ShortlistRole:
    company_key: str
    company_display: str
    title: str
    location: str
    fit: str
    reason: str
    resume_alias: str
    generator_script: str | None
    fallback_alias: str | None
    resume_state: str | None = None


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", "", value.replace("（", "(").replace("）", ")").strip().lower())


def escape_markdown_table_cell(value: str) -> str:
    return value.replace("|", "\\|")


def match_target_job(jobs: list[dict[str, object]], target: TargetRoleProfile) -> dict[str, object] | None:
    target_name = normalize_text(target.title)
    for job in jobs:
        title = str(job.get("position_name", ""))
        if normalize_text(title) == target_name:
            return job
    return None


def build_shortlist_role(company: CompanyConfig, target: TargetRoleProfile, matched_job: dict[str, object]) -> ShortlistRole:
    return ShortlistRole(
        company_key=company.key,
        company_display=company.doc_heading,
        title=str(matched_job.get("position_name", target.title)),
        location=str(matched_job.get("work_locations", "")),
        fit=target.fit,
        reason=target.reason,
        resume_alias=target.resume_alias,
        generator_script=target.generator_script,
        fallback_alias=target.fallback_alias,
    )


def select_top_roles(company_key: str, jobs: list[dict[str, object]], top_n: int | None = None) -> list[ShortlistRole]:
    company = get_company_config(company_key)
    profile = get_fit_profile(company.fit_profile_key)
    limit = top_n or profile.default_top_n

    roles: list[ShortlistRole] = []
    used_titles: set[str] = set()

    for target in profile.targets:
        matched = match_target_job(jobs, target)
        if not matched:
            continue
        title = str(matched.get("position_name", ""))
        if title in used_titles:
            continue
        roles.append(build_shortlist_role(company, target, matched))
        used_titles.add(title)
        if len(roles) >= limit:
            break

    return roles


def collect_generator_scripts(roles: list[ShortlistRole], export_dir: Path) -> list[Path]:
    scripts: list[Path] = []
    seen: set[Path] = set()
    for role in roles:
        pdf_path = export_dir / f"{role.resume_alias}.pdf"
        if pdf_path.exists() or not role.generator_script:
            continue
        script_path = Path(role.generator_script)
        if script_path in seen:
            continue
        seen.add(script_path)
        scripts.append(script_path)
    return scripts


def classify_resume_states(
    roles: list[ShortlistRole],
    export_dir: Path,
    newly_generated_aliases: set[str] | None = None,
) -> list[ShortlistRole]:
    generated = newly_generated_aliases or set()
    classified: list[ShortlistRole] = []

    for role in roles:
        alias_pdf = export_dir / f"{role.resume_alias}.pdf"
        fallback_pdf = export_dir / f"{role.fallback_alias}.pdf" if role.fallback_alias else None

        if alias_pdf.exists() and role.resume_alias in generated:
            state = "generated_now"
        elif alias_pdf.exists():
            state = "existing_pdf"
        elif fallback_pdf and fallback_pdf.exists():
            state = "reused_template"
        else:
            state = "generation_failed"

        classified.append(replace(role, resume_state=state))

    return classified


def render_company_priority_section(company_heading: str, roles: list[ShortlistRole]) -> str:
    lines = [
        f"### {company_heading}",
        "",
        "| 岗位 | 地点 | 适配度 | 说明 |",
        "| --- | --- | --- | --- |",
    ]
    for role in roles:
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_markdown_table_cell(role.title),
                    escape_markdown_table_cell(role.location or "-"),
                    escape_markdown_table_cell(role.fit),
                    escape_markdown_table_cell(role.reason),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def build_shortlist_doc_path(company_keys: list[str], on_date: date | None = None) -> Path:
    current = on_date or date.today()
    slug = "job-fit-shortlist" if len(company_keys) > 2 else "-".join(company_keys) + "-shortlist"
    return DEFAULT_SHORTLIST_DOC / f"{current.isoformat()}-{slug}.md"


def render_shortlist_doc(roles_by_company: dict[str, list[ShortlistRole]], on_date: date | None = None) -> str:
    current = on_date or date.today()
    lines = [
        "# Job Fit Shortlist",
        "",
        f"更新时间：`{current.isoformat()}`",
        "",
    ]
    for company_heading, roles in roles_by_company.items():
        lines.append(render_company_priority_section(company_heading, roles))
        lines.append("")
        lines.append("| 对应简历 | 状态 |")
        lines.append("| --- | --- |")
        for role in roles:
            state = role.resume_state or "pending"
            lines.append(f"| {role.resume_alias}.pdf | {state} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def replace_company_priority_sections(content: str, company_sections: dict[str, str]) -> str:
    marker = "## 🔍 推荐次优岗位"
    if marker not in content:
        raise ValueError(f"无法定位文档段落: {marker}")

    updated = content
    for heading, section in company_sections.items():
        pattern = re.compile(rf"### {re.escape(heading)}\n\n.*?(?=\n### |\n## )", re.S)
        if pattern.search(updated):
            updated = pattern.sub(section + "\n", updated, count=1)
        else:
            updated = updated.replace(marker, section + "\n\n" + marker, 1)
    return updated


def refresh_scraped_company_table(content: str, companies: list[CompanyConfig], on_date: date | None = None) -> str:
    current = (on_date or date.today()).isoformat()
    lines = content.splitlines()
    start = None
    end = None
    for index, line in enumerate(lines):
        if line.strip() == "### 已爬取的公司":
            start = index + 1
            continue
        if start is not None and line.startswith("**总计原始导出："):
            end = index
            break
    if start is None or end is None:
        raise ValueError("无法定位已爬取公司表格")

    header = [
        "| 公司            | 爬取日期       | 数据来源                        | 岗位数量      |",
        "| ------------- | ---------- | --------------------------- | --------- |",
    ]

    rows: list[list[str]] = []
    for line in lines[start:end]:
        stripped = line.strip()
        if not stripped.startswith("|") or "公司" in stripped or set(stripped.replace("|", "").replace(" ", "")) == {"-"}:
            continue
        parts = [part.strip() for part in stripped.split("|")[1:-1]]
        if len(parts) == 4:
            rows.append(parts)

    row_map = {row[0]: row for row in rows}
    for company in companies:
        payload = json.loads(company.data_json.read_text(encoding="utf-8"))
        total_count = count_company_jobs(payload, company)
        row_map[company.display_name] = [company.display_name, current, company.source_label, str(total_count)]

    ordered_names = [row[0] for row in rows if row[0] in row_map]
    for company in companies:
        if company.display_name not in ordered_names:
            ordered_names.append(company.display_name)

    rebuilt = ["### 已爬取的公司", "", *header]
    total = 0
    for name in ordered_names:
        row = row_map[name]
        rebuilt.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")
        total += sum(int(value) for value in re.findall(r"\d+", row[3]))
    rebuilt.append("")
    rebuilt.append(f"**总计原始导出：约 {total} 行**")

    prefix = "\n".join(lines[: start - 1])
    suffix = "\n".join(lines[end + 1 :])
    return prefix + "\n" + "\n".join(rebuilt) + "\n\n" + suffix


def sync_progress_doc(progress_doc: Path, companies: list[CompanyConfig], roles_by_company: dict[str, list[ShortlistRole]], export_dir: Path) -> None:
    content = progress_doc.read_text(encoding="utf-8")
    content = refresh_scraped_company_table(content, companies)
    company_sections = {
        company_heading: render_company_priority_section(company_heading, roles)
        for company_heading, roles in roles_by_company.items()
    }
    content = replace_company_priority_sections(content, company_sections)

    targets = extract_target_roles(content)
    templates = collect_resume_templates(DEFAULT_SCRIPTS_DIR, export_dir)
    results = audit_targets(targets, templates)
    updated = sync_resume_sections(content, results)
    progress_doc.write_text(updated, encoding="utf-8")


def resolve_resume_env() -> dict[str, str]:
    env = os.environ.copy()
    if env.get("RESUME_PHOTO"):
        return env
    for candidate in DEFAULT_PHOTO_CANDIDATES:
        if candidate.exists():
            env["RESUME_PHOTO"] = str(candidate)
            break
    return env


def run_generator_scripts(scripts: list[Path]) -> set[str]:
    if not scripts:
        return set()
    env = resolve_resume_env()
    for script in scripts:
        subprocess.run([sys.executable, str(REPO_ROOT / script)], cwd=REPO_ROOT, env=env, check=True)
    return set()


def load_company_jobs(company: CompanyConfig) -> list[dict[str, object]]:
    payload = json.loads(company.data_json.read_text(encoding="utf-8"))
    return filter_company_jobs(payload, company)


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank high-fit roles per company, generate targeted resumes, and sync docs.")
    parser.add_argument("--companies", required=True, help="Comma-separated company keys, e.g. netease,pinduoduo,didi")
    parser.add_argument("--top-n-per-company", type=int, default=3, help="Maximum roles to keep per company.")
    parser.add_argument("--generate", dest="generate", action="store_true", default=True, help="Generate missing PDFs when generators exist.")
    parser.add_argument("--no-generate", dest="generate", action="store_false", help="Skip PDF generation and only render shortlist.")
    parser.add_argument("--sync-progress", dest="sync_progress", action="store_true", default=True, help="Sync docs/job-search-progress.md after shortlist generation.")
    parser.add_argument("--no-sync-progress", dest="sync_progress", action="store_false", help="Skip main dashboard updates.")
    parser.add_argument("--progress-doc", type=Path, default=DEFAULT_PROGRESS_DOC)
    parser.add_argument("--output-doc", type=Path)
    args = parser.parse_args()

    company_keys = parse_company_keys(args.companies)
    companies = [get_company_config(key) for key in company_keys]

    shortlist: list[ShortlistRole] = []
    for company in companies:
        shortlist.extend(select_top_roles(company.key, load_company_jobs(company), top_n=args.top_n_per_company))

    export_dir = DEFAULT_EXPORT_DIR
    before = {role.resume_alias for role in shortlist if (export_dir / f"{role.resume_alias}.pdf").exists()}
    scripts = collect_generator_scripts(shortlist, export_dir)
    if args.generate:
        run_generator_scripts(scripts)
    after = {role.resume_alias for role in shortlist if (export_dir / f"{role.resume_alias}.pdf").exists()}
    classified = classify_resume_states(shortlist, export_dir, newly_generated_aliases=after - before)

    roles_by_company: dict[str, list[ShortlistRole]] = {}
    for role in classified:
        roles_by_company.setdefault(role.company_display, []).append(role)

    output_doc = args.output_doc or build_shortlist_doc_path(company_keys)
    output_doc.parent.mkdir(parents=True, exist_ok=True)
    output_doc.write_text(render_shortlist_doc(roles_by_company), encoding="utf-8")

    if args.sync_progress:
        sync_progress_doc(args.progress_doc, companies, roles_by_company, export_dir)

    print(output_doc)


if __name__ == "__main__":
    main()
