import unittest

from scripts.scrape_extra_bigtech import (
    normalize_netease_job,
    normalize_xiaomi_job,
    parse_didi_markdown,
    parse_pdd_markdown,
)


PDD_SAMPLE = """
职位标签

- 紧缺

大模型算法实习生
紧缺
技术专场
技术
上海
2026-03-03

服务端研发实习生
技术专场
技术
上海
2026-03-03

共6个岗位
"""


DIDI_SAMPLE = r"""
[急Artificial Intelligence-后端研发实习生\
\
实习生招聘项目实习技术类\
\
北京市\
\
发布时间：2026-03-19](https://app.mokahr.com/apply/didiglobal/6222#/job/d776b384-456e-48b8-b3b0-03f43cd4a326)

[急技术/测试开发实习生\
\
实习生招聘项目实习技术类\
\
北京市\
\
发布时间：2026-03-13](https://app.mokahr.com/apply/didiglobal/6222#/job/732b0737-fcc3-4cbf-b3ac-c07adfcb24ee)
"""


DIDI_WITH_HEADER_NOISE = r"""
[![](https://public-cdn.mokahr.com/e7f054a1-317c-429d-b163-cd0570d6680c.png)](https://www.didiglobal.com/)

- [在招实习生职位](https://app.mokahr.com/apply/didiglobal/6222#/?anchorName=3046959645&sourceToken=)

[急Artificial Intelligence-后端研发实习生\
\
实习生招聘项目实习技术类\
\
北京市\
\
发布时间：2026-03-19](https://app.mokahr.com/apply/didiglobal/6222#/job/d776b384-456e-48b8-b3b0-03f43cd4a326)
"""


class ParseMarkdownTests(unittest.TestCase):
    def test_parse_pdd_markdown_extracts_titles_and_hot_flag(self) -> None:
        jobs = parse_pdd_markdown(PDD_SAMPLE)

        self.assertEqual([job["title"] for job in jobs], ["大模型算法实习生", "服务端研发实习生"])
        self.assertEqual(jobs[0]["location"], "上海")
        self.assertEqual(jobs[0]["category"], "技术")
        self.assertEqual(jobs[0]["feature_tags"], ["紧缺"])
        self.assertEqual(jobs[1]["feature_tags"], [])

    def test_parse_didi_markdown_extracts_linked_jobs(self) -> None:
        jobs = parse_didi_markdown(DIDI_SAMPLE)

        self.assertEqual(
            [job["title"] for job in jobs],
            ["Artificial Intelligence-后端研发实习生", "技术/测试开发实习生"],
        )
        self.assertEqual(jobs[0]["batch_name"], "实习生招聘项目实习技术类")
        self.assertEqual(jobs[0]["location"], "北京市")
        self.assertEqual(jobs[0]["publish_date"], "2026-03-19")
        self.assertTrue(jobs[0]["position_url"].endswith("d776b384-456e-48b8-b3b0-03f43cd4a326"))

    def test_parse_didi_markdown_ignores_header_links(self) -> None:
        jobs = parse_didi_markdown(DIDI_WITH_HEADER_NOISE)

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["title"], "Artificial Intelligence-后端研发实习生")


class NormalizeTests(unittest.TestCase):
    def test_normalize_netease_job_uses_detail_page_and_category(self) -> None:
        row = normalize_netease_job(
            {
                "id": 75210,
                "name": "Agent工程师",
                "firstPostTypeName": "人工智能",
                "description": "负责 Agent 方案设计",
                "requirement": "熟悉大模型与工作流",
                "workPlaceNameList": ["广州市", "杭州市"],
                "productName": "网易游戏",
                "updateTime": "2026-03-25 10:00:00",
            }
        )

        self.assertEqual(row["source"], "netease")
        self.assertEqual(row["position_id"], "75210")
        self.assertEqual(row["position_name"], "Agent工程师")
        self.assertEqual(row["category_name"], "人工智能")
        self.assertEqual(row["work_locations"], "广州市 | 杭州市")
        self.assertEqual(row["position_url"], "https://hr.163.com/job-detail.html?postId=75210")

    def test_normalize_xiaomi_job_uses_function_city_and_detail_url(self) -> None:
        row = normalize_xiaomi_job(
            {
                "id": "7600322815397824774",
                "title": "软件开发工程师实习生",
                "description": "参与多个创新agent设计和研发。",
                "requirement": "熟悉服务端架构和大模型。",
                "publish_time": 1774574457787,
                "city_list": [{"name": "北京"}],
                "job_function": {"id": "7178759516879405165", "name": "软件研发类"},
                "recruit_type": {"name": "实习", "parent": {"name": "校招"}},
                "job_hot_flag": {"name": "AI人才专项"},
            }
        )

        self.assertEqual(row["source"], "xiaomi")
        self.assertEqual(row["position_id"], "7600322815397824774")
        self.assertEqual(row["position_name"], "软件开发工程师实习生")
        self.assertEqual(row["category_name"], "软件研发类")
        self.assertEqual(row["work_locations"], "北京")
        self.assertEqual(row["feature_tags"], "AI人才专项")
        self.assertEqual(
            row["position_url"],
            "https://xiaomi.jobs.f.mioffice.cn/internship/position/7600322815397824774/detail",
        )


if __name__ == "__main__":
    unittest.main()
