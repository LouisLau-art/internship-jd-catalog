import unittest
from datetime import date
from pathlib import Path
import subprocess
import sys


from scripts.run_company_scrape import build_scrape_execution_plan, build_status_doc_path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RunCompanyScrapeTests(unittest.TestCase):
    def test_build_scrape_execution_plan_groups_companies_by_family(self) -> None:
        jobs = build_scrape_execution_plan(["netease", "didi", "oppo"], refresh_mode="live")

        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0].group_key, "extra_bigtech")
        self.assertEqual(jobs[0].script_path.name, "scrape_extra_bigtech.py")
        self.assertEqual([company.key for company in jobs[0].companies], ["netease", "didi"])
        self.assertEqual(jobs[1].group_key, "more_bigtech")
        self.assertEqual(jobs[1].script_path.name, "scrape_more_bigtech.py")
        self.assertEqual([company.key for company in jobs[1].companies], ["oppo"])

    def test_cached_refresh_adds_cached_firecrawl_flag(self) -> None:
        jobs = build_scrape_execution_plan(["oppo"], refresh_mode="cached")

        self.assertIn("--use-cached-firecrawl", jobs[0].command)

    def test_campus_core_group_uses_campus_scraper_without_cached_firecrawl_flag(self) -> None:
        jobs = build_scrape_execution_plan(["bytedance", "huawei"], refresh_mode="cached")

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].group_key, "campus_core")
        self.assertEqual(jobs[0].script_path.name, "scrape_campus_jobs.py")
        self.assertEqual([company.key for company in jobs[0].companies], ["bytedance", "huawei"])
        self.assertNotIn("--use-cached-firecrawl", jobs[0].command)

    def test_status_doc_path_uses_group_name_and_date(self) -> None:
        path = build_status_doc_path("more_bigtech", on_date=date(2026, 3, 28))

        self.assertEqual(path.name, "2026-03-28-more-bigtech-crawl-status.md")

    def test_script_can_be_invoked_directly_from_repo_root(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/run_company_scrape.py", "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--companies", result.stdout)


if __name__ == "__main__":
    unittest.main()
