import os
import sys
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts import audit_resume_coverage as coverage


def write_script(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_collect_resume_templates_detects_generated_and_generator_ready(tmp_path: Path):
    scripts_dir = tmp_path / "scripts"
    export_dir = tmp_path / "sources"
    scripts_dir.mkdir()
    export_dir.mkdir()
    write_script(
        scripts_dir / "generate_sample_resumes.py",
        """RESUMES = [
    {"alias": "刘新宇-京东-AI创新应用-人力资源方向", "role": "AI创新应用（人力资源方向）"},
    {"alias": "刘新宇-小红书-产品工程师-AI应用方向-质效研发", "role": "产品工程师-AI应用方向-质效研发"},
    {"alias": "刘新宇-网易互娱-Agent工程师", "role": "Agent工程师"},
]
""",
    )
    (export_dir / "刘新宇-京东-AI创新应用-人力资源方向.pdf").write_text("pdf", encoding="utf-8")
    (export_dir / "刘新宇-小红书-产品工程师-AI应用方向-质效研发.pdf").write_text("pdf", encoding="utf-8")

    templates = coverage.collect_resume_templates(scripts_dir, export_dir)
    by_alias = {template.alias: template for template in templates}

    assert by_alias["刘新宇-京东-AI创新应用-人力资源方向"].pdf_exists is True
    assert by_alias["刘新宇-小红书-产品工程师-AI应用方向-质效研发"].pdf_exists is True
    assert by_alias["刘新宇-网易互娱-Agent工程师"].pdf_exists is False


def test_audit_targets_distinguishes_generated_reusable_and_generator_ready():
    templates = [
        coverage.ResumeTemplate(
            script_name="generate_jd_resumes.py",
            alias="刘新宇-京东-AI创新应用-人力资源方向",
            company="京东",
            role="AI创新应用（人力资源方向）",
            pdf_exists=True,
        ),
        coverage.ResumeTemplate(
            script_name="generate_antgroup_resumes.py",
            alias="刘新宇-蚂蚁-AI工程师-应用方向",
            company="蚂蚁",
            role="AI工程师（应用方向）",
            pdf_exists=True,
        ),
        coverage.ResumeTemplate(
            script_name="generate_antgroup_resumes.py",
            alias="刘新宇-蚂蚁-应用研发工程师-JAVA",
            company="蚂蚁",
            role="应用研发工程师-JAVA",
            pdf_exists=True,
        ),
        coverage.ResumeTemplate(
            script_name="generate_netease_resumes.py",
            alias="刘新宇-网易互娱-Agent工程师",
            company="网易互娱",
            role="Agent工程师",
            pdf_exists=False,
        ),
    ]
    targets = [
        coverage.TargetRole(company="JD", role="AI创新应用（人力资源方向）", source="priority"),
        coverage.TargetRole(company="Ant Group", role="研发工程师（金融AI）", source="priority"),
        coverage.TargetRole(company="NetEase Games", role="Agent Engineer（AI Native）", source="priority"),
    ]

    results = coverage.audit_targets(targets, templates)
    status_map = {(result.company, result.role): result.status for result in results}

    assert status_map[("JD", "AI创新应用（人力资源方向）")] == "generated"
    assert status_map[("Ant Group", "研发工程师（金融AI）")] == "reusable"
    assert status_map[("NetEase Games", "Agent Engineer（AI Native）")] == "generator_ready"


def test_collect_resume_templates_supports_audit_resumes_literal(tmp_path: Path):
    scripts_dir = tmp_path / "scripts"
    export_dir = tmp_path / "sources"
    scripts_dir.mkdir()
    export_dir.mkdir()
    write_script(
        scripts_dir / "generate_gap_resumes.py",
        """RESUMES = [clone_resume("ignored")]
AUDIT_RESUMES = [
    {"alias": "刘新宇-网易游戏-Agent-Engineer-AI-Native", "role": "Agent Engineer（AI Native）"},
]
""",
    )

    templates = coverage.collect_resume_templates(scripts_dir, export_dir)
    by_alias = {template.alias: template for template in templates}

    assert by_alias["刘新宇-网易游戏-Agent-Engineer-AI-Native"].role == "Agent Engineer（AI Native）"


def test_sync_resume_sections_rewrites_generated_and_pending_tables():
    doc = """# 求职进度记事本

### 已生成的定向简历

| 目标公司 | 简历文件 | 状态 |
| --- | --- | --- |
| OldCo | old.pdf | 已生成 |

### 待生成简历

| 目标公司 | 岗位 | 优先级 |
| --- | --- | --- |
| OldGap | old role | 高 |

## 🎯 项目证据库
"""
    results = [
        coverage.CoverageResult(
            company="JD",
            role="AI创新应用（人力资源方向）",
            source="priority",
            status="generated",
            matched_alias="刘新宇-京东-AI创新应用-人力资源方向",
            matched_script="generate_jd_resumes.py",
            note="已存在定向 PDF",
        ),
        coverage.CoverageResult(
            company="Ant Group",
            role="研发工程师（金融AI）",
            source="priority",
            status="reusable",
            matched_alias="刘新宇-蚂蚁-AI工程师-应用方向",
            matched_script="generate_antgroup_resumes.py",
            note="建议先复用相近岗位简历",
        ),
        coverage.CoverageResult(
            company="NetEase Games",
            role="Agent Engineer（AI Native）",
            source="priority",
            status="generator_ready",
            matched_alias="刘新宇-网易互娱-Agent工程师",
            matched_script="generate_netease_resumes.py",
            note="脚本已存在，但成品尚未导出",
        ),
    ]

    updated = coverage.sync_resume_sections(doc, results)

    assert "OldCo" not in updated
    assert "OldGap" not in updated
    assert "刘新宇-京东-AI创新应用-人力资源方向.pdf" in updated
    assert "研发工程师（金融AI）" in updated
    assert "可复用现有简历" in updated
    assert "可直接运行脚本生成" in updated
