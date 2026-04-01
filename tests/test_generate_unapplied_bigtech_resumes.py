import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "resumes" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import generate_unapplied_bigtech_resumes as target


class UnappliedBigtechResumeConfigTests(unittest.TestCase):
    def test_resume_aliases_cover_seven_unapplied_companies(self) -> None:
        aliases = {resume["alias"] for resume in target.RESUMES}

        self.assertEqual(
            aliases,
            {
                "刘新宇-网易-AI应用开发实习生",
                "刘新宇-网易-AI平台研发工程师",
                "刘新宇-网易-服务端开发工程师",
                "刘新宇-拼多多-服务端研发实习生",
                "刘新宇-拼多多-大模型算法实习生",
                "刘新宇-拼多多-web前端研发实习生",
                "刘新宇-滴滴-网约车技术部-后端研发实习生",
                "刘新宇-滴滴-网约车平台公司-后端研发实习生",
                "刘新宇-滴滴-企业服务事业群-后端研发实习生",
                "刘新宇-快手-AI-Agent研发工程师-实习生",
                "刘新宇-快手-AI-Agent研发实习生-AgentOps方向",
                "刘新宇-快手-AI应用开发实习生-效率工程部",
                "刘新宇-荣耀-AI模型能力评测工程师",
                "刘新宇-荣耀-互联网算法工程师",
                "刘新宇-荣耀-机器人软件系统开发工程师",
                "刘新宇-OPPO-应用开发工程师-AI-Agent方向",
                "刘新宇-OPPO-应用开发工程师-AI-Infra-AIOps方向",
                "刘新宇-OPPO-后端工程师",
                "刘新宇-哔哩哔哩-AI开发实习生-应用工程方向",
                "刘新宇-哔哩哔哩-AI创作开发实习生",
                "刘新宇-哔哩哔哩-AI创作系统后端实习生-Python-Flask",
            },
        )

    def test_each_company_has_three_targeted_resumes(self) -> None:
        counts: dict[str, int] = {}
        for resume in target.RESUMES:
            company = str(resume["alias"]).split("-")[1]
            counts[company] = counts.get(company, 0) + 1

        self.assertEqual(
            counts,
            {
                "网易": 3,
                "拼多多": 3,
                "滴滴": 3,
                "快手": 3,
                "荣耀": 3,
                "OPPO": 3,
                "哔哩哔哩": 3,
            },
        )


if __name__ == "__main__":
    unittest.main()
