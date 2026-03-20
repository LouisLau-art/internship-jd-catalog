# Raw Export Layer

This directory stores bulk site exports that are useful for later filtering, shortlisting, and tailored resume generation.

These files are **not** the same thing as the curated `catalog.csv` at the repo root:

- `catalog.csv`
  Small, manually reviewed shortlist with fit notes.
- `data/*.csv` / `data/*.json`
  Large raw pools exported directly from company campus job pages.

## Current snapshots

- `alibaba_positions_100000540002.csv` / `.json`
  - source: Alibaba campus site
  - batch: `100000540002`
  - exported rows: `455`
- `alibaba_positions_100000560002_tech.csv` / `.json`
  - source: Alibaba campus site
  - batch: `100000560002`
  - source batch rows before filtering: `115`
  - filter: `category_name == 技术类`
  - exported rows: `72`
- `antgroup_positions_26022600074513.csv` / `.json`
  - source: Ant Group campus site
  - batch: `26022600074513`
  - exported rows: `96`
- `huawei_positions_intern.csv` / `.json`
  - source: Huawei campus site
  - page: internship campus portal (`jobType=0`, `jobTypes=0`)
  - exported position cards: `20`
  - exported intent-level rows: `80`
- `huawei_positions_wuhan_rd.csv` / `.json`
  - source: Huawei campus site
  - filter: intent rows whose locations include `武汉` and whose family code is `JFC1`
  - exported rows: `73`
- `campus_positions_combined.csv` / `.json`
  - combined exported rows: `703`

## Flat CSV schema

All CSV exports share the same columns:

- `source`
- `company`
- `position_id`
- `parent_position_id`
- `job_requirement_id`
- `position_intention_id`
- `position_intention_name`
- `position_name`
- `position_url`
- `position_req_code`
- `batch_id`
- `batch_name`
- `category_name`
- `family_code`
- `family_name`
- `data_source`
- `work_locations`
- `interview_locations`
- `departments`
- `circles`
- `circle_codes`
- `channels`
- `feature_tags`
- `publish_time`
- `modify_time`
- `graduation_from`
- `graduation_to`
- `requirement`
- `description`

## Intended workflow

1. Refresh raw exports with `scripts/scrape_campus_jobs.py`
2. Keep raw data in `data/`
3. Only promote reviewed positions into:
   - `catalog.csv`
   - `docs/companies/*.md`
   - company-specific top-N shortlist docs
