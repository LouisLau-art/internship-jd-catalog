# Handoff: Alibaba Ant ByteDance Top-10 JD Shortlists

## Session Metadata
- Created: 2026-03-22 02:22:48
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: ~1 hour

### Recent Commits (for context)
  - 0e282ff docs(jd): add expanded alibaba ant and bytedance top-10 shortlists
  - 8c0f4cd feat(repo): expand internship exports and remove private resumes
  - fc4ad41 feat(jd): add bytedance byteintern backend export
  - 49a6a04 feat(jd): expand campus exports and add daily shortlist
  - 38cee8e docs(jd): split alibaba and ant shortlists

## Handoff Chain

- **Continues from**: None (fresh start)
- **Supersedes**: None

> This is the first handoff for this task.

## Current State Summary

This session focused only on `/home/louis/internship-jd-catalog` and specifically on ranking the most suitable internship roles for Louis across Alibaba, Ant Group, and ByteDance based on the current raw export pools. The immediate milestone is complete: the repo now contains refreshed top-10 shortlist docs for all three companies, the README links were verified, and the changes were committed and pushed to `origin/main` at `0e282ff`. The next session should not redo scraping first; it should use the current shortlist docs to decide which `2-3` roles per company deserve tailored resumes and application sequencing.

## Codebase Understanding

### Architecture Overview

This repo has a clear two-layer structure. `data/` is the raw export layer and is allowed to be large; it stores CSV/JSON dumps from site scrapers for Alibaba, Ant Group, ByteDance, and others. `docs/` is the reviewed layer: company notes, shortlist docs, and apply-order reasoning. `catalog.csv` stays relatively small and curated instead of absorbing every raw export row. Resume artifacts are intentionally not tracked here; the repo is meant to stay publishable. For ByteDance specifically, raw export generation is more fragile than the others because it depends on browser-bootstrapped cookies and CSRF; the shortlist docs should be treated as downstream outputs of those exports, not hand-maintained truth detached from `data/`.

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| [README.md](/home/louis/internship-jd-catalog/README.md) | Repo overview and pointers to current shortlist docs and raw exports | First file a resuming agent should sanity-check before making new ranking claims |
| [alibaba-top-10.md](/home/louis/internship-jd-catalog/docs/alibaba-top-10.md) | Reviewed Alibaba top-10 shortlist | Captures the latest prioritized ranking across Alibaba batch and daily internship pools |
| [antgroup-top-10.md](/home/louis/internship-jd-catalog/docs/antgroup-top-10.md) | Reviewed Ant Group top-10 shortlist | Captures the latest prioritized ranking across Ant transfer-offer and daily internship pools |
| [bytedance-top-10.md](/home/louis/internship-jd-catalog/docs/bytedance-top-10.md) | Reviewed ByteDance top-10 shortlist | Captures the latest prioritized ranking across ByteIntern and DailyIntern backend pools |
| [bytedance_positions_byteintern_backend.csv](/home/louis/internship-jd-catalog/data/bytedance_positions_byteintern_backend.csv) | Raw ByteDance ByteIntern backend export | Main upstream dataset behind the current ByteDance shortlist |
| [bytedance_positions_dailyintern_backend.csv](/home/louis/internship-jd-catalog/data/bytedance_positions_dailyintern_backend.csv) | Raw ByteDance DailyIntern backend export | Needed to justify the DailyIntern fallback roles in the shortlist |
| [alibaba_positions_100000540002.csv](/home/louis/internship-jd-catalog/data/alibaba_positions_100000540002.csv) | Raw Alibaba 2027 internship export | Main upstream dataset behind the current Alibaba shortlist |
| [alibaba_positions_100000560002_tech.csv](/home/louis/internship-jd-catalog/data/alibaba_positions_100000560002_tech.csv) | Raw Alibaba daily internship tech export | Needed for daily-role fallback ranking |
| [antgroup_positions_26022600074513.csv](/home/louis/internship-jd-catalog/data/antgroup_positions_26022600074513.csv) | Raw Ant transfer-offer internship export | Main upstream dataset behind the current Ant shortlist |
| [antgroup_positions_25051200066269.csv](/home/louis/internship-jd-catalog/data/antgroup_positions_25051200066269.csv) | Raw Ant daily internship export | Important because README wording was corrected based on this CSV's actual `batch_name` |

### Key Patterns Discovered

- Treat raw export files as source-of-truth for counts and batch naming; do not rely on older prose summaries if CSV says otherwise.
- Keep `data/` and `docs/` separate. Large dumps belong in `data/`; reviewed top lists and fit judgments belong in `docs/`.
- Rank by honest fit to Louis's current evidence base, not by prestige or by the most AI-sounding title.
- When a company has both conversion-oriented and daily tracks, prefer the conversion track only when fit is close. Do not force a weaker batch role above a much better daily role.
- De-duplicate location clones conceptually when ranking; the shortlist should be about role families, not city-count inflation.

## Work Completed

### Tasks Finished

- [x] Re-verified the current raw export coverage for Alibaba, Ant Group, and ByteDance from files on disk instead of relying on earlier summaries
- [x] Used parallel subagents to independently rank Alibaba, Ant Group, and ByteDance roles against Louis's real evidence base
- [x] Rewrote [alibaba-top-10.md](/home/louis/internship-jd-catalog/docs/alibaba-top-10.md) using the stronger subagent ranking
- [x] Rewrote [antgroup-top-10.md](/home/louis/internship-jd-catalog/docs/antgroup-top-10.md) using the stronger subagent ranking
- [x] Rewrote [bytedance-top-10.md](/home/louis/internship-jd-catalog/docs/bytedance-top-10.md) using the stronger subagent ranking
- [x] Corrected README wording so the Ant `25051200066269` batch is described as `日常实习`
- [x] Verified README links and committed/pushed the shortlist changes

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| [README.md](/home/louis/internship-jd-catalog/README.md) | Corrected Ant daily-batch wording and retained links to top-10 docs | Prevent stale wording from confusing future ranking work |
| [alibaba-top-10.md](/home/louis/internship-jd-catalog/docs/alibaba-top-10.md) | Replaced rough local draft with refined top-10 ranking | Align final shortlist with stronger company-specific ranking logic |
| [antgroup-top-10.md](/home/louis/internship-jd-catalog/docs/antgroup-top-10.md) | Replaced rough local draft with refined top-10 ranking | Capture the strongest Ant-fit roles without mixing algorithm-heavy stretches too high |
| [bytedance-top-10.md](/home/louis/internship-jd-catalog/docs/bytedance-top-10.md) | Replaced earlier draft with de-duplicated and stronger ByteDance ranking | Shifted ByteDance ordering toward the clearest agent/backend/dev-tooling fits |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Keep the work in one narrow session scope | Also continue resumes or re-run scrapes in the same session | The user explicitly wanted unrelated tracks split; this pass only handled shortlist governance in `internship-jd-catalog` |
| Treat Ant `25051200066269` as `日常实习` in repo prose | Keep older “campus internship batch” wording | The CSV's actual `batch_name` is `日常实习`, so the older wording was less precise |
| Prefer fit-driven ranking over batch prestige | Always place transfer-offer roles above daily roles | Some daily roles, especially OceanBase-AI平台研发实习生, fit Louis better than weaker conversion-track roles |
| Use current raw export files as ranking anchors | Rank from memory, old notes, or title vibe alone | This avoids drift and makes the shortlist defensible |
| Push the shortlist docs immediately after verification | Leave docs only locally | This repo is the persistent public-ish strategy source, so the shortlist should live in git once verified |

## Pending Work

### Immediate Next Steps

1. Use the three top-10 docs to choose the next `2-3` roles that should get tailored resumes first.
2. Generate or refine targeted resumes in the private/workbench path rather than committing resume artifacts back into this public repo.
3. Only re-run scrapers if a company's site visibly changes or if the current exports become stale enough to invalidate the shortlist.

### Blockers/Open Questions

- [ ] Open question: whether the next session should prioritize ByteDance tailored resumes first or continue expanding Alibaba/Ant tailored variants.
- [ ] Open question: whether a cross-company `top picks for immediate application` doc should be added, or whether the existing company-specific top-10 docs are enough.

### Deferred Items

- Tailored resumes for the newly ranked Alibaba / Ant / ByteDance roles were deferred because this session only handled shortlist curation.
- Any additional scraping beyond the current export pool was deferred because current raw data is already sufficient for ranking.
- Broader cross-company shortlist consolidation was deferred to keep this session single-purpose.

## Context for Resuming Agent

### Important Context

The key milestone is already complete: the repo now has pushed top-10 shortlists for Alibaba, Ant Group, and ByteDance, and those rankings are not the original rough drafts anymore. They were rewritten using stronger company-specific ranking passes, including parallel subagent results for Alibaba, ByteDance, and Ant. The repo is clean, on `main`, and the latest commit is `0e282ff`. Do not re-summarize old state from memory; read the three top-10 docs and the raw CSVs they cite. Also keep the privacy boundary intact: this repo stays publishable, so resumes, contact info, and photos belong in the private resume workbench, not back in this repo. If resuming, the highest-value move is not more scraping but converting the current shortlists into application actions and targeted resumes.

### Assumptions Made

- Louis's current strongest honest story is still backend/full-stack delivery, AI application engineering, agent workflows, MCP/Skills tooling, observability/debugging, and product-to-delivery execution.
- Current raw export files are recent enough for shortlist work; no immediate refresh is needed before choosing next applications.
- This repo should remain publishable, so shortlist docs are safe to push but resume artifacts are not.

### Potential Gotchas

- Do not confuse “campus internship” wording in older prose with the Ant CSV's real `batch_name`; for `25051200066269`, the data says `日常实习`.
- Do not let title prestige override fit. Several algorithm-, infra-, and pretraining-heavy roles sound attractive but are weaker honest matches.
- ByteDance roles often appear as multiple city clones; ranking should be by role family, not by raw row count.
- If you regenerate ByteDance exports later, remember that their scrape path is more brittle than Alibaba/Ant and depends on browser-derived auth state.

## Environment State

### Tools/Services Used

- `python` for repo inspection, CSV sanity checks, and handoff tooling
- `git` for status, commit, and push
- session-handoff skill scripts from `/home/louis/.codex/skills/session-handoff/scripts/`
- parallel subagents for company-specific shortlist ranking

### Active Processes

- None left running intentionally at handoff time

### Environment Variables

- `NODE_PATH` may matter if ByteDance scraping is rerun with the Bun/legacy toolchain, but it was not required for this handoff itself

## Related Resources

- [README.md](/home/louis/internship-jd-catalog/README.md)
- [alibaba-top-10.md](/home/louis/internship-jd-catalog/docs/alibaba-top-10.md)
- [antgroup-top-10.md](/home/louis/internship-jd-catalog/docs/antgroup-top-10.md)
- [bytedance-top-10.md](/home/louis/internship-jd-catalog/docs/bytedance-top-10.md)
- [alibaba-top-5.md](/home/louis/internship-jd-catalog/docs/alibaba-top-5.md)
- [antgroup-top-5.md](/home/louis/internship-jd-catalog/docs/antgroup-top-5.md)
- [data/README.md](/home/louis/internship-jd-catalog/data/README.md)
- [scrape_campus_jobs.py](/home/louis/internship-jd-catalog/scripts/scrape_campus_jobs.py)
- [scrape_bytedance_jobs.py](/home/louis/internship-jd-catalog/scripts/scrape_bytedance_jobs.py)

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
