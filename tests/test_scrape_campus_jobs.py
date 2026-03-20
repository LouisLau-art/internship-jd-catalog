import unittest

from scripts.scrape_campus_jobs import (
    build_alibaba_position_url,
    build_ant_position_url,
    clamp_ant_page_size,
    collect_paginated,
    normalize_alibaba_job,
    normalize_ant_job,
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


if __name__ == "__main__":
    unittest.main()
