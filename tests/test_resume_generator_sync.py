import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "resumes" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import generate_alibaba_resumes as alibaba
import generate_antgroup_resumes as antgroup
import generate_xhs_resumes_tailored as xhs_tailored


PHOTO = xhs_tailored.base.resolve_photo()


def normalize_markdown(text: str) -> str:
    return text.strip() + "\n"


class ResumeGeneratorSyncTests(unittest.TestCase):
    def assert_render_matches_activity_source(
        self,
        rendered: str,
        markdown_path: Path,
    ) -> None:
        expected = markdown_path.read_text(encoding="utf-8")
        self.assertEqual(normalize_markdown(rendered), normalize_markdown(expected))

    def test_alibaba_activity_source_matches_generator_data(self) -> None:
        rendered = alibaba.base.render_markdown(alibaba.RESUMES[0], PHOTO)
        self.assert_render_matches_activity_source(
            rendered,
            REPO_ROOT / "resumes" / "scripts" / "alibaba-ai-application-rd-engineer-resume.md",
        )

    def test_ant_activity_source_matches_generator_data(self) -> None:
        rendered = antgroup.base.render_markdown(antgroup.RESUMES[0], PHOTO)
        self.assert_render_matches_activity_source(
            rendered,
            REPO_ROOT / "resumes" / "scripts" / "ant-ai-engineer-application-resume.md",
        )

    def test_xhs_activity_source_matches_generator_data(self) -> None:
        rendered = xhs_tailored.base.render_markdown(xhs_tailored.RESUMES[0], PHOTO)
        self.assert_render_matches_activity_source(
            rendered,
            REPO_ROOT / "resumes" / "scripts" / "xhs-ai-native-dev-tooling-resume.md",
        )


if __name__ == "__main__":
    unittest.main()
