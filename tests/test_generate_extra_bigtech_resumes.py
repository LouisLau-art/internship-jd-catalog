import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "resumes" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import generate_extra_bigtech_resumes as target


class ExtraBigtechResumeConfigTests(unittest.TestCase):
    def test_recommended_resumes_cover_four_companies(self) -> None:
        aliases = {resume["alias"] for resume in target.RESUMES}

        self.assertEqual(
            aliases,
            {
                "刘新宇-网易有道-AI应用开发实习生",
                "刘新宇-小米-AI Agent开发实习生",
                "刘新宇-小米-大模型Agent开发工程师实习生",
                "刘新宇-拼多多-服务端研发实习生",
                "刘新宇-滴滴-网约车平台公司-后端研发实习生",
            },
        )


if __name__ == "__main__":
    unittest.main()
