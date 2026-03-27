import re
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "resumes" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import generate_xhs_resumes as xhs
import generate_xiaomi_resumes as xiaomi


def extract_section(markdown: str, heading: str) -> str:
    match = re.search(rf"## {re.escape(heading)}\n(?P<section>[\s\S]*?)(?:\n## |\Z)", markdown)
    if not match:
        raise AssertionError(f"missing section: {heading}")
    return match.group("section")


class ResumeSharedProfileTests(unittest.TestCase):
    def test_common_profile_contains_detailed_education_and_language(self) -> None:
        postgraduate = xhs.COMMON["education"][0]
        undergraduate = xhs.COMMON["education"][1]

        self.assertIn("2025.09 - 2027.06", postgraduate["meta"])
        self.assertIn("人工智能教育学部", postgraduate["meta"])
        self.assertIn("时空预测", postgraduate["note"])
        self.assertIn("崔建群", postgraduate["note"])

        self.assertIn("2019.09 - 2023.06", undergraduate["meta"])
        self.assertIn("信息工程学院", undergraduate["meta"])
        self.assertIn("范士喜", undergraduate["note"])

        self.assertEqual(
            xhs.COMMON["language"],
            ["英语 CET-4：610 分", "英语 CET-6：469 分"],
        )

    def test_xhs_markdown_includes_language_and_new_project_focus(self) -> None:
        markdown = xhs.render_markdown(xhs.RESUMES[0], Path("/tmp/louis-photo.png"))
        projects_section = extract_section(markdown, "重点项目")

        self.assertIn("## 语言能力", markdown)
        self.assertIn("英语 CET-4：610 分", markdown)
        self.assertIn("multi-agent-skills-catalog", projects_section)
        self.assertIn("internship-jd-catalog", projects_section)
        self.assertIn("louislau-art.github.io（个人主页 / 技术博客）", projects_section)
        self.assertNotIn("ScholarFlow（学术出版工作流系统）", projects_section)
        self.assertNotIn("multi-cloud-email-sender", projects_section)

    def test_xiaomi_markdown_includes_language_and_new_project_focus(self) -> None:
        markdown = xiaomi.render_markdown(xiaomi.RESUMES[0])
        projects_section = extract_section(markdown, "重点项目")

        self.assertIn("## 语言能力", markdown)
        self.assertIn("英语 CET-6：469 分", markdown)
        self.assertIn("multi-agent-skills-catalog", projects_section)
        self.assertIn("internship-jd-catalog", projects_section)
        self.assertIn("louislau-art.github.io（个人主页 / 技术博客）", projects_section)
        self.assertNotIn("ScholarFlow（学术出版工作流系统）", projects_section)
        self.assertNotIn("multi-cloud-email-sender", projects_section)


if __name__ == "__main__":
    unittest.main()
