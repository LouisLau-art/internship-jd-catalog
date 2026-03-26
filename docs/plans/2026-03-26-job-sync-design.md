# Design Doc: `/sync-jobs` Automated Job Search Sync System

**Date**: 2026-03-26
**Status**: Approved
**Topic**: Automation of interview invitation syncing from QQ Mail to Markdown tracking.

## 1. Overview
The system provides a unified command `/sync-jobs` to automatically fetch job-related notifications (interviews, assessments, offers) from the user's QQ Mail and synchronize them with the project's central tracking document `docs/job-search-progress.md`.

## 2. Architecture: Local-First Audit Engine
To resolve previous IMAP `SEARCH` failures caused by Chinese character encoding issues on the server side, this system shifts the logic to a local Python audit engine.

### 2.1 Component: Python Engine (`scripts/parse_qq_job_emails.py`)
- **Transport**: IMAP4 over SSL (`imap.qq.com:993`).
- **Phase 1: Metadata Fetch**: Use `FETCH 1:* (BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])` to retrieve metadata for the most recent 100 emails without marking them as read.
- **Phase 2: Local Regex Audit**: Scan headers against a high-precision keyword list:
    - **Domains**: `bytedance.com`, `mi.com`, `meituan.com`, etc.
    - **Actions**: `面试`, `笔试`, `测评`, `录取`, `Offer`.
- **Phase 3: Targeted Retrieval**: Only perform `FETCH (RFC822)` for emails matching Phase 2 criteria to extract body content and parse interview timestamps/locations.

### 2.2 Component: Security Layer (`.env`)
- Credentials (`QQ_EMAIL`, `QQ_AUTH_CODE`) are stored in a root-level `.env` file.
- **Strict Constraint**: `.env` MUST be added to `.gitignore` to prevent accidental commits to public repositories.

### 2.3 Component: Custom Skill (`job-sync`)
- Wraps the Python engine into a single command `/sync-jobs`.
- Responsible for cross-referencing `docs/job-search-progress.md` to prevent duplicate entries based on `Message-ID` or `(Subject + Date)` unique keys.

## 3. Data Flow
1. User runs `/sync-jobs`.
2. Skill validates `.env` existence.
3. Python script audits mail headers and outputs `data/detected_job_events.json`.
4. Skill parses JSON and identifies "New" vs "Existing" events.
5. Skill performs surgical update to `docs/job-search-progress.md` using the `replace` tool.

## 4. Success Criteria
- [ ] No encoding errors during Chinese character searches.
- [ ] Successful extraction of interview dates/times from email bodies.
- [ ] Automatic, duplicate-free updates to the Markdown dashboard.
- [ ] Zero leakage of credentials to Git history.
