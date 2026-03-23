# Handoff: Meituan & JD Scrape and Resume Deep Customization

## Session Metadata
- Created: 2026-03-24 04:29:33
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: ~1 hour

### Recent Commits (for context)
  - 882d8de feat(jd): add meituan and jd scrapers, data, and shortlists
  - 0e282ff docs(jd): add expanded alibaba ant and bytedance top-10 shortlists
  - 8c0f4cd feat(repo): expand internship exports and remove private resumes
  - fc4ad41 feat(jd): add bytedance byteintern backend export
  - 49a6a04 feat(jd): expand campus exports and add daily shortlist

## Handoff Chain

- **Continues from**: [2026-03-24-014749-firecrawl-cli-migration-and-internship-jd-catalog-config.md](./2026-03-24-014749-firecrawl-cli-migration-and-internship-jd-catalog-config.md)
  - Previous title: Firecrawl CLI 迁移至 Bun + 完整 AI CLI 工具链配置
- **Supersedes**: None

## Current State Summary

This session focused on expanding the internship JD catalog to include Meituan and JD. We successfully discovered their API endpoints, wrote a scraper, and integrated the data into the combined catalog. We also generated deep-customized resumes for the top recommended roles in Alibaba, Ant Group, ByteDance, Meituan, and JD, focusing on AI Agent and engineering efficiency themes. The repo is clean, pushed to origin/main, and all generated assets are exported to the user's local Downloads folder.

## Codebase Understanding

### Architecture Overview

The repository follows a clear data pipeline:
1.  **Scraping**: Company-specific scripts in `scripts/` (e.g., `scrape_meituan_jd.py`) fetch raw JSON/CSV data.
2.  **Normalization**: Data is normalized to a common schema.
3.  **Combination**: `scripts/scrape_campus_jobs.py` acts as the central orchestrator to merge all sources into `data/campus_positions_combined.json`.
4.  **Curation**: Human-reviewed shortlists and company notes live in `docs/`.
5.  **Generation**: Resume scripts in `resumes/sources/` use `generate_xhs_resumes.py` as a base to render customized PDFs/DOCXs.

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `scripts/scrape_meituan_jd.py` | New scraper for Meituan and JD APIs | Source of new data |
| `scripts/scrape_campus_jobs.py` | Central merging and combined export logic | Updated to include Meituan/JD |
| `docs/meituan-jd-top-5.md` | Reviewed shortlist for Meituan and JD | Prioritization for new roles |
| `resumes/sources/generate_bytedance_resumes.py` | New resume generation script | Tailored for ByteDance roles |
| `resumes/sources/generate_meituan_resumes.py` | New resume generation script | Tailored for Meituan roles |
| `resumes/sources/generate_jd_resumes.py` | New resume generation script | Tailored for JD roles |

### Key Patterns Discovered

- **API-First Scraping**: Most job boards have internal POST APIs that can be reached with standard `urllib` if correct headers (User-Agent, Origin, Referer) are provided.
- **Base-Template Resume Pattern**: All resume scripts import `base` (generate_xhs_resumes) to reuse rendering and export logic.
- **Evidence-Driven Tailoring**: Resumes are customized by updating the `summary`, `signals`, and `experience` bullets to match specific JD requirements while staying grounded in real projects like `ScholarFlow`.

## Work Completed

### Tasks Finished

- [x] Researched GitHub for LLM/Backend internship experiences (e.g., `jingtian11/EasyOffer`).
- [x] Scraped 70 Meituan and 81 JD internship positions.
- [x] Integrated Meituan and JD data into the combined catalog (total count: 1667).
- [x] Created `docs/meituan-jd-top-5.md` shortlist.
- [x] Generated deep-customized resumes for:
    - Alibaba (AI Agent)
    - Ant Group (Smart Collab, OceanBase AI)
    - ByteDance (AI Agent Backend, Dev Agent)
    - Meituan (Eng Infra, AI Coding)
    - JD (AI Innovation)
- [x] Exported all assets to `/home/louis/Downloads/resume-refresh-20260319/`.
- [x] Pushed all changes to `origin/main`.

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `scripts/scrape_campus_jobs.py` | Added Meituan/JD merging logic | Support new sources |
| `resumes/sources/generate_alibaba_resumes.py` | Added AI Agent resume | Customize for target role |
| `resumes/sources/generate_antgroup_resumes.py` | Added Smart Collab and OceanBase resumes | Customize for target roles |
| `README.md` | Updated counts and source list | Keep overview current |

## Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Prioritize Meituan "AI Coding" and "Eng Infra" | General Backend | These roles perfectly match Louis's unique strengths in MCP/Skills/CLI Agents. |
| Use `urllib` for Meituan/JD | Playwright | API endpoints were discovered and accessible via pure HTTP, which is faster and lighter. |
| Export resumes to Downloads | Stay in repo | The repo is public; private resume data must stay out of Git history. |

## Pending Work

### Immediate Next Steps

1. **Submit Applications**: Prioritize Meituan (AI Coding), ByteDance (AI Agent), and OceanBase.
2. **Interview Prep**: Study the `jingtian11/EasyOffer` repository for LLM-specific interview questions.
3. **Internal Referral**: Search for contacts at Meituan and ByteDance to increase hit rates.

### Blockers/Open Questions

- [ ] None currently. All technical tasks completed.

### Deferred Items

- Expansion to NetEase/PDD/Baidu (pending user request).

## Context for Resuming Agent

### Important Context

- **The environment has Playwright**, but use it only when pure HTTP/API requests fail.
- **The `agent-browser` skill** requires being in a `gemini` session; it is not a system command.
- **Check `.claude/handoffs/`** for the full chain of context.
- **Louis's "Unique Selling Point"**: The combination of robust Backend Engineering (FastAPI/Spring Boot) + cutting-edge AI Agent Orchestration (MCP/Skills/Context7). Focus on this in all future tailoring.

### Assumptions Made

- The user wants the public repo to be a "JD Catalog" and "Strategy Hub" while keeping private resume data in local/ignored folders.

### Potential Gotchas

- When adding new companies to `scrape_campus_jobs.py`, ensure the JSON snapshot contains a `"jobs"` list, as `load_maintained_exports` expects this key.

## Environment State

### Tools/Services Used

- `Python 3`
- `Pandoc` (for DOCX generation)
- `Google Chrome` (headless for PDF generation)
- `Git`

### Active Processes

- None.

### Environment Variables

- None required for current scripts.

## Related Resources

- [jingtian11/EasyOffer](https://github.com/jingtian11/EasyOffer)
- `docs/meituan-jd-top-5.md`
- `data/campus_positions_combined.json`

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
