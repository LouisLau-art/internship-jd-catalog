# Campus Job Workflow Split Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Split the repo’s job-search workflow into two thin skills, one for refreshing technical-intern exports and one for selecting high-fit roles, generating resumes, and syncing the dashboard.

**Architecture:** Introduce a shared company registry plus company fit-profile layer, then add two script-first orchestration entrypoints. `campus-job-scrape` routes selected companies to existing scraper families and updates temp crawl-status docs. `job-fit-to-resume` reads the latest exports, ranks about three roles per company, reuses or generates PDFs, and then updates the shortlist doc and `docs/job-search-progress.md`.

**Tech Stack:** Python 3.x, existing scraper scripts, existing resume generators, Markdown docs, Claude custom skills.

---

### Task 1: Add failing tests for the shared registry and fit-profile layer

**Files:**
- Create: `tests/test_company_registry.py`
- Create: `tests/test_company_fit_profiles.py`

**Step 1: Write the failing registry tests**

Cover:
- company key lookup
- scrape-group routing
- required output paths
- unsupported-company rejection

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_company_registry.py tests/test_company_fit_profiles.py -q`

Expected: import or missing-symbol failures because the shared modules do not exist yet.

### Task 2: Implement the shared company registry and fit profiles

**Files:**
- Create: `scripts/company_registry.py`
- Create: `scripts/company_fit_profiles.py`
- Test: `tests/test_company_registry.py`
- Test: `tests/test_company_fit_profiles.py`

**Step 1: Implement company registry entries**

Register at least:
- `netease`
- `pinduoduo`
- `didi`
- `xiaomi`
- `kuaishou`
- `honor`
- `oppo`
- `bilibili`

**Step 2: Implement fit-profile entries**

Encode:
- preferred role lanes
- up-rank keywords
- down-rank keywords
- fallback resume family
- default `top_n`

**Step 3: Run tests to verify green**

Run: `python -m pytest tests/test_company_registry.py tests/test_company_fit_profiles.py -q`

Expected: PASS.

### Task 3: Add the scraping orchestration script with TDD

**Files:**
- Create: `tests/test_run_company_scrape.py`
- Create: `scripts/run_company_scrape.py`

**Step 1: Write the failing orchestration tests**

Cover:
- selecting companies by key
- grouping by scrape family
- building the correct downstream command plan
- rejecting unsupported company keys

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_run_company_scrape.py -q`

Expected: import failure or missing-function failure.

**Step 3: Write minimal orchestration code**

The script should:
- parse `--companies`
- parse `--refresh-mode`
- load the registry
- group selected companies by scrape family
- invoke existing scraper scripts only once per family
- update temp crawl-status docs through a thin helper layer

**Step 4: Run tests to verify it passes**

Run: `python -m pytest tests/test_run_company_scrape.py -q`

Expected: PASS.

### Task 4: Add the new `campus-job-scrape` skill

**Files:**
- Create: `.claude/skills/campus-job-scrape/SKILL.md`
- Modify: `CLAUDE.md`

**Step 1: Add the skill entrypoint**

Document:
- supported company keys
- live vs cached refresh
- outputs written to `data/` and `docs/temp/`
- non-goals: no shortlist, no resume generation, no progress-doc sync

**Step 2: Advertise the entrypoint**

Add the new command to `CLAUDE.md` workflow guidance.

### Task 5: Add failing tests for the shortlist-and-resume orchestration

**Files:**
- Create: `tests/test_run_job_fit_resume.py`

**Step 1: Write the failing tests**

Cover:
- selecting top N roles per company from fresh exports
- applying fit-profile ranking rules
- mapping to resume coverage states
- generating a shortlist result model before touching docs or PDFs

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_run_job_fit_resume.py -q`

Expected: import failure or missing-function failure.

### Task 6: Implement the shortlist-and-resume orchestration script

**Files:**
- Create: `scripts/run_job_fit_resume.py`
- Modify: `scripts/audit_resume_coverage.py`
- Modify: `resumes/export_manifest.json`
- Modify: `tests/test_generate_unapplied_bigtech_resumes.py`
- Test: `tests/test_run_job_fit_resume.py`

**Step 1: Build shortlist selection**

Read selected company exports and fit profiles, then rank about three roles per company.

**Step 2: Build resume resolution**

For each shortlisted role, classify it as:
- `existing_pdf`
- `generated_now`
- `reused_template`
- `generation_failed`

**Step 3: Integrate existing generators**

Route to the correct targeted generator script or reuse flow without replacing the existing per-company generators.

**Step 4: Sync docs**

Write:
- `docs/temp/YYYY-MM-DD-*-shortlist.md`
- `docs/job-search-progress.md`

**Step 5: Run tests to verify green**

Run: `python -m pytest tests/test_run_job_fit_resume.py tests/test_generate_unapplied_bigtech_resumes.py -q`

Expected: PASS.

### Task 7: Upgrade the `job-fit-to-resume` skill

**Files:**
- Modify: `.claude/skills/job-fit-to-resume/SKILL.md`
- Modify: `CLAUDE.md`

**Step 1: Rewrite the skill scope**

Document that the skill now:
- reads fresh exports
- ranks top roles per company
- checks / generates resume coverage
- updates shortlist docs and the progress dashboard

**Step 2: Keep the boundary explicit**

Document that scraping belongs to `campus-job-scrape`, and post-application email syncing belongs to `job-sync`.

### Task 8: Verify the full two-stage workflow

**Files:**
- Modify: `docs/temp/2026-03-27-more-bigtech-crawl-status.md`
- Modify: `docs/job-search-progress.md`
- Modify: one fresh shortlist file under `docs/temp/`

**Step 1: Run the scrape stage**

Run: `python scripts/run_company_scrape.py --companies netease,pinduoduo,didi,kuaishou,honor,oppo --refresh-mode live`

Expected: refreshed exports and updated crawl-status docs.

**Step 2: Run the fit-and-resume stage**

Run: `python scripts/run_job_fit_resume.py --companies netease,pinduoduo,didi,kuaishou,honor,oppo --top-n-per-company 3`

Expected: shortlist doc, updated progress doc, and expected PDFs.

**Step 3: Run focused regressions**

Run: `python -m pytest tests/test_company_registry.py tests/test_company_fit_profiles.py tests/test_run_company_scrape.py tests/test_run_job_fit_resume.py tests/test_generate_unapplied_bigtech_resumes.py tests/test_scrape_extra_bigtech.py tests/test_scrape_more_bigtech.py -q`

Expected: PASS.
