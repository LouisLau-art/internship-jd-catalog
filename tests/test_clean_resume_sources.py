import os
import sys
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts import clean_resume_sources as cleanup


def test_is_public_resume_pdf_requires_pdf_and_chinese_name():
    assert cleanup.is_public_resume_pdf(Path("刘新宇-网易游戏-AI应用工程师.pdf")) is True
    assert cleanup.is_public_resume_pdf(Path("netease-games-ai-application-engineer-resume.pdf")) is False
    assert cleanup.is_public_resume_pdf(Path("刘新宇-网易游戏-AI应用工程师.docx")) is False


def test_clean_resume_sources_removes_non_pdf_and_slug_exports(tmp_path: Path):
    export_dir = tmp_path / "sources"
    export_dir.mkdir()

    keep = export_dir / "刘新宇-网易游戏-AI应用工程师.pdf"
    remove_docx = export_dir / "刘新宇-网易游戏-AI应用工程师.docx"
    remove_slug_pdf = export_dir / "netease-games-ai-application-engineer-resume.pdf"
    remove_slug_docx = export_dir / "netease-games-ai-application-engineer-resume.docx"

    keep.write_text("pdf", encoding="utf-8")
    remove_docx.write_text("docx", encoding="utf-8")
    remove_slug_pdf.write_text("pdf", encoding="utf-8")
    remove_slug_docx.write_text("docx", encoding="utf-8")

    removed = cleanup.clean_resume_sources(export_dir)

    assert [path.name for path in removed] == [
        "netease-games-ai-application-engineer-resume.docx",
        "netease-games-ai-application-engineer-resume.pdf",
        "刘新宇-网易游戏-AI应用工程师.docx",
    ]
    assert keep.exists() is True
    assert remove_docx.exists() is False
    assert remove_slug_pdf.exists() is False
    assert remove_slug_docx.exists() is False
