import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class WorkflowSkillDocsTests(unittest.TestCase):
    def test_campus_job_scrape_skill_exists_with_script_entrypoint(self) -> None:
        content = (REPO_ROOT / ".claude/skills/campus-job-scrape/SKILL.md").read_text(encoding="utf-8")

        self.assertIn("name: campus-job-scrape", content)
        self.assertIn("`/campus-job-scrape`", content)
        self.assertIn("python scripts/run_company_scrape.py", content)
        self.assertIn("docs/temp/", content)
        self.assertIn("alibaba,antgroup,bytedance", content)

    def test_job_fit_skill_points_to_new_orchestrator(self) -> None:
        content = (REPO_ROOT / ".claude/skills/job-fit-to-resume/SKILL.md").read_text(encoding="utf-8")

        self.assertIn("python scripts/run_job_fit_resume.py", content)
        self.assertIn("docs/job-search-progress.md", content)
        self.assertIn("每家公司", content)

    def test_claude_md_documents_both_two_stage_workflow_skills(self) -> None:
        content = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")

        self.assertIn("/campus-job-scrape", content)
        self.assertIn("python scripts/run_company_scrape.py", content)
        self.assertIn("python scripts/run_job_fit_resume.py", content)
        self.assertIn("scrape_campus_jobs.py", content)


if __name__ == "__main__":
    unittest.main()
