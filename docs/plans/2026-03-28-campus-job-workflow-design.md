# Design Doc: Split Campus Job Workflow Skills

**Date**: 2026-03-28
**Status**: Approved
**Topic**: Split the “抓岗 -> 选岗 -> 生成简历 -> 更新文档” workflow into two in-repo skills with clear boundaries.

## 1. Overview

The repository now has enough raw exports, tailored resume generators, and dashboard automation that the core job-search workflow should stop depending on session memory. The approved direction is to split the workflow into two skills:

1. `campus-job-scrape`
2. `job-fit-to-resume`

This keeps the data-refresh layer independent from the resume-and-tracking layer, while preserving `job-sync` as a separate post-application workflow.

## 2. Approved Direction

### 2.1 Skill A: `campus-job-scrape`

This skill is the data-ingest entrypoint.

It is responsible for:
- refreshing technical internship exports for selected companies
- routing the request to the correct scraper script(s)
- writing normalized `data/*.json` and `data/*.csv`
- updating `docs/temp/*crawl-status.md`

It is explicitly **not** responsible for:
- updating `docs/job-search-progress.md`
- ranking which roles to apply to
- generating or reusing resumes

### 2.2 Skill B: `job-fit-to-resume`

This skill becomes the shortlist and resume entrypoint.

It is responsible for:
- reading the latest `data/*` exports
- selecting about 3 high-fit roles per company
- deciding whether a role already has coverage, can reuse an existing template, or needs a targeted generator
- generating or reusing PDFs in `resumes/sources/`
- updating `docs/job-search-progress.md`
- writing a shortlist artifact under `docs/temp/`

### 2.3 Keep `job-sync` Separate

`job-sync` remains the post-application synchronization skill:
- parse QQ mail
- detect interview / assessment / offer updates
- sync those events back into `docs/job-search-progress.md`

This skill should not be folded into either of the two pre-application workflow skills.

### 2.4 Keep `skill-curator` Out Of Runtime

`skill-curator` is useful for evaluating whether a new external skill should be installed, kept, or pruned. It is **not** part of the runtime execution path for scraping or resume generation.

The approved rule is:
- use `skill-curator` for environment and capability governance
- do not call it from `campus-job-scrape` or `job-fit-to-resume`

## 3. Scope

### In scope

- add a shared company registry for scraper routing
- add a shared fit-profile layer for per-company ranking logic
- add a new `campus-job-scrape` skill
- upgrade `job-fit-to-resume` so it reads fresh exports and drives shortlist + resume generation + progress sync
- standardize validation for both stages

### Out of scope

- merging all three workflows into one giant skill
- rewriting existing per-company scraper logic unless a company truly needs a new source
- adding automatic email sync into the scraping or resume stage
- replacing current resume generators with a single universal generator

## 4. Architecture

### 4.1 Shared Company Registry

Create a shared registry module, for example `scripts/company_registry.py`.

Each company entry should declare only the stable routing and storage metadata:
- `company_key`
- `display_name`
- `scrape_group`
- `data_json`
- `data_csv`
- `status_doc`
- `default_top_n`
- `fit_profile_key`
- `resume_strategy_key`

This registry becomes the source of truth for:
- what companies are supported
- which scraper group owns them
- where refreshed outputs live

### 4.2 Shared Fit Profiles

Create a second shared module, for example `scripts/company_fit_profiles.py`.

This layer should contain per-company ranking knowledge:
- which role lanes to prioritize (`agent`, `ai_application`, `backend`, `platform`, `efficiency`, etc.)
- which title keywords to up-rank
- which titles should be down-ranked even if they sound attractive
- which resume template family should be reused when no company-specific generator exists

This keeps ranking and resume-mapping logic out of the skill text itself.

### 4.3 Thin Skill, Script-First Orchestration

The skills should stay thin and route into Python scripts.

Recommended helper entrypoints:
- `scripts/run_company_scrape.py`
- `scripts/run_job_fit_resume.py`

The skills call those entrypoints; the scripts handle parsing arguments, reading the registry, and orchestrating existing scraper/generator modules.

### 4.4 Scraper Routing

`campus-job-scrape` should dispatch by scrape group instead of hard-coded company branches in the skill:

- `extra_bigtech`: `netease`, `xiaomi`, `pinduoduo`, `didi`
- `more_bigtech`: `kuaishou`, `honor`, `oppo`, `bilibili`
- future single-source groups such as `baidu`

Adding a new company should first mean:
1. register the company
2. attach it to an existing scrape group or add one new scraper

### 4.5 Resume Orchestration

`job-fit-to-resume` should:
1. load fresh exports for selected companies
2. rank the best-fit roles using `company_fit_profiles.py`
3. check resume coverage
4. reuse existing targeted PDFs when possible
5. invoke matched generators when needed
6. update the dashboard and temp shortlist docs

The skill should report each role using an explicit state:
- `existing_pdf`
- `generated_now`
- `reused_template`
- `generation_failed`

## 5. Data Flow

### Stage A: `campus-job-scrape`

1. User selects company keys.
2. Skill resolves company metadata from the registry.
3. Orchestrator groups the companies by scraper family.
4. Existing scraper scripts refresh raw exports.
5. Temp crawl-status docs are updated with `refreshed`, `failed`, or `zero-result but valid`.

### Stage B: `job-fit-to-resume`

1. User selects company keys.
2. Skill loads latest exports and fit profiles.
3. Orchestrator ranks about 3 roles per company.
4. Existing coverage audit + resume generator logic determines whether to reuse or generate.
5. PDFs are produced or confirmed.
6. Temp shortlist doc and `docs/job-search-progress.md` are updated.

## 6. Error Handling

### 6.1 Scraping Stage

- A failure for one company must not invalidate successful outputs for other companies.
- New data should only replace the old file set after the company export succeeds.
- `zero-result` must be recorded explicitly when the source is valid but empty.

### 6.2 Fit And Resume Stage

- Shortlist generation should complete even if one PDF fails to build.
- Failed resume builds should be marked as `generation_failed`, not silently dropped.
- Dashboard updates should only write confirmed states.

## 7. Verification

### 7.1 Scraping Stage

- run focused scraper tests
- verify output files exist
- verify `total_count` matches the actual job list size
- verify combined exports still reconcile per-source counts

### 7.2 Fit And Resume Stage

- run focused fit / export tests
- verify shortlist doc exists
- verify expected PDFs exist
- extract PDF text and confirm target-role keywords are present

## 8. Success Criteria

- [ ] `campus-job-scrape` can refresh selected companies without touching resume logic
- [ ] `job-fit-to-resume` can take selected companies from fresh exports to shortlist + PDF + progress sync
- [ ] new companies can be added through the registry + fit profile without rewriting the skill text
- [ ] temp docs and main dashboard no longer drift as easily from raw exports and real resume artifacts
