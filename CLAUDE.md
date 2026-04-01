# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a personalized internship job description catalog and resume generation toolkit. It tracks campus internship opportunities from major tech companies (Alibaba, Ant Group, ByteDance, Meituan, JD, Tencent, Xiaohongshu, Huawei, Xiaomi, OceanBase, NetEase, Pinduoduo, Didi, Kuaishou, Honor, OPPO, Bilibili) and automates the generation of highly targeted resumes tailored to specific roles.

**Workflow Snapshot:** `main` currently includes the two-stage company workflow (`campus-job-scrape` -> `job-fit-to-resume` -> `job-sync`), validated handoffs, and local study-note tracking.

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

# Scrape extra bigtech (NetEase, Pinduoduo, Didi, Xiaomi)
python scripts/scrape_extra_bigtech.py

# Scrape more bigtech (Kuaishou, Honor, OPPO, Bilibili)
python scripts/scrape_more_bigtech.py
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

### Two-Stage Company Workflow
```bash
# Stage 1: refresh raw exports for selected companies and write crawl status notes
/campus-job-scrape

# Equivalent script entrypoint
python scripts/run_company_scrape.py --companies alibaba,antgroup,bytedance,meituan,jd,tencent,xiaohongshu,huawei,netease,pinduoduo,didi,xiaomi,kuaishou,honor,oppo,bilibili --refresh-mode cached

# Stage 2: rank top roles, generate/reuse resumes, and sync the main notebook
/job-fit-to-resume

# Equivalent script entrypoint
python scripts/run_job_fit_resume.py --companies alibaba,antgroup,bytedance,meituan,jd,tencent,xiaohongshu,huawei --top-n-per-company 3

# Safe dry run: rank roles without generating PDFs or syncing the dashboard
python scripts/run_job_fit_resume.py --companies alibaba,bytedance,xiaohongshu --top-n-per-company 3 --no-generate --no-sync-progress --output-doc docs/temp/YYYY-MM-DD-campus-core-dryrun-shortlist.md
```

### Sync Job Notifications
```bash
# Synchronize job notifications from QQ emails to the dashboard
/sync-jobs
```

### Legacy Resume Coverage Audit
```bash
# Use this when you only want coverage audit, not the full shortlist workflow
python scripts/audit_resume_coverage.py --sync-doc docs/job-search-progress.md
```

### Tests
```bash
python -m unittest discover tests
```

## Recommended Workflow

### 1. Automation & Discovery
- Prefer repo-local skills first: `/campus-job-scrape`, `/job-fit-to-resume`, `/sync-jobs`.
- Treat `/automation-recommender` as optional/global only; do not assume this repo provides it.

### 2. Company Scrape
- Use **`/campus-job-scrape`** as the default stage-1 entrypoint for company shortlist work.
- The orchestrator groups companies by scraper family (`campus_core`, `extra_bigtech`, `more_bigtech`) and writes only to `data/*.json|csv` and `docs/temp/*crawl-status.md`.
- Keep the scope narrow here: no resume generation and no main notebook edits.

### 3. Job Fit → Resume Coverage
- Use **`/job-fit-to-resume`** after stage 1.
- The orchestrator reads refreshed company exports, picks the top `N` roles per company, maps them to targeted resumes, optionally runs generator scripts, and syncs `docs/job-search-progress.md`.
- Treat resume states as the decision gate:
  - `existing_pdf`: current PDF is ready to use
  - `generated_now`: a missing PDF was generated in this run
  - `reused_template`: reuse the mapped same-company version
  - `generation_failed`: investigate the matched generator before hand-editing

### 4. AI-Native Resume Generation (The Deep Diver)
- There is no repo-local `/generate-resume` slash command. For deep resume rewriting, use `resumes/scripts/ai-native-resume-generation/SKILL.md` or the concrete `generate_*_resumes.py` scripts.
- **MANDATORY**: Audit `.claude/handoffs/` for specific technical fixes (e.g., "Patched session-handoff validator", "Model switching strategy for 400 errors") to prove engineering depth.
- **Pattern**: `Problem -> AI Constraint -> Engineering Solution`.

### 5. Safety & Context Management
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
[run_company_scrape.py] → docs/temp/*crawl-status.md
    ↓
[run_job_fit_resume.py] → shortlist + progress sync
    ↓
[generate_*_resumes.py] / [export_resumes.py] → HTML → DOCX/PDF
```

### Key Files

| Path | Purpose |
|------|---------|
| `catalog.csv` | Curated shortlist with fit notes (small, reviewed) |
| `data/*.csv` / `data/*.json` | Raw bulk exports from company sites (large, unsifted) |
| `data/campus_positions_combined.csv` | Union of all raw exports |
| `docs/companies/*.md` | Structured notes per company |
| `docs/*-top-*.md` | Prioritized shortlists |
| `scripts/scrape_campus_jobs.py` | Main scraper for Alibaba/Ant/Huawei + combined-export rebuild for ByteDance/Meituan/JD/Tencent/Xiaohongshu |
| `scripts/scrape_extra_bigtech.py` | Scraper for NetEase/Pinduoduo/Didi/Xiaomi |
| `scripts/scrape_more_bigtech.py` | Scraper for Kuaishou/Honor/OPPO/Bilibili |
| `scripts/company_registry.py` | Company metadata and scrape-group routing |
| `scripts/company_fit_profiles.py` | Per-company priority roles and resume mappings |
| `scripts/run_company_scrape.py` | Stage-1 scrape orchestrator |
| `scripts/run_job_fit_resume.py` | Stage-2 shortlist and resume orchestrator |
| `scripts/export_resumes.py` | Unified resume export entrypoint |
| `resumes/scripts/generate_unapplied_bigtech_resumes.py` | Resume generator for NetEase/Pinduoduo/Didi/Kuaishou/Honor/OPPO |
| `resumes/scripts/generate_extra_bigtech_resumes.py` | Resume generator for Xiaomi |
| `resumes/export_manifest.json` | Defines export jobs for `export_resumes.py` |
| `.claude/skills/campus-job-scrape/SKILL.md` | Skill wrapper for stage-1 scrape orchestration |
| `.claude/skills/job-fit-to-resume/SKILL.md` | Skill wrapper for stage-2 shortlist and resume sync |

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

## Environment Prerequisites

- Python environment should include at least `requests`.
- Live ByteDance / Bilibili scraping may require Playwright plus `playwright install chromium`.
- `/sync-jobs` requires a local `.env` with `QQ_EMAIL` and `QQ_AUTH_CODE`.
- Resume export depends on `pandoc`, Chrome, and usually a configured profile photo path (for example via `RESUME_PHOTO` or the script defaults).

## Development Conventions

- **Code Style:** Python scripts use type hinting (`from __future__ import annotations`, `typing`) and follow structured data normalization patterns.
- **Data Management:** Raw data dumps from scrapers are intentionally kept in `data/` to avoid polluting the curated `catalog.csv` at the root. Data is exported in both `.csv` and `.json` formats.
- **Gitignore:** Generated artifacts (`.pdf`, `.docx`, `.png`) and certain scripts (`scripts/export_resumes.py`, `tests/test_export_resumes.py`) are excluded from Git to keep the repository lightweight. The `resumes/` and `resume-refresh-*/` directories are also gitignored.
- **Testing:** The project uses a standard Python `unittest` framework for testing scripts (located in `tests/`).
- **Workflow Split:** Keep the three scrape families (`campus_core`, `extra_bigtech`, `more_bigtech`) in stage 1, then run shortlist/resume in stage 2. `job-sync` stays separate from both.

## Tracking Boundaries

- `data/*.json|csv` are tracked raw exports and should be treated as the durable source of truth for refreshed company data.
- `.firecrawl/`, `docs/temp/`, `.claude/temp/`, and `.tmp/` are generated working artifacts and are intentionally untracked.
- When a workflow writes temp shortlist or crawl-status docs, treat them as disposable run outputs unless there is an explicit reason to promote them.

## Troubleshooting & Common Issues

### Scraping Issues
- **Playwright登录失败**: 运行`playwright install chromium`安装浏览器，检查网络连接和滑块验证是否需要手动干预
- **网站结构变化**: 公司官网更新后需要调整对应的XPath/CSS选择器
- **IP被限制**: 增加请求间隔时间，或使用代理池

### Resume Export Issues
- **Pandoc转换错误**: 检查Markdown语法是否正确，特别是表格和列表格式
- **Chrome无头模式启动失败**: 确保已安装`google-chrome-stable`，尝试`google-chrome --version`验证
- **中文字体显示问题**: 安装中文字体包（如`fonts-noto-cjk`），确保PDF生成时字体路径正确
- **图片加载失败**: 检查头像图片路径是否正确，支持绝对路径和相对路径

### Sync Issues
- **QQ邮件同步失败**: 检查IMAP权限是否开启，授权码是否正确配置

## Gotchas

- Some files referenced in documentation (e.g., `scripts/export_resumes.py`, `resumes/export_manifest.json`) may be gitignored and not present in the working tree.
- Personal resume sources and generated application materials are intentionally kept out of Git so that the repository can stay publishable.
- The curated root `catalog.csv` is kept separate from raw `data/` exports to prevent large site dumps from polluting the reviewed shortlist.
- `campus_core` companies do not always have dedicated per-company JSON exports. Stage 2 reads `data/campus_positions_combined.*` and filters rows by `source` through `scripts/company_registry.py`.
- Companies are split into three scrape groups: `campus_core` (Alibaba, Ant Group, ByteDance, Meituan, JD, Tencent, Xiaohongshu, Huawei), `extra_bigtech` (NetEase, Pinduoduo, Didi, Xiaomi), and `more_bigtech` (Kuaishou, Honor, OPPO, Bilibili).
