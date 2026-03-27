# `/sync-jobs` Automated Job Search Sync System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Automate the extraction of interview notifications from QQ Mail and sync them to the Markdown dashboard.

**Architecture:** A lightweight Python engine fetches recent email headers via IMAP, performs local regex auditing to bypass encoding issues, and outputs a JSON of detected events for Markdown synchronization.

**Tech Stack:** Python 3.x (imaplib, email, re), Markdown.

---

### Task 1: Refactor Email Engine for Local Header Audit

**Files:**
- Modify: `scripts/parse_qq_job_emails.py`

**Step 1: Replace server-side `SEARCH` with `FETCH` metadata**
Rewrite the search logic to retrieve headers for the most recent 100 emails and audit them locally using Regex.

```python
# In scripts/parse_qq_job_emails.py
def fetch_and_audit_locally(mail, limit=100):
    # Get total count
    status, response = mail.select("INBOX")
    total = int(response[0])
    start = max(1, total - limit + 1)
    
    # Fetch headers only
    status, data = mail.fetch(f"{start}:{total}", "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
    # ... Local regex audit loop ...
```

**Step 2: Implement Natural Language Time Extraction**
Enhance regex patterns to handle "Tomorrow 2PM" or "March 27th" in Chinese.

**Step 3: Test parsing with dummy header strings**
Ensure the regex correctly identifies "字节跳动" and "面试邀请".

**Step 4: Commit refactor**
```bash
git add scripts/parse_qq_job_emails.py
git commit -m "refactor(mail): implement local-first header audit engine"
```

---

### Task 2: Robust MD Table Synchronization

**Files:**
- Create: `scripts/sync_md_dashboard.py`
- Modify: `docs/job-search-progress.md`

**Step 1: Write de-duplication logic**
Ensure that emails with the same `Subject` and `Date` aren't added twice to the Markdown table.

**Step 2: Implement surgical `replace` for MD tables**
Locate the `## ✅ 已投递岗位` or `## 📋 面试记录` section and insert new rows formatted as Markdown table rows.

**Step 3: Commit sync script**
```bash
git add scripts/sync_md_dashboard.py
git commit -m "feat(sync): add markdown dashboard synchronization logic"
```

---

### Task 3: Command Wrapping & Workflow Integration

**Files:**
- Modify: `CLAUDE.md`
- Create: `.claude/skills/job-sync/SKILL.md`

**Step 1: Create the `/sync-jobs` Custom Skill**
Define the skill that checks for `.env`, runs the engine, and then triggers the MD sync.

**Step 2: Update `CLAUDE.md` Common Commands**
Add the new sync command to the documentation.

**Step 3: Final End-to-End Verification**
Run `/sync-jobs` and verify `docs/job-search-progress.md` is updated correctly.

**Step 4: Commit final workflow**
```bash
git add .claude/skills/job-sync/SKILL.md CLAUDE.md
git commit -m "feat(workflow): wrap job sync into a reusable custom skill"
```
