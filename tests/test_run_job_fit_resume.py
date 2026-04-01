import tempfile
import unittest
from pathlib import Path
import subprocess
import sys


from scripts.run_job_fit_resume import (
    ShortlistRole,
    classify_resume_states,
    collect_generator_scripts,
    load_company_jobs,
    render_company_priority_section,
    select_top_roles,
)
from scripts.company_registry import get_company_config


REPO_ROOT = Path(__file__).resolve().parents[1]


class RunJobFitResumeTests(unittest.TestCase):
    def test_select_top_roles_prefers_profile_targets_and_skips_downranked_titles(self) -> None:
        jobs = [
            {"position_name": "Artificial Intelligence-后端研发实习生", "work_locations": "北京市"},
            {"position_name": "企业服务事业群（3）-后端研发实习生", "work_locations": "北京市"},
            {"position_name": "网约车平台公司-后端研发实习生", "work_locations": "北京市"},
            {"position_name": "网约车技术部-后端研发实习生", "work_locations": "北京市"},
        ]

        shortlist = select_top_roles("didi", jobs, top_n=3)

        self.assertEqual(
            [role.title for role in shortlist],
            [
                "网约车技术部-后端研发实习生",
                "网约车平台公司-后端研发实习生",
                "企业服务事业群（3）-后端研发实习生",
            ],
        )

    def test_load_company_jobs_filters_shared_combined_export_by_source(self) -> None:
        jobs = load_company_jobs(get_company_config("bytedance"))

        self.assertGreater(len(jobs), 100)
        self.assertTrue(all(job.get("source") == "bytedance" for job in jobs))

    def test_select_top_roles_matches_current_xiaohongshu_titles(self) -> None:
        jobs = [
            {
                "position_name": "【27届实习】Product Engineer-产品工程师（AI应用方向）-质效研发",
                "work_locations": "北京市，上海市，杭州市",
            },
            {
                "position_name": "【27届实习】Product Engineer-产品工程师（AI/全栈/应用研发方向）-商业技术",
                "work_locations": "北京市，上海市，杭州市",
            },
            {"position_name": "Java后端开发实习生", "work_locations": "北京市，上海市"},
        ]

        shortlist = select_top_roles("xiaohongshu", jobs, top_n=3)

        self.assertEqual(
            [role.title for role in shortlist],
            [
                "【27届实习】Product Engineer-产品工程师（AI应用方向）-质效研发",
                "【27届实习】Product Engineer-产品工程师（AI/全栈/应用研发方向）-商业技术",
                "Java后端开发实习生",
            ],
        )

    def test_collect_generator_scripts_deduplicates_missing_generators(self) -> None:
        roles = [
            ShortlistRole(
                company_key="oppo",
                company_display="OPPO",
                title="应用开发工程师（AI Agent方向）",
                location="深圳市",
                fit="very strong",
                reason="test",
                resume_alias="刘新宇-OPPO-应用开发工程师-AI-Agent方向",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
                fallback_alias=None,
            ),
            ShortlistRole(
                company_key="oppo",
                company_display="OPPO",
                title="应用开发工程师（AI Infra/AIOps方向）",
                location="深圳市",
                fit="very strong",
                reason="test",
                resume_alias="刘新宇-OPPO-应用开发工程师-AI-Infra-AIOps方向",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
                fallback_alias=None,
            ),
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            scripts = collect_generator_scripts(roles, export_dir=Path(tmp_dir))

        self.assertEqual(scripts, [Path("resumes/scripts/generate_unapplied_bigtech_resumes.py")])

    def test_classify_resume_states_distinguishes_existing_generated_and_reused(self) -> None:
        roles = [
            ShortlistRole(
                company_key="oppo",
                company_display="OPPO",
                title="应用开发工程师（AI Agent方向）",
                location="深圳市",
                fit="very strong",
                reason="test",
                resume_alias="existing",
                generator_script=None,
                fallback_alias=None,
            ),
            ShortlistRole(
                company_key="didi",
                company_display="Didi",
                title="网约车平台公司-后端研发实习生",
                location="北京市",
                fit="strong",
                reason="test",
                resume_alias="generated",
                generator_script=None,
                fallback_alias=None,
            ),
            ShortlistRole(
                company_key="honor",
                company_display="Honor",
                title="AI模型能力评测工程师",
                location="北京市",
                fit="medium",
                reason="test",
                resume_alias="missing",
                generator_script=None,
                fallback_alias="fallback",
            ),
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            export_dir = Path(tmp_dir)
            (export_dir / "existing.pdf").write_text("x", encoding="utf-8")
            (export_dir / "generated.pdf").write_text("x", encoding="utf-8")
            (export_dir / "fallback.pdf").write_text("x", encoding="utf-8")

            classified = classify_resume_states(roles, export_dir, newly_generated_aliases={"generated"})

        self.assertEqual([role.resume_state for role in classified], ["existing_pdf", "generated_now", "reused_template"])

    def test_render_company_priority_section_outputs_markdown_table(self) -> None:
        roles = [
            ShortlistRole(
                company_key="netease",
                company_display="NetEase（网易）",
                title="AI 应用开发实习生",
                location="北京市",
                fit="very strong",
                reason="主线最贴",
                resume_alias="刘新宇-网易-AI应用开发实习生",
                generator_script=None,
                fallback_alias=None,
                resume_state="existing_pdf",
            )
        ]

        section = render_company_priority_section("NetEase（网易）", roles)

        self.assertIn("### NetEase（网易）", section)
        self.assertIn("| 岗位 | 地点 | 适配度 | 说明 |", section)
        self.assertIn("AI 应用开发实习生", section)

    def test_render_company_priority_section_escapes_markdown_table_cells(self) -> None:
        roles = [
            ShortlistRole(
                company_key="alibaba",
                company_display="Alibaba（阿里巴巴）",
                title="AI应用研发工程师",
                location="北京 | 杭州 | 上海",
                fit="very strong",
                reason="覆盖 Prompt | Context | RAG",
                resume_alias="刘新宇-阿里巴巴-AI应用研发工程师",
                generator_script=None,
                fallback_alias=None,
            )
        ]

        section = render_company_priority_section("Alibaba（阿里巴巴）", roles)

        self.assertIn("北京 \\| 杭州 \\| 上海", section)
        self.assertIn("Prompt \\| Context \\| RAG", section)

    def test_script_can_be_invoked_directly_from_repo_root(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/run_job_fit_resume.py", "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--companies", result.stdout)


if __name__ == "__main__":
    unittest.main()
