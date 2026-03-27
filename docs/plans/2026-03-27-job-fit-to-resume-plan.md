# `job-fit-to-resume` Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a reusable in-repo skill that audits suitable roles against resume coverage, recommends reuse or generation paths, and syncs the job-progress document to real workspace assets.

**Architecture:** A Python audit script parses recommended/applied roles from the Markdown dashboard, inspects `resumes/scripts/generate_*` registries plus `resumes/sources/` artifacts, classifies each target as generated, generator-ready, reusable, or missing, and then rewrites the resume coverage sections in `docs/job-search-progress.md`. A custom skill wraps this workflow and points high-end AI roles to the existing deep-diver resume skill.

**Tech Stack:** Python 3.x (`ast`, `dataclasses`, `pathlib`, `re`, `difflib`), Markdown, Claude custom skills.

---

### Task 1: Add failing coverage-audit tests

**Files:**
- Create: `tests/test_audit_resume_coverage.py`

**Step 1: Write the failing tests**
Cover generator parsing, target classification, and Markdown section syncing.

**Step 2: Run test to verify it fails**
Run: `python -m pytest tests/test_audit_resume_coverage.py -q`
Expected: import or missing-function failure before implementation exists.

### Task 2: Implement the coverage audit engine

**Files:**
- Create: `scripts/audit_resume_coverage.py`

**Step 1: Parse generator registries**
Load `RESUMES` literals from `resumes/scripts/generate_*_resumes.py` and tailored generators.

**Step 2: Parse target roles from the dashboard**
Read `docs/job-search-progress.md` and extract applied + recommended suitable roles.

**Step 3: Classify coverage**
Mark each target as `generated`, `generator_ready`, `reusable`, or `missing`.

**Step 4: Sync Markdown sections**
Rewrite `### 已生成的定向简历` and `### 待生成简历` from the computed coverage.

**Step 5: Run tests to verify green**
Run: `python -m pytest tests/test_audit_resume_coverage.py -q`

### Task 3: Wrap the workflow as a custom skill

**Files:**
- Create: `.claude/skills/job-fit-to-resume/SKILL.md`
- Modify: `CLAUDE.md`

**Step 1: Add the orchestration skill**
Document the audit command, review steps, and when to branch into `ai-native-resume-generation`.

**Step 2: Advertise the new entrypoint**
Add `/job-fit-to-resume` to `CLAUDE.md` common commands/workflow guidance.

### Task 4: Sync the live dashboard and verify

**Files:**
- Modify: `docs/job-search-progress.md`

**Step 1: Run the audit script with doc sync enabled**
Run: `python scripts/audit_resume_coverage.py --sync-doc docs/job-search-progress.md`

**Step 2: Verify updated sections**
Confirm generated/pending tables match actual `resumes/sources/` assets and script readiness.

**Step 3: Run focused regression checks**
Run: `python -m pytest tests/test_audit_resume_coverage.py tests/test_sync_md_dashboard.py -q`
