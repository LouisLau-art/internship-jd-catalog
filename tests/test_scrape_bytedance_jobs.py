import argparse
import unittest

from scripts.scrape_bytedance_jobs import normalize_job


class NormalizeByteDanceJobTests(unittest.TestCase):
    def test_normalize_job_builds_flat_record(self) -> None:
        args = argparse.Namespace(
            source="bytedance",
            company="ByteDance",
            project_id="7194661644654577981",
            project_name="DailyIntern",
            category_name="后端",
        )
        job = {
            "id": "7610000000000000001",
            "title": "后端开发实习生-大模型平台",
            "code": "A10001",
            "job_subject": {
                "id": "7194661644654577981",
                "name": {"zh_cn": "DailyIntern"},
            },
            "job_category": {"name": "后端"},
            "city_list": [{"name": "北京"}, {"name": "杭州"}],
            "department_id": "D1000",
            "job_hot_flag": True,
            "process_type": 2,
            "storefront_mode": 1,
            "publish_time": 1760000000000,
            "requirement": "熟悉 Python 或 Go",
            "description": "参与平台开发",
        }

        row = normalize_job(job, args)

        self.assertEqual(row["source"], "bytedance")
        self.assertEqual(row["position_id"], "7610000000000000001")
        self.assertEqual(row["position_name"], "后端开发实习生-大模型平台")
        self.assertEqual(row["batch_name"], "DailyIntern")
        self.assertEqual(row["category_name"], "后端")
        self.assertEqual(row["work_locations"], "北京 | 杭州")
        self.assertIn("hot", row["feature_tags"])
        self.assertIn("process_type:2", row["feature_tags"])
        self.assertEqual(row["channels"], "campus")


if __name__ == "__main__":
    unittest.main()
