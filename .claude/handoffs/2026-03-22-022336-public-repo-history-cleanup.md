# Handoff: Public Repo History Cleanup And Internship Export Expansion

## Session Metadata
- Created: 2026-03-22 02:23:36
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: ~90 minutes

### Recent Commits (for context)
  - 0e282ff docs(jd): add expanded alibaba ant and bytedance top-10 shortlists
  - 8c0f4cd feat(repo): expand internship exports and remove private resumes
  - fc4ad41 feat(jd): add bytedance byteintern backend export
  - 49a6a04 feat(jd): expand campus exports and add daily shortlist
  - 38cee8e docs(jd): split alibaba and ant shortlists

## Handoff Chain

- **Continues from**: None
- **Supersedes**: None

## Current State Summary

This session completed two major tracks. First, the repo's raw export layer was expanded to cover a second Ant Group internship batch and a ByteDance `DailyIntern + 后端` pool, with `data/campus_positions_combined.*` rebuilt to `1516` rows. Second, the repository was made safe to publish: `resumes/` was removed from the tracked tree, `.gitignore` was updated, the entire Git history was rewritten with `git-filter-repo --path resumes --invert-paths`, the rewritten `main` was force-pushed, and the GitHub repo was switched from `PRIVATE` to `PUBLIC`. The repo is now clean, on `main`, and tracking `origin/main`.

## Codebase Understanding

### Architecture Overview

The repo has a clear split between a public raw-data layer and a curated shortlist layer. Public scraping and normalization live under `scripts/`, raw CSV/JSON exports live under `data/`, and company-specific notes live under `docs/companies/`. The root `catalog.csv` is intentionally smaller and manually curated. `scripts/scrape_campus_jobs.py` owns Alibaba, Ant Group, Huawei, and the rebuild of the combined export. ByteDance is scraped separately via `scripts/scrape_bytedance_jobs.py`, which writes normalized raw exports into `data/`; the Python combine step then ingests those maintained ByteDance JSON files by glob.

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `scripts/scrape_campus_jobs.py` | Alibaba/Ant/Huawei scrapers plus combined export rebuild | Central batch-export entrypoint and combined schema owner |
| `scripts/scrape_bytedance_jobs.py` | Python Playwright ByteDance scraper | New primary path for ByteDance raw exports |
| `tests/test_scrape_campus_jobs.py` | Unit tests for normalization, pagination, export loading | Verifies multi-batch Ant and combined-export helper behavior |
| `tests/test_scrape_bytedance_jobs.py` | Unit test for ByteDance row normalization | Verifies new ByteDance Python scraper schema |
| `data/campus_positions_combined.json` | Latest combined export metadata and rows | Current snapshot is `1516` rows |
| `README.md` | Public-facing repo summary | Now reflects public-safe scope and current source counts |
| `.gitignore` | Public/private boundary | Ignores `resumes/`, `resume-refresh-*`, and local-only resume tooling |
| `.claude/handoffs/2026-03-22-022248-jd-shortlists-alibaba-ant-bytedance-top10.md` | Prior JD shortlist handoff | Useful if the next agent continues shortlist work rather than scraping |

### Key Patterns Discovered

- Raw exports are kept in `data/` as flat CSV/JSON with one shared schema.
- Curated notes and rankings are separate from raw site dumps; do not dump large raw pools into `catalog.csv`.
- ByteDance now uses a Python Playwright scraper because this environment already had Python Playwright available while the legacy Bun script lacked a local Node `playwright` package.
- Public/private separation matters in this repo. Resume sources stay local and ignored; only JD data, scripts, and public notes should be committed.

## Work Completed

### Tasks Finished

- [x] Added Ant Group batch `25051200066269` to the raw export layer.
- [x] Added ByteDance `DailyIntern + 后端` export support and generated a `210`-row snapshot.
- [x] Added Python ByteDance scraper and tests.
- [x] Rebuilt the combined export to include Alibaba, two Ant batches, two ByteDance pools, and Huawei (`1516` rows total).
- [x] Removed `resumes/` from the tracked tree and added ignore rules for private local resume material.
- [x] Rewrote Git history to remove `resumes/` from all commits.
- [x] Force-pushed rewritten history and changed the GitHub repo visibility to `PUBLIC`.

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `.gitignore` | Added ignore rules for `resumes/`, `resume-refresh-*`, and local-only resume tooling | Keep the repo publishable |
| `scripts/scrape_campus_jobs.py` | Added multi-batch Ant support, maintained-export ingestion, and updated combined export flow | Expand raw export coverage without manual merge steps |
| `scripts/scrape_bytedance_jobs.py` | Added new Python Playwright scraper | Replace environment-fragile Bun-only path with a working primary scraper |
| `tests/test_scrape_campus_jobs.py` | Added helper tests for Ant batch handling and maintained export loading | Keep combine logic verified |
| `tests/test_scrape_bytedance_jobs.py` | Added ByteDance normalization test | Verify new scraper output shape |
| `data/antgroup_positions_25051200066269.csv` | New Ant Group campus internship raw export | Capture new Ant source |
| `data/bytedance_positions_dailyintern_backend.csv` | New ByteDance daily internship backend raw export | Capture new ByteDance daily pool |
| `data/campus_positions_combined.csv` | Rebuilt combined export to `1516` rows | Keep all sources in one normalized file |
| `docs/companies/antgroup-campus-intern.md` | Added raw export note for Ant batch `25051200066269` | Document non-return-offer Ant internship pool |
| `docs/companies/bytedance-daily.md` | Added raw export note for ByteDance `DailyIntern` backend pool | Document new ByteDance daily source |
| `README.md` and `data/README.md` | Updated source counts, workflow, and public-scope wording | Align docs with current public repo state |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Use a Python Playwright ByteDance scraper as the primary path | Keep Bun script only, reverse-engineer pure HTTP immediately, or add Python Playwright | Python Playwright already worked in this environment and produced stable results without adding Node dependencies |
| Keep the current repo and rewrite history instead of creating a new public repo | Fresh public repo, or leave current repo private | User explicitly chose to rewrite the existing repo so the current GitHub location could become public |
| Remove only `resumes/` from history | Remove broader local-only files too | `resumes/` was the only tracked private path found in Git history; other resume-related files were untracked local artifacts |
| Preserve a local mirror backup before rewriting history | Rewrite with no backup, or rely on a tag only | A mirror backup outside the repo retains old objects safely in case recovery is ever needed |

## Pending Work

### Immediate Next Steps

1. Continue expanding raw exports to more big-tech companies if requested, following the same `data/` plus `docs/companies/` pattern.
2. Do a second-pass shortlist/ranking for the new Ant and ByteDance daily pools if the user wants a smaller application set.
3. Decide whether to keep or securely remove the local mirror backup that still contains old private resume history.

### Blockers/Open Questions

- [ ] Question: whether to extend the repo to Tencent, JD, Baidu, Meituan, or other companies next - Needs: user priority order
- [ ] Question: whether to refactor `catalog.csv` for the newer `武汉优先，但接受异地` location-priority logic - Needs: user confirmation that curation should be updated now

### Deferred Items

- Catalog/location-priority refactor was deferred because this session focused on public-safe history cleanup and export expansion first.
- The legacy Bun ByteDance scraper was left in place as a fallback, but the Python scraper is now the primary path.

## Context for Resuming Agent

### Important Context

The repo is now publicly reachable at `https://github.com/LouisLau-art/internship-jd-catalog`. The rewritten public branch head is `8c0f4cd`. `git log --all -- resumes` returns nothing, so `resumes/` is gone from visible history. A local mirror backup still exists at `/home/louis/internship-jd-catalog-history-backup-20260322-470004.git`; that backup contains the pre-rewrite private history and must never be pushed or published. The current combined export metadata is in `data/campus_positions_combined.json` with `generated_at = 2026-03-21T05:35:45.762839+00:00` and `1516` total rows. Source totals are Alibaba `455 + 72`, Ant Group `96 + 45`, ByteDance `558 + 210`, and Huawei `80`.

### Assumptions Made

- The user wanted the current GitHub repo made public, not a new separate public repo.
- Removing `resumes/` from tracked history was sufficient for the privacy requirement because that was the tracked private path found in history.
- The local mirror backup should remain for now unless the user explicitly asks to delete it.

### Potential Gotchas

- `git-filter-repo` removes the `origin` remote as a safety measure. It has already been re-added and `main` is again tracking `origin/main`.
- Future history rewrites on this repo will require another explicit force-push flow.
- The local backup repo still contains private data. Treat `/home/louis/internship-jd-catalog-history-backup-20260322-470004.git` as sensitive.
- Local ignored files like `resume-refresh-*`, `GEMINI.md`, and ignored resume scripts may still exist on disk even though they are not tracked.

## Environment State

### Tools/Services Used

- `git-filter-repo`: used to rewrite history and remove `resumes/`
- `gh`: used to inspect repo visibility and change the repo to `PUBLIC`
- Python `unittest`: used for verification
- Python `playwright`: used by `scripts/scrape_bytedance_jobs.py`

### Active Processes

- None

### Environment Variables

- No special project-specific environment variables were required for the completed work

## Related Resources

- `README.md`
- `data/README.md`
- `scripts/scrape_campus_jobs.py`
- `scripts/scrape_bytedance_jobs.py`
- `tests/test_scrape_campus_jobs.py`
- `tests/test_scrape_bytedance_jobs.py`
- `.claude/handoffs/2026-03-22-022248-jd-shortlists-alibaba-ant-bytedance-top10.md`
- Local backup: `/home/louis/internship-jd-catalog-history-backup-20260322-470004.git`

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
