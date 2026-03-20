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
  - exported rows: `449`
- `antgroup_positions_26022600074513.csv` / `.json`
  - source: Ant Group campus site
  - batch: `26022600074513`
  - exported rows: `96`
- `campus_positions_combined.csv` / `.json`
  - combined exported rows: `545`

## Flat CSV schema

All CSV exports share the same columns:

- `source`
- `company`
- `position_id`
- `position_name`
- `position_url`
- `batch_id`
- `batch_name`
- `category_name`
- `work_locations`
- `interview_locations`
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
