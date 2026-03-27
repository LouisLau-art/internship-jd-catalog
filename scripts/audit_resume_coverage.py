#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOC = REPO_ROOT / "docs" / "job-search-progress.md"
DEFAULT_SCRIPTS_DIR = REPO_ROOT / "resumes" / "scripts"
DEFAULT_EXPORT_DIR = REPO_ROOT / "resumes" / "sources"
GENERATOR_GLOB = "generate*.py"

COMPANY_ALIASES = {
    "阿里巴巴": {"alibaba", "阿里巴巴"},
    "蚂蚁": {"ant", "ant group", "antgroup", "蚂蚁"},
    "字节跳动": {"bytedance", "字节跳动"},
    "华为": {"huawei", "华为"},
    "京东": {"jd", "京东"},
    "美团": {"meituan", "美团"},
    "网易互娱": {"netease", "netease games", "网易互娱", "网易游戏"},
    "OceanBase": {"oceanbase", "奥星贝斯"},
    "拼多多": {"pinduoduo", "拼多多"},
    "腾讯": {"tencent", "腾讯"},
    "小红书": {"xiaohongshu", "xhs", "小红书"},
    "小米": {"xiaomi", "小米"},
    "滴滴": {"didi", "滴滴"},
}

ROLE_KEYWORDS = (
    "ai",
    "agent",
    "coding",
    "backend",
    "java",
    "后端",
    "服务端",
    "开发",
    "研发",
    "工程师",
    "平台",
    "应用",
    "infra",
    "基建",
    "搜索",
    "金融",
    "知识工程",
    "训推",
    "oceanbase",
    "native",
)

DIRECT_ROLE_KEYWORDS = (
    "ai",
    "agent",
    "coding",
    "backend",
    "java",
    "后端",
    "服务端",
    "平台",
    "应用",
    "infra",
    "基建",
    "搜索",
    "金融",
    "知识工程",
    "训推",
    "oceanbase",
    "native",
    "产品",
    "生态",
)


@dataclass(frozen=True)
class ResumeTemplate:
    script_name: str
    alias: str
    company: str
    role: str
    pdf_exists: bool


@dataclass(frozen=True)
class TargetRole:
    company: str
    role: str
    source: str


@dataclass(frozen=True)
class CoverageResult:
    company: str
    role: str
    source: str
    status: str
    matched_alias: str | None
    matched_script: str | None
    note: str


def normalize_text(value: str) -> str:
    text = value.lower()
    text = text.replace("（", "(").replace("）", ")")
    text = text.replace("—", "-").replace("–", "-")
    text = re.sub(r"^[a-z0-9\s\-/]+(?=[\u4e00-\u9fff])", "", text)
    text = re.sub(r"[\s*_`·.,:;!?\-_/()（）【】\[\]]+", "", text)
    return text


def normalize_company(value: str) -> str:
    cleaned = normalize_text(value)
    for canonical, aliases in COMPANY_ALIASES.items():
        if cleaned in {normalize_text(alias) for alias in aliases}:
            return canonical
    return value.strip()


def normalize_role(value: str) -> str:
    return normalize_text(value)


def parse_alias(alias: str) -> tuple[str, str]:
    body = alias
    if body.startswith("刘新宇-"):
        body = body[len("刘新宇-") :]
    company, _, role = body.partition("-")
    if company == "蚂蚁" and role.startswith("OceanBase-"):
        return "OceanBase", role
    return company, role


def load_resume_registry(script_path: Path) -> list[dict[str, object]]:
    module = ast.parse(script_path.read_text(encoding="utf-8"))
    fallback: list[dict[str, object]] = []
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            if target.id not in {"AUDIT_RESUMES", "RESUMES"}:
                continue
            try:
                value = ast.literal_eval(node.value)
            except (SyntaxError, ValueError):
                continue
            if not isinstance(value, list):
                continue
            items = [item for item in value if isinstance(item, dict)]
            if target.id == "AUDIT_RESUMES":
                return items
            fallback = items
    return fallback


def collect_resume_templates(scripts_dir: Path, export_dir: Path) -> list[ResumeTemplate]:
    templates: list[ResumeTemplate] = []
    for script_path in sorted(scripts_dir.glob(GENERATOR_GLOB)):
        for item in load_resume_registry(script_path):
            alias = str(item.get("alias", "")).strip()
            role = str(item.get("role", "")).strip()
            if not alias or not role:
                continue
            company, inferred_role = parse_alias(alias)
            effective_role = role or inferred_role
            pdf_exists = (export_dir / f"{alias}.pdf").exists()
            templates.append(
                ResumeTemplate(
                    script_name=script_path.name,
                    alias=alias,
                    company=normalize_company(company),
                    role=effective_role,
                    pdf_exists=pdf_exists,
                )
            )
    return templates


def strip_markdown(value: str) -> str:
    return value.replace("**", "").strip()


def parse_markdown_table(lines: list[str], start_index: int) -> tuple[list[list[str]], int]:
    rows: list[list[str]] = []
    index = start_index
    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()
        if not stripped:
            if rows:
                break
            index += 1
            continue
        if not stripped.startswith("|"):
            if rows:
                break
            index += 1
            continue
        columns = [strip_markdown(part) for part in stripped.split("|")[1:-1]]
        if not columns or all(set(col) <= {"-"} for col in columns):
            index += 1
            continue
        if columns[0] == "公司" or columns[0] == "岗位" or columns[0] == "目标公司":
            index += 1
            continue
        rows.append(columns)
        index += 1
    return rows, index


def extract_applied_targets(md_content: str) -> list[TargetRole]:
    lines = md_content.splitlines()
    targets: list[TargetRole] = []
    in_section = False
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if line.startswith("## ✅ 已投递岗位"):
            in_section = True
            index += 1
            continue
        if in_section and line.startswith("## ") and not line.startswith("## ✅ 已投递岗位"):
            break
        if in_section and line.startswith("|"):
            rows, index = parse_markdown_table(lines, index)
            for row in rows:
                if len(row) < 6:
                    continue
                company, role, _, _, _, note = row[:6]
                if company == "-" or role == "-":
                    continue
                if "匹配度一般" in note:
                    continue
                targets.append(TargetRole(company=company, role=role, source="applied"))
            continue
        index += 1
    return targets


def extract_recommended_targets(md_content: str) -> list[TargetRole]:
    lines = md_content.splitlines()
    targets: list[TargetRole] = []
    current_company: str | None = None
    section: str | None = None
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        if line.startswith("## 🎯 推荐优先岗位"):
            section = "priority"
            index += 1
            continue
        if line.startswith("## 🔍 推荐次优岗位"):
            section = "secondary"
            current_company = None
            index += 1
            continue
        if section and line.startswith("## ") and not (
            line.startswith("## 🎯 推荐优先岗位") or line.startswith("## 🔍 推荐次优岗位")
        ):
            break
        if section == "priority" and line.startswith("### "):
            current_company = line[4:].split("（", 1)[0].strip()
            index += 1
            continue
        if section and line.startswith("|"):
            rows, index = parse_markdown_table(lines, index)
            for row in rows:
                if section == "priority":
                    if current_company is None or len(row) < 3:
                        continue
                    role, _, fit = row[:3]
                    if role == "-" or fit == "-":
                        continue
                    targets.append(TargetRole(company=current_company, role=role, source=section))
                elif section == "secondary":
                    if len(row) < 4:
                        continue
                    company, role, _, fit = row[:4]
                    if company == "-" or role == "-" or fit == "-":
                        continue
                    targets.append(TargetRole(company=company, role=role, source=section))
            continue
        index += 1

    return targets


def extract_target_roles(md_content: str) -> list[TargetRole]:
    seen: set[tuple[str, str]] = set()
    ordered: list[TargetRole] = []
    for target in [*extract_applied_targets(md_content), *extract_recommended_targets(md_content)]:
        key = (normalize_company(target.company), normalize_role(target.role))
        if key in seen:
            continue
        seen.add(key)
        ordered.append(target)
    return ordered


def role_keyword_overlap(left: str, right: str) -> int:
    return sum(1 for keyword in ROLE_KEYWORDS if keyword in left and keyword in right)


def direct_keyword_overlap(left: str, right: str) -> int:
    return sum(1 for keyword in DIRECT_ROLE_KEYWORDS if keyword in left and keyword in right)


def score_role_match(target_role: str, template_role: str) -> float:
    target_norm = normalize_role(target_role)
    template_norm = normalize_role(template_role)
    if not target_norm or not template_norm:
        return 0.0
    if target_norm == template_norm:
        return 1.0

    score = SequenceMatcher(None, target_norm, template_norm).ratio()
    if target_norm in template_norm or template_norm in target_norm:
        score += 0.25
    score += min(role_keyword_overlap(target_norm, template_norm) * 0.03, 0.15)
    return min(score, 1.0)


def is_direct_match(target_role: str, template_role: str) -> bool:
    target_norm = normalize_role(target_role)
    template_norm = normalize_role(template_role)
    if target_norm == template_norm:
        return True
    if target_norm in template_norm or template_norm in target_norm:
        return True
    score = score_role_match(target_role, template_role)
    if direct_keyword_overlap(target_norm, template_norm) >= 1 and score >= 0.7:
        return True
    return score >= 0.82


def status_note(result_status: str, alias: str | None, script_name: str | None) -> str:
    if result_status == "generated":
        return "已存在定向 PDF"
    if result_status == "generator_ready":
        return f"可直接运行 `python resumes/scripts/{script_name}` 生成"
    if result_status == "reusable":
        return f"可复用现有简历 `{alias}.pdf`，再按岗位微调"
    return "暂无对应模板，建议新增定向简历"


def audit_targets(targets: list[TargetRole], templates: list[ResumeTemplate]) -> list[CoverageResult]:
    results: list[CoverageResult] = []
    for target in targets:
        normalized_company = normalize_company(target.company)
        company_templates = [
            template for template in templates if normalize_company(template.company) == normalized_company
        ]
        if not company_templates:
            results.append(
                CoverageResult(
                    company=target.company,
                    role=target.role,
                    source=target.source,
                    status="missing",
                    matched_alias=None,
                    matched_script=None,
                    note=status_note("missing", None, None),
                )
            )
            continue

        best_template = max(company_templates, key=lambda template: score_role_match(target.role, template.role))
        direct_match = is_direct_match(target.role, best_template.role)

        if direct_match and best_template.pdf_exists:
            status = "generated"
        elif direct_match and not best_template.pdf_exists:
            status = "generator_ready"
        elif best_template.pdf_exists:
            status = "reusable"
        else:
            status = "generator_ready"

        results.append(
            CoverageResult(
                company=target.company,
                role=target.role,
                source=target.source,
                status=status,
                matched_alias=best_template.alias,
                matched_script=best_template.script_name,
                note=status_note(status, best_template.alias, best_template.script_name),
            )
        )

    return results


def build_generated_table(results: list[CoverageResult]) -> str:
    lines = [
        "| 目标公司 | 目标岗位 | 对应简历 | 状态 |",
        "| --- | --- | --- | --- |",
    ]
    generated = [result for result in results if result.status == "generated"]
    if not generated:
        lines.append("| - | - | - | 暂无 |")
        return "\n".join(lines)

    for result in generated:
        lines.append(
            f"| {result.company} | {result.role} | {result.matched_alias}.pdf | 已生成 |"
        )
    return "\n".join(lines)


def build_pending_table(results: list[CoverageResult]) -> str:
    lines = [
        "| 目标公司 | 目标岗位 | 当前建议 | 状态 |",
        "| --- | --- | --- | --- |",
    ]
    order = {"generator_ready": 0, "reusable": 1, "missing": 2}
    pending = [result for result in results if result.status != "generated"]
    pending.sort(key=lambda result: (order.get(result.status, 9), result.company, result.role))
    if not pending:
        lines.append("| - | - | - | 暂无缺口 |")
        return "\n".join(lines)

    for result in pending:
        if result.status == "generator_ready":
            suggestion = f"可直接运行脚本生成（{result.matched_script}）"
        elif result.status == "reusable":
            suggestion = f"可复用现有简历（{result.matched_alias}.pdf）"
        else:
            suggestion = "需新建定向简历"
        lines.append(
            f"| {result.company} | {result.role} | {suggestion} | {result.status} |"
        )
    return "\n".join(lines)


def replace_section(content: str, heading: str, body: str, next_heading_pattern: str) -> str:
    pattern = re.compile(
        rf"({re.escape(heading)}\n\n).*?(?=\n{next_heading_pattern})",
        re.S,
    )
    replacement = rf"\1{body}\n"
    updated, count = pattern.subn(replacement, content, count=1)
    if count != 1:
        raise ValueError(f"无法定位文档段落: {heading}")
    return updated


def sync_resume_sections(md_content: str, results: list[CoverageResult]) -> str:
    generated_table = build_generated_table(results)
    pending_table = build_pending_table(results)
    updated = replace_section(md_content, "### 已生成的定向简历", generated_table, r"### 待生成简历")
    updated = replace_section(updated, "### 待生成简历", pending_table, r"## ")
    return updated


def print_summary(results: list[CoverageResult]) -> None:
    counts = {
        "generated": 0,
        "generator_ready": 0,
        "reusable": 0,
        "missing": 0,
    }
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1

    print("Resume coverage audit:")
    for key in ("generated", "generator_ready", "reusable", "missing"):
        print(f"  - {key}: {counts[key]}")

    interesting = [result for result in results if result.status != "generated"][:8]
    if interesting:
        print("\nOpen gaps:")
        for result in interesting:
            print(f"  - {result.company} / {result.role}: {result.note}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit suitable-role resume coverage and optionally sync the dashboard.")
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC, help="Path to docs/job-search-progress.md")
    parser.add_argument("--scripts-dir", type=Path, default=DEFAULT_SCRIPTS_DIR, help="Path to resume generator scripts")
    parser.add_argument("--sources-dir", type=Path, default=DEFAULT_EXPORT_DIR, help="Path to generated resume assets")
    parser.add_argument("--sync-doc", type=Path, help="Rewrite the target Markdown document with refreshed resume coverage sections")
    args = parser.parse_args()

    doc_content = args.doc.read_text(encoding="utf-8")
    targets = extract_target_roles(doc_content)
    templates = collect_resume_templates(args.scripts_dir, args.sources_dir)
    results = audit_targets(targets, templates)
    print_summary(results)

    if args.sync_doc:
        updated = sync_resume_sections(doc_content, results)
        args.sync_doc.write_text(updated, encoding="utf-8")
        print(f"\nSynced resume sections in {args.sync_doc}")


if __name__ == "__main__":
    main()
