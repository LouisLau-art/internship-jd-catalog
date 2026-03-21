# Public Repo And Daily Intern Sources Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the repository safe to publish in its current snapshot, add the new Ant Group and ByteDance daily internship sources, and regenerate the combined raw export.

**Architecture:** Split the repository into a committed public scraping/data layer and a local-only resume layer. Extend the existing campus export pipeline so Python owns Alibaba, Ant Group, Huawei, and final combination, while the Bun scraper continues to collect parameterized ByteDance raw exports that the Python combiner can ingest from `data/`.

**Tech Stack:** Python 3 stdlib, Bun, Playwright, Git, CSV/JSON flat files

---

### Task 1: Add privacy boundary files

**Files:**
- Create: `docs/plans/2026-03-21-public-repo-and-daily-intern-design.md`
- Modify: `.gitignore`

**Step 1: Add ignore rules**

Update `.gitignore` to ignore:

- `resumes/`
- `resume-refresh-*/`
- other local resume bundle files that should never enter Git again

**Step 2: Review tracked resume files**

Run: `git ls-files | rg '(^resumes/|resume-refresh-|刘新宇|resume)'`

Expected: tracked private files are identified before untracking.

**Step 3: Untrack private resume files**

Run cached deletes so files remain local:

```bash
git rm --cached -r resumes resume-refresh-20260319
```

Expected: Git stages removals, but local files still exist on disk.

### Task 2: Extend Ant Group batch coverage

**Files:**
- Modify: `scripts/scrape_campus_jobs.py`
- Modify: `tests/test_scrape_campus_jobs.py`

**Step 1: Write failing test**

Add tests for any new helper that builds combined source metadata or loads maintained raw exports.

**Step 2: Implement Ant batch list support**

Replace the single Ant batch flow with a list-driven flow that can export:

- `26022600074513`
- `25051200066269`

Each batch should still write its own CSV/JSON file.

**Step 3: Regenerate combined source metadata**

Ensure combined JSON records both Ant batches distinctly.

### Task 3: Integrate maintained ByteDance exports into combine flow

**Files:**
- Modify: `scripts/scrape_campus_jobs.py`
- Modify: `tests/test_scrape_campus_jobs.py`

**Step 1: Write failing test**

Add a test for loading an existing raw export JSON file from `data/` and returning normalized job rows plus metadata.

**Step 2: Implement raw export ingestion**

Teach the Python combine step to read maintained export JSON files from `data/`, starting with ByteDance raw exports.

**Step 3: Keep schema stable**

The resulting combined CSV/JSON must preserve the existing flat schema.

### Task 4: Export the new ByteDance daily internship backend pool

**Files:**
- Modify: `README.md`
- Modify: `data/README.md`
- Create: `docs/companies/bytedance-daily.md`
- Create: `data/bytedance_positions_dailyintern_backend.csv`
- Create: `data/bytedance_positions_dailyintern_backend.json`

**Step 1: Run the parameterized scraper**

Run:

```bash
bun scripts/scrape_bytedance_jobs.js \
  --project-id 7194661644654577981 \
  --project-slug dailyintern \
  --project-name DailyIntern \
  --category-id 6704215862557018372 \
  --category-slug backend \
  --category-name 后端 \
  --list-url 'https://jobs.bytedance.com/campus/position?keywords=&category=6704215862557018372&location=&project=7194661644654577981&type=&job_hot_flag=&current=1&limit=10&functionCategory=&tag='
```

Expected: `data/bytedance_positions_dailyintern_backend.csv` and `.json` are written.

**Step 2: Add company note**

Create a short note in `docs/companies/bytedance-daily.md` summarizing the snapshot.

### Task 5: Refresh public docs and outputs

**Files:**
- Modify: `README.md`
- Modify: `data/README.md`
- Modify: `data/campus_positions_combined.csv`
- Modify: `data/campus_positions_combined.json`

**Step 1: Run export refresh**

Run:

```bash
python scripts/scrape_campus_jobs.py
```

Expected: Alibaba, Ant Group, Huawei, and combined exports refresh.

**Step 2: Verify counts**

Inspect generated files and confirm the new Ant batch and ByteDance daily pool are represented in docs and combined output.

### Task 6: Verify, commit, and push

**Files:**
- Modify: Git index state for all public changes

**Step 1: Run tests**

Run:

```bash
python -m unittest tests.test_scrape_campus_jobs
```

Expected: PASS.

**Step 2: Review git status**

Run: `git status --short --branch`

Expected: only intended public files remain staged or modified.

**Step 3: Commit**

```bash
git add .gitignore README.md data docs scripts tests
git commit -m "feat: expand internship exports and remove private resume files"
```

**Step 4: Push**

```bash
git push origin main
```
