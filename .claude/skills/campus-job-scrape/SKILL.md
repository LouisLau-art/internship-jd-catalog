---
name: campus-job-scrape
description: Use when refreshing raw internship exports for selected companies, rebuilding company-specific JSON or CSV snapshots, or updating crawl status notes without touching resume generation.
---

# Campus Job Scrape

## Overview
This is the first half of the workflow. It refreshes selected company raw exports and writes only two places: `data/` and `docs/temp/*crawl-status.md`.

## When to Use
- You need the latest technical internship roles for one or more companies.
- You want to reuse existing scrapers by company family instead of calling them manually.
- You want a clean crawl status note before shortlist or resume work starts.

## `/campus-job-scrape`

1. Refresh selected companies with one entrypoint:
   `python scripts/run_company_scrape.py --companies alibaba,antgroup,bytedance,meituan,jd,tencent,xiaohongshu,huawei,netease,pinduoduo,didi,xiaomi,kuaishou,honor,oppo,bilibili --refresh-mode cached`
2. Choose `--refresh-mode live` when you want a real fetch; keep `cached` for cheaper reruns.
3. Read the generated status note in `docs/temp/`, for example:
   `docs/temp/2026-03-29-campus-core-crawl-status.md`

## Scrape Families
- `campus_core`: Alibaba, Ant Group, ByteDance, Meituan, JD, Tencent, Xiaohongshu, Huawei
- `extra_bigtech`: NetEase, Pinduoduo, Didi, Xiaomi
- `more_bigtech`: Kuaishou, Honor, OPPO, Bilibili

## Scope Boundary
- It updates `data/*.json|csv`.
- It updates `docs/temp/*crawl-status.md`.
- It does **not** generate resumes.
- It does **not** update `docs/job-search-progress.md`.

## Common Mistakes
- Running downstream shortlist or resume work before the raw exports are refreshed.
- Editing the main notebook here instead of leaving that to `/job-fit-to-resume`.
- Calling family scrapers directly when `scripts/run_company_scrape.py` already knows the grouping.
