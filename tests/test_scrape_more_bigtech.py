import unittest

from scripts.scrape_more_bigtech import (
    build_kuaishou_signature,
    canonicalize_kuaishou_params,
    is_kuaishou_tech_job,
    is_oppo_tech_job,
    normalize_honor_job,
    normalize_bilibili_job,
    normalize_kuaishou_job,
    normalize_oppo_job,
    parse_bilibili_job_count,
    split_bilibili_position_description,
)


class KuaishouTests(unittest.TestCase):
    def test_canonicalize_kuaishou_params_sorts_keys_and_array_values(self) -> None:
        canonical = canonicalize_kuaishou_params(
            {
                "pageSize": 10,
                "pageNum": 1,
                "tag": ["后端", "AI Agent"],
                "empty": "",
                "none": None,
            }
        )

        self.assertEqual(
            canonical,
            "pageNum=1&pageSize=10&tag=AI+Agent%2C%E5%90%8E%E7%AB%AF",
        )

    def test_build_kuaishou_signature_matches_expected_hmac(self) -> None:
        signature = build_kuaishou_signature(
            secret="652f962a-0575-4575-98d2-f04e2291bee2",
            timestamp="1700000000000",
            params={
                "pageSize": 10,
                "pageNum": 1,
                "tag": ["后端", "AI Agent"],
            },
        )

        self.assertEqual(
            signature,
            "fc840d878604ac37c31ff57e1c1647abe0487cb2bb15cf25a35e6cb486515883",
        )

    def test_is_kuaishou_tech_job_only_accepts_engineering_and_algorithm(self) -> None:
        self.assertTrue(is_kuaishou_tech_job({"positionCategoryCode": "J0011"}))
        self.assertTrue(is_kuaishou_tech_job({"positionCategoryCode": "J0012"}))
        self.assertFalse(is_kuaishou_tech_job({"positionCategoryCode": "J0005"}))
        self.assertFalse(
            is_kuaishou_tech_job(
                {
                    "positionCategoryCode": "J0012",
                    "name": "Aigc美学设计师-实习生",
                }
            )
        )

    def test_normalize_kuaishou_job_maps_category_and_locations(self) -> None:
        row = normalize_kuaishou_job(
            {
                "id": 25593,
                "name": "Java开发实习生-【主站】",
                "positionCategoryCode": "J0012",
                "workLocationsCode": ["Beijing", "Hangzhou"],
                "updateTime": "2026-03-26T19:55:37.000+08:00",
                "description": "负责服务端研发",
                "positionDemand": "熟悉 Java / Go",
                "departmentCode": "D13334",
            }
        )

        self.assertEqual(row["source"], "kuaishou")
        self.assertEqual(row["company"], "Kuaishou")
        self.assertEqual(row["position_id"], "25593")
        self.assertEqual(row["position_name"], "Java开发实习生-【主站】")
        self.assertEqual(row["category_name"], "工程类")
        self.assertEqual(row["work_locations"], "北京 | 杭州")
        self.assertEqual(row["batch_name"], "日常实习")
        self.assertEqual(row["departments"], "D13334")


class HonorTests(unittest.TestCase):
    def test_normalize_honor_job_uses_project_and_company_fields(self) -> None:
        row = normalize_honor_job(
            {
                "postId": "69b75d3bbe908548be3b46a3",
                "postCode": "HONOR009965",
                "postName": "机器人整机设计工程师",
                "postTypeName": "研发类",
                "workTypeStr": "实习",
                "workPlaceStr": "北京市、上海市",
                "publishDate": "2026-03-16 09:30:32",
                "company": "新产业孵化部",
                "projectName": "2026年实习生",
                "educationStr": "本科及以上",
            }
        )

        self.assertEqual(row["source"], "honor")
        self.assertEqual(row["company"], "Honor")
        self.assertEqual(row["position_id"], "69b75d3bbe908548be3b46a3")
        self.assertEqual(row["position_name"], "机器人整机设计工程师")
        self.assertEqual(row["batch_name"], "2026年实习生")
        self.assertEqual(row["category_name"], "研发类")
        self.assertEqual(row["work_locations"], "北京市 | 上海市")
        self.assertEqual(row["departments"], "新产业孵化部")
        self.assertEqual(row["feature_tags"], "本科及以上")


class OppoTests(unittest.TestCase):
    def test_is_oppo_tech_job_only_accepts_technical_categories(self) -> None:
        self.assertTrue(is_oppo_tech_job({"positionType": "Software"}))
        self.assertTrue(is_oppo_tech_job({"positionType": "AI/algorithm"}))
        self.assertFalse(is_oppo_tech_job({"positionType": "Products"}))

    def test_normalize_oppo_job_uses_project_type_and_cities(self) -> None:
        row = normalize_oppo_job(
            {
                "idRecruitPosition": 1642,
                "projectName": "2027届寻梦实习招聘",
                "recruitmentTypeName": "实习生",
                "positionType": "Software",
                "positionTypeName": "软件类",
                "positionName": "后端工程师",
                "positionDesc": "负责服务端研发",
                "positionRequire": "熟悉 Java / Go",
                "workCityName": "成都市,深圳市,南京市",
                "releaseTime": "2026-03-06",
                "specialRecruitment": "",
            }
        )

        self.assertEqual(row["source"], "oppo")
        self.assertEqual(row["company"], "OPPO")
        self.assertEqual(row["position_id"], "1642")
        self.assertEqual(row["position_name"], "后端工程师")
        self.assertEqual(row["batch_name"], "2027届寻梦实习招聘")
        self.assertEqual(row["category_name"], "软件类")
        self.assertEqual(row["work_locations"], "成都市 | 深圳市 | 南京市")
        self.assertEqual(row["publish_time"], "2026-03-06")


class BilibiliTests(unittest.TestCase):
    def test_parse_bilibili_job_count_handles_zero_and_non_zero(self) -> None:
        self.assertEqual(parse_bilibili_job_count("### 职位列表 （0）"), 0)
        self.assertEqual(parse_bilibili_job_count("### 职位列表 （23）"), 23)

    def test_split_bilibili_position_description_handles_html_markers(self) -> None:
        description, requirement = split_bilibili_position_description(
            "<strong>工作职责:</strong>\n负责 Agent 工作流开发\n<strong>工作要求:</strong>\n熟悉 Python / Go"
        )

        self.assertEqual(description, "负责 Agent 工作流开发")
        self.assertEqual(requirement, "熟悉 Python / Go")

    def test_normalize_bilibili_job_maps_core_fields(self) -> None:
        row = normalize_bilibili_job(
            {
                "id": 27295,
                "campusProjectId": 53,
                "hotRecruit": 1,
                "positionDescription": (
                    "工作职责:\n参与视频 CDN 点直播流量调度研发\n"
                    "工作要求:\n熟悉数据结构、操作系统、网络"
                ),
                "positionName": "视频CDN研发实习生【2027届】",
                "positionTypeName": "实习",
                "postCodeName": "技术类",
                "pushTime": "2026-03-19 13:24:01",
                "recruitType": 1,
                "workLocation": "上海/北京",
            }
        )

        self.assertEqual(row["source"], "bilibili")
        self.assertEqual(row["company"], "Bilibili")
        self.assertEqual(row["position_id"], "27295")
        self.assertEqual(row["position_name"], "视频CDN研发实习生【2027届】")
        self.assertEqual(row["position_url"], "https://jobs.bilibili.com/campus/positions/27295")
        self.assertEqual(row["batch_name"], "实习生招聘")
        self.assertEqual(row["category_name"], "技术类")
        self.assertEqual(row["work_locations"], "上海 | 北京")
        self.assertEqual(row["publish_time"], "2026-03-19 13:24:01")
        self.assertEqual(row["description"], "参与视频 CDN 点直播流量调度研发")
        self.assertEqual(row["requirement"], "熟悉数据结构、操作系统、网络")
        self.assertEqual(row["feature_tags"], "热门职位 | campusProjectId=53")


if __name__ == "__main__":
    unittest.main()
