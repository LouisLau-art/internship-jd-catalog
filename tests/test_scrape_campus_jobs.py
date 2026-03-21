import json
import tempfile
import unittest
from pathlib import Path

from scripts.scrape_campus_jobs import (
    build_ant_batch_id_list,
    build_alibaba_position_url,
    build_ant_position_url,
    build_export_source_entry,
    build_huawei_position_url,
    clamp_ant_page_size,
    collect_paginated,
    filter_jobs_by_category_name,
    is_huawei_wuhan_rd_job,
    load_maintained_exports,
    normalize_alibaba_job,
    normalize_ant_job,
    normalize_huawei_job,
    resolve_huawei_graduate_item,
)


class PaginationTests(unittest.TestCase):
    def test_collect_paginated_fetches_until_total_count(self) -> None:
        calls = []

        def fetch_page(page_index: int, page_size: int) -> dict:
            calls.append((page_index, page_size))
            if page_index == 1:
                return {"items": [{"id": 1}, {"id": 2}], "total": 3}
            if page_index == 2:
                return {"items": [{"id": 3}], "total": 3}
            raise AssertionError("unexpected page request")

        items, total = collect_paginated(fetch_page, page_size=2)

        self.assertEqual(total, 3)
        self.assertEqual([item["id"] for item in items], [1, 2, 3])
        self.assertEqual(calls, [(1, 2), (2, 2)])


class NormalizeTests(unittest.TestCase):
    def test_build_ant_batch_id_list_deduplicates_and_preserves_order(self) -> None:
        self.assertEqual(
            build_ant_batch_id_list("26022600074513", "25051200066269,26022600074513,,"),
            ["26022600074513", "25051200066269"],
        )

    def test_clamp_ant_page_size_caps_large_values(self) -> None:
        self.assertEqual(clamp_ant_page_size(25), 25)
        self.assertEqual(clamp_ant_page_size(100), 40)

    def test_normalize_ant_job_builds_flat_record(self) -> None:
        job = {
            "id": 26030308931579,
            "tid": "trace-token",
            "name": "【转正实习】算法工程师-搜索推荐",
            "batchId": 26022600074513,
            "batchName": "蚂蚁集团2027届转正实习",
            "categoryName": "技术类",
            "workLocations": ["北京", "上海", "杭州"],
            "interviewLocations": ["远程"],
            "featureTagList": ["Python", "推荐算法"],
            "requirement": "必须具备的：...",
            "description": "你是搜索推荐领域的专家",
            "publishTime": "2026-03-04T05:52:57.000+00:00",
            "graduationTime": {
                "from": "2026-10-31T16:00:00.000+00:00",
                "to": "2027-10-30T16:00:00.000+00:00",
            },
        }

        normalized = normalize_ant_job(job)

        self.assertEqual(normalized["source"], "antgroup")
        self.assertEqual(normalized["position_id"], 26030308931579)
        self.assertEqual(
            normalized["position_url"],
            build_ant_position_url(26030308931579, "trace-token"),
        )
        self.assertEqual(normalized["work_locations"], "北京 | 上海 | 杭州")
        self.assertEqual(normalized["feature_tags"], "Python | 推荐算法")
        self.assertEqual(normalized["graduation_from"], "2026-10-31T16:00:00.000+00:00")

    def test_normalize_alibaba_job_builds_flat_record(self) -> None:
        job = {
            "id": 199903480006,
            "name": "Agent Infra工程师",
            "batchId": 100000540002,
            "batchName": "阿里巴巴2027届实习生",
            "categoryName": "技术类",
            "workLocations": ["北京", "杭州"],
            "interviewLocations": ["远程"],
            "circleNames": ["阿里巴巴控股集团", "阿里云"],
            "circleCodeList": ["60000", "60001"],
            "channels": ["campus_group_official_site", "new_campus_shixiseng_website"],
            "requirement": "基础条件...",
            "description": "负责构建支撑AI Agent全生命周期的核心基础设施",
            "modifyTime": 1773922157000,
            "graduationTime": {"from": 1793491200000, "to": 1824940800000},
        }

        normalized = normalize_alibaba_job(job)

        self.assertEqual(normalized["source"], "alibaba")
        self.assertEqual(normalized["position_id"], 199903480006)
        self.assertEqual(
            normalized["position_url"],
            build_alibaba_position_url(199903480006),
        )
        self.assertEqual(normalized["circles"], "阿里巴巴控股集团 | 阿里云")
        self.assertEqual(normalized["circle_codes"], "60000 | 60001")
        self.assertEqual(normalized["channels"], "campus_group_official_site | new_campus_shixiseng_website")

    def test_filter_jobs_by_category_name_keeps_matching_rows(self) -> None:
        rows = [
            {"position_id": 1, "category_name": "技术类"},
            {"position_id": 2, "category_name": "产品类"},
            {"position_id": 3, "category_name": "技术类"},
        ]

        filtered = filter_jobs_by_category_name(rows, "技术类")

        self.assertEqual([row["position_id"] for row in filtered], [1, 3])
        self.assertEqual(filter_jobs_by_category_name(rows, ""), rows)

    def test_resolve_huawei_graduate_item_defaults_to_two(self) -> None:
        self.assertEqual(
            resolve_huawei_graduate_item({"jobType": "0", "graduateItem": None}, {"jobType": "0", "graduateItem": None}),
            "2",
        )
        self.assertEqual(
            resolve_huawei_graduate_item({"jobType": "2", "graduateItem": None}, {"jobType": "2", "graduateItem": None}),
            "0",
        )

    def test_normalize_huawei_job_expands_intent_level_record(self) -> None:
        job = {
            "jobId": 30860,
            "dataSource": 1,
            "jobname": "AI应用工程师",
            "jobFamClsCode": "JFC1",
            "positionReqCode": "PO2026031400004",
        }
        detail = {
            "jobId": 30860,
            "jobRequirementId": 95289,
            "jobname": "AI应用工程师",
            "jobArea": "中国/北京,中国/武汉",
            "jobRequire": "请您详见岗位意向中的岗位要求",
            "mainBusiness": "请您详见岗位意向中的岗位职责",
            "jobFamClsCode": "JFC1",
            "dataSource": 1,
            "effectiveDate": "2026-03-14T00:00:00.000+0800",
            "lastUpdateDate": "2026-03-18T16:21:22.000+0800",
        }
        intent = {
            "positionIntentionId": "11311",
            "positionIntention": "AI系统软件",
            "jobPlaceName": "中国\\广东\\深圳,中国\\湖北\\武汉",
            "deptName": "中央软件院,云计算BU",
            "jobResponsibilities": "1、参与系统设计；<br>2、参与性能调优；<br>",
            "jobDemand": "1、计算机相关专业；<br>2、熟练运用Python；<br>",
        }

        normalized = normalize_huawei_job(job, detail, intent)

        self.assertEqual(normalized["source"], "huawei")
        self.assertEqual(normalized["position_id"], "30860:11311")
        self.assertEqual(normalized["parent_position_id"], "30860")
        self.assertEqual(normalized["job_requirement_id"], 95289)
        self.assertEqual(normalized["position_intention_id"], "11311")
        self.assertEqual(normalized["position_intention_name"], "AI系统软件")
        self.assertEqual(normalized["position_name"], "AI应用工程师 - AI系统软件")
        self.assertEqual(
            normalized["position_url"],
            build_huawei_position_url(30860, 1),
        )
        self.assertEqual(normalized["work_locations"], "中国/广东/深圳 | 中国/湖北/武汉")
        self.assertEqual(normalized["departments"], "中央软件院 | 云计算BU")
        self.assertIn("参与系统设计", normalized["description"])
        self.assertIn("熟练运用Python", normalized["requirement"])

    def test_is_huawei_wuhan_rd_job_matches_intent_rows(self) -> None:
        row = {
            "source": "huawei",
            "family_code": "JFC1",
            "work_locations": "中国/广东/深圳 | 中国/湖北/武汉",
        }
        self.assertTrue(is_huawei_wuhan_rd_job(row))
        self.assertFalse(is_huawei_wuhan_rd_job({**row, "family_code": "JFC4"}))
        self.assertFalse(is_huawei_wuhan_rd_job({**row, "work_locations": "中国/广东/深圳"}))

    def test_build_export_source_entry_keeps_relevant_metadata(self) -> None:
        entry = build_export_source_entry(
            {
                "source": "bytedance",
                "company": "ByteDance",
                "project_id": "7194661644654577981",
                "project_name": "DailyIntern",
                "category_name": "后端",
                "total_count": 123,
            },
            "bytedance_positions_dailyintern_backend.json",
        )

        self.assertEqual(entry["source"], "bytedance")
        self.assertEqual(entry["file"], "bytedance_positions_dailyintern_backend.json")
        self.assertEqual(entry["project_name"], "DailyIntern")
        self.assertEqual(entry["total_count"], 123)

    def test_load_maintained_exports_reads_matching_json_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            (data_dir / "bytedance_positions_dailyintern_backend.json").write_text(
                json.dumps(
                    {
                        "source": "bytedance",
                        "company": "ByteDance",
                        "project_id": "7194661644654577981",
                        "project_name": "DailyIntern",
                        "category_name": "后端",
                        "total_count": 2,
                        "jobs": [
                            {"source": "bytedance", "position_id": "1"},
                            {"source": "bytedance", "position_id": "2"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (data_dir / "ignore_me.json").write_text(json.dumps({"jobs": [{"position_id": "3"}]}), encoding="utf-8")

            source_entries, jobs = load_maintained_exports(data_dir, "bytedance_positions_*.json")

        self.assertEqual(len(source_entries), 1)
        self.assertEqual(source_entries[0]["project_name"], "DailyIntern")
        self.assertEqual([job["position_id"] for job in jobs], ["1", "2"])


if __name__ == "__main__":
    unittest.main()
