#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXPORT_DIR = REPO_ROOT / "resumes" / "sources"
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")


def is_public_resume_pdf(path: Path) -> bool:
    return path.suffix.lower() == ".pdf" and bool(CHINESE_RE.search(path.stem))


def find_unwanted_files(export_dir: Path) -> list[Path]:
    return sorted(path for path in export_dir.iterdir() if path.is_file() and not is_public_resume_pdf(path))


def clean_resume_sources(export_dir: Path) -> list[Path]:
    removed = find_unwanted_files(export_dir)
    for path in removed:
        path.unlink()
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(description="Keep resumes/sources limited to Chinese-named resume PDFs.")
    parser.add_argument(
        "--dir",
        type=Path,
        default=DEFAULT_EXPORT_DIR,
        help="Directory to clean. Defaults to resumes/sources.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Only print files that would be removed.")
    args = parser.parse_args()

    targets = find_unwanted_files(args.dir)
    if args.dry_run:
        for path in targets:
            print(path)
        return

    removed = clean_resume_sources(args.dir)
    for path in removed:
        print(path)


if __name__ == "__main__":
    main()
