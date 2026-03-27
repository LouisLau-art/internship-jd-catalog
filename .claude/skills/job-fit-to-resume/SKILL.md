---
name: job-fit-to-resume
description: Use when reviewing suitable internship roles, checking whether matching resumes already exist, or deciding which resume to reuse or generate next.
---

# Job Fit To Resume

## Overview
Use one entrypoint to answer three questions in order: which roles are worth pursuing, which of them already have usable resume coverage, and which ones should be generated next.

## When to Use
- You want to know whether current `strong` / `very strong` / targeted roles already have resumes.
- The dashboard and `resumes/sources/` may have drifted out of sync.
- You need a shortlist of gaps before generating new resumes.

## `/job-fit-to-resume`

1. Run the coverage audit and sync the dashboard:
   `python scripts/audit_resume_coverage.py --sync-doc docs/job-search-progress.md`
2. Read the statuses:
   - `generated`: matching PDF already exists in `resumes/sources/`
   - `generator_ready`: a generator script exists, but the PDF has not been exported yet
   - `reusable`: reuse the closest existing targeted resume, then do small role-specific edits
   - `missing`: no same-company template exists yet
3. If the target is a high-end AI role such as Seed / MiMo / AI PaaS, pivot into `resumes/scripts/ai-native-resume-generation/SKILL.md` to mine handoff evidence before rewriting bullets.
4. If the role is company-specific and a generator already exists, run the matched `resumes/scripts/generate_*_resumes.py` script instead of drafting from scratch.

## Common Mistakes
- Treating `docs/job-search-progress.md` as source of truth when `resumes/sources/` already has newer artifacts.
- Generating a fresh resume before checking whether a same-company version is already reusable.
- Using the deep-diver AI-native workflow for generic backend roles that only need a light adaptation.

## Real-World Impact
This keeps the “找岗 -> 查覆盖 -> 生成/复用简历 -> 回写看板” flow skillized instead of depending on session memory.
