# Public Repo Privacy Boundary And Daily Intern Expansion Design

**Date:** 2026-03-21

## Goal

Keep this repository publishable by removing resume artifacts that contain personal information from the tracked tree, while continuing to expand the raw internship export layer with the new Ant Group and ByteDance daily-intern sources.

## Approved Direction

The approved approach is `A`:

- keep scraping scripts, raw JD exports, and company notes in the repo
- remove tracked `resumes/` content and resume refresh folders from the Git snapshot
- add ignore rules so future resume artifacts stay local

## Scope

### In scope

- add Git ignore rules for private resume material
- remove tracked resume files from the repository snapshot without deleting the local working copies
- add the Ant Group batch `25051200066269`
- add the ByteDance daily internship backend project `7194661644654577981`
- make the combined export reflect all maintained raw exports
- update README and raw-data documentation so internship types are explicit

### Out of scope

- rewriting existing Git history
- deleting local private files
- building a public web UI on top of the exports
- fully re-ranking every curated shortlist in `catalog.csv`

## Architecture

The repo will keep two clear layers:

1. `public data layer`
   - scraper code
   - normalized CSV/JSON exports
   - company notes and shortlist docs

2. `private application layer`
   - tailored resumes
   - generated export bundles
   - photo assets
   - resume refresh work folders

The public layer remains committed. The private layer is ignored and untracked.

## Data Flow

### Ant Group

`scripts/scrape_campus_jobs.py` already knows how to paginate Ant Group campus batches. Extend it so one run exports both:

- existing batch `26022600074513`
- new batch `25051200066269`

Both batches should be written as separate CSV/JSON snapshots and then merged into the combined export with source metadata that preserves the batch identity.

### ByteDance

`scripts/scrape_bytedance_jobs.js` already supports parameterized `project-id`, `project-name`, `project-slug`, `category-id`, and `category-slug`. Reuse that for the new daily internship backend source and then teach the Python combine flow to ingest maintained ByteDance export files from `data/`.

## Privacy Boundary

`.gitignore` must cover:

- `resumes/`
- `resume-refresh-*`
- similar generated local resume bundles

Tracked resume files must be removed from Git with a cached delete so local copies stay on disk.

## Risk Note

Ignoring and untracking files protects the current snapshot only. Earlier pushed commits may still contain personal information. That requires a separate history-rewrite decision before confidently flipping the repository to public visibility.

## Verification

- run unit tests for the Python scraper
- run the Ant/Huawei/Alibaba export script
- run the ByteDance export script for the new project
- verify combined counts and the presence of new output files
- verify `git status` no longer shows private resume files as tracked changes
