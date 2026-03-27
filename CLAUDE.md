# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a personalized internship job description catalog and resume generation toolkit. It tracks campus internship opportunities from major tech companies (Alibaba, Ant Group, ByteDance, Meituan, JD, Tencent, Xiaohongshu, Huawei, Xiaomi, OceanBase) and automates the generation of highly targeted resumes tailored to specific roles.

**Current Snapshot:** `2026-03-21`

**Evidence-Driven:** Fit notes and resume templates are based on actual project experience (ScholarFlow, multi-cloud-email-sender, multi-agent-skills-catalog), not fabricated claims.

The project consists of three main layers:
1. **Data Scraping (`scripts/`)**: Python utilities that fetch raw job postings directly from company career portals and export them to CSV/JSON in `data/`.
2. **Resume Generation (`resumes/sources/`, `scripts/export_resumes.py`)**: Scripts that take markdown resume templates, render them into HTML, DOCX (via Pandoc), and PDF (via headless Chrome).
3. **Curation and Notes (`docs/`, `catalog.csv`)**: Markdown files and a central CSV index containing structured notes, fit assessments, and prioritized shortlists.

## Common Commands

### Scrape Job Postings
```bash
# Scrape Alibaba, Ant, Huawei and rebuild combined export
python scripts/scrape_campus_jobs.py --output-dir data

# Scrape ByteDance separately (uses Playwright for auth)
python scripts/scrape_bytedance_jobs.py

# Scrape Meituan/JD
python scripts/scrape_meituan_jd.py

# Scrape Tencent
python scripts/scrape_tencent_jobs.py

# Scrape Xiaohongshu
python scripts/scrape_xhs_jobs.py
```

### Resume Export
```bash
# List available export jobs
python scripts/export_resumes.py --list

# Run all exports
python scripts/export_resumes.py

# Run only specific jobs
python scripts/export_resumes.py --only xiaohongshu-eco --only xiaohongshu-java

# Skip generator scripts, only export existing markdown
python scripts/export_resumes.py --skip-generators

# Note: Resume generation scripts expect a profile photo (e.g., louis-profile-photo.png)
#       to be available in the working directory as configured in scripts.
```

### Tests
```bash
python -m unittest discover tests
```

### Sync Job Notifications
```bash
# Synchronize job notifications from QQ emails to the dashboard
/sync-jobs
```

### Audit Job Fit vs Resume Coverage
```bash
# Audit suitable roles against current resume assets and sync the dashboard
/job-fit-to-resume

# Equivalent script entrypoint
python scripts/audit_resume_coverage.py --sync-doc docs/job-search-progress.md
```

## Recommended Workflow

### 1. Automation & Discovery
- **Always** start configuration, automation, or plugin/MCP setup sessions by invoking the automation recommender first with `/automation-recommender` to leverage pre-built workflows and avoid redundant setup.

### 1.5 Job Fit → Resume Coverage
- Use **`/job-fit-to-resume`** before generating a new targeted resume.
- The audit checks `docs/job-search-progress.md`, generator scripts under `resumes/scripts/`, and exported assets in `resumes/sources/`.
- Treat the audit statuses as the decision gate:
  - `generated`: reuse current PDF
  - `generator_ready`: run the matched generator script
  - `reusable`: adapt the closest existing same-company resume
  - `missing`: create a new targeted version

### 2. AI-Native Resume Generation (The Deep Diver)
- Use the **`/generate-resume`** pattern to extract high-leverage "AI-Native Engineering" evidence.
- **MANDATORY**: Audit `.claude/handoffs/` for specific technical fixes (e.g., "Patched session-handoff validator", "Model switching strategy for 400 errors") to prove engineering depth.
- **Pattern**: `Problem -> AI Constraint -> Engineering Solution`.

### 3. Safety & Context Management
- **Pre-flight Check**: ALWAYS run a glob/ls preview (e.g., `ls resumes/sources/*.pdf`) before any mass deletion or file organization.
- **Context Preservation**: For context-heavy tasks, switch to **ModelScope/Kimi-K2.5** early if encountering context-length 400 errors with other models.
- **Handoffs**: Use `session-handoff` to preserve state across long-running tasks.

## High-Level Architecture

### Data Flow
```
Company Career Portals
    ↓
[scrape_*.py] → raw JSON/CSV (data/)
    ↓
[manual curation] → catalog.csv + docs/companies/*.md
    ↓
[generate_*_resumes.py] → markdown templates (resumes/sources/)
    ↓
[export_resumes.py] → HTML → DOCX/PDF
```

### Key Files

| Path | Purpose |
|------|---------|
| `catalog.csv` | Curated shortlist with fit notes (small, reviewed) |
| `data/*.csv` / `data/*.json` | Raw bulk exports from company sites (large, unsifted) |
| `data/campus_positions_combined.csv` | Union of all raw exports |
| `docs/companies/*.md` | Structured notes per company |
| `docs/*-top-*.md` | Prioritized shortlists |
| `scripts/scrape_campus_jobs.py` | Main scraper for Alibaba/Ant/Huawei + combiner |
| `scripts/export_resumes.py` | Unified resume export entrypoint |
| `resumes/export_manifest.json` | Defines export jobs for `export_resumes.py` |

### Fit Legend
- `strong`: worth prioritizing
- `medium`: can apply if needed
- `stretch`: possible, but not a natural fit
- `low`: weak match
- `avoid`: likely waste of application bandwidth

### Data Schema (Raw Exports)
All CSV exports in `data/` share a consistent schema with columns: `source`, `company`, `position_id`, `position_name`, `position_url`, `work_locations`, `departments`, `requirement`, `description`, `batch_id`, `category_name`, etc.

### External Dependencies
- `pandoc` - for markdown → DOCX conversion
- `google-chrome` / `google-chrome-stable` - for HTML → PDF conversion (headless mode)

## Development Conventions

- **Code Style:** Python scripts use type hinting (`from __future__ import annotations`, `typing`) and follow structured data normalization patterns.
- **Data Management:** Raw data dumps from scrapers are intentionally kept in `data/` to avoid polluting the curated `catalog.csv` at the root. Data is exported in both `.csv` and `.json` formats.
- **Gitignore:** Generated artifacts (`.pdf`, `.docx`, `.png`) and certain scripts (`scripts/export_resumes.py`, `tests/test_export_resumes.py`) are excluded from Git to keep the repository lightweight. The `resumes/` and `resume-refresh-*/` directories are also gitignored.
- **Testing:** The project uses a standard Python `unittest` framework for testing scripts (located in `tests/`).

## Gotchas

- Some files referenced in documentation (e.g., `scripts/export_resumes.py`, `resumes/export_manifest.json`) may be gitignored and not present in the working tree.
- Personal resume sources and generated application materials are intentionally kept out of Git so that the repository can stay publishable.
- The curated root `catalog.csv` is kept separate from raw `data/` exports to prevent large site dumps from polluting the reviewed shortlist.
