---
name: job-fit-to-resume
description: Use when ranking the best roles from refreshed company exports, deciding which targeted resumes to reuse or generate, or syncing shortlist decisions back to the main dashboard.
---

# Job Fit To Resume

## Overview
This is the second half of the workflow. It reads refreshed company exports, picks the best roles, checks resume coverage, optionally generates missing PDFs, and syncs the main notebook.

## When to Use
- You already refreshed raw exports and now need a per-company shortlist.
- You want to know which targeted PDFs already exist and which ones should be generated next.
- The dashboard and `resumes/sources/` may have drifted out of sync.

## `/job-fit-to-resume`

1. Run the orchestrator:
   `python scripts/run_job_fit_resume.py --companies alibaba,antgroup,bytedance,meituan,jd,tencent,xiaohongshu,huawei --top-n-per-company 3`
2. 默认每家公司推荐 3 个左右最适合岗位，并把 shortlists 写到 `docs/temp/*job-fit-shortlist.md`。
3. Keep `--generate` on when you want missing company PDFs exported automatically; use `--no-generate` for a dry ranking pass.
4. Keep `--sync-progress` on when you want `docs/job-search-progress.md` updated together with the shortlist.
5. If the target is a high-end AI role such as Seed / MiMo / AI PaaS, pivot into `resumes/scripts/ai-native-resume-generation/SKILL.md` before rewriting bullets by hand.

## Common Mistakes
- Treating `docs/job-search-progress.md` as source of truth when refreshed `data/` exports are newer.
- Generating a fresh resume before checking whether the orchestrator already mapped a reusable same-company PDF.
- Mixing scrape and shortlist responsibilities instead of running `/campus-job-scrape` first.

## Real-World Impact
This keeps the “抓岗 -> 选岗 -> 生成/复用简历 -> 回写看板” flow reusable instead of depending on session memory.
