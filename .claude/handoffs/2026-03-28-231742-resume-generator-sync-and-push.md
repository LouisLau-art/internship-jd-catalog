# Handoff: 阿里/蚂蚁/小红书生成器同步收口与安全分支推送

## Session Metadata
- Created: 2026-03-28 23:17:42
- Project: /home/louis/internship-jd-catalog
- Branch: codex/resume-generator-sync
- Session duration: 约 1.5 小时

### Recent Commits (for context)
  - cba90e3 fix(resume): track generator sources and sync tailored drafts
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic

## Handoff Chain

- **Continues from**: [2026-03-28-113912-exam-prep-resume-refresh.md](./2026-03-28-113912-exam-prep-resume-refresh.md)
  - Previous title: 阿里/蚂蚁/小红书笔试辅导与定制简历-PDF刷新
- **Supersedes**: None

## Current State Summary

上一份 handoff 留下的核心风险是：阿里、蚂蚁、小红书三份定制简历虽然已经有最新活动稿和 PDF，但对应 `generate_*_resumes.py` 的内嵌数据层没有完全同步，直接重跑生成脚本可能把新版内容冲回旧版。这一轮已经把三份生成器数据补齐，并进一步发现真正的深层漂移点不只在 `RESUMES` 数据，而在共享渲染器 `generate_xhs_resumes.py` 会无条件调用 `normalize_projects()`，把手工调整过的项目顺序重新标准化。我为三份定制稿增加了 `preserve_projects` 保护分支，新增了渲染结果对比当前活动稿的回归测试，并将最小可运行的生成器链路以 commit `cba90e3` 推到远端分支 `codex/resume-generator-sync`。本轮没有重跑 PDF 导出，但现在这三份脚本可以安全重跑。

## Codebase Understanding

### Architecture Overview

本仓库的定制简历生成逻辑集中在 `resumes/scripts/`。其中 `generate_alibaba_resumes.py`、`generate_antgroup_resumes.py`、`generate_xhs_resumes_tailored.py` 负责维护各自岗位的定制 `RESUMES` 数据，最终都复用 `generate_xhs_resumes.py` 提供的共享渲染逻辑输出 markdown / html / pdf。共享数据和项目规范化逻辑则来自 `resume_profile.py`。本次发现的问题说明，单独同步上游岗位数据并不够，任何走到共享渲染器的路径都会再次经过项目列表规范化，因此定制简历如果依赖手工编排的项目顺序，必须显式声明保留行为，否则 rerun 仍然会与活动稿漂移。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `resumes/scripts/generate_xhs_resumes.py` | 共享 markdown/html 渲染器 | 本轮真正修复点，新增 `preserve_projects` 分支，阻止定制稿被统一项目模板覆盖 |
| `resumes/scripts/generate_alibaba_resumes.py` | 阿里 AI 应用研发岗定制简历数据源 | 已同步到当前活动稿，并为定制稿打开 `preserve_projects` |
| `resumes/scripts/generate_antgroup_resumes.py` | 蚂蚁 AI 工程岗定制简历数据源 | 已同步到当前活动稿，并为定制稿打开 `preserve_projects` |
| `resumes/scripts/generate_xhs_resumes_tailored.py` | 小红书 AI Native Dev Tooling 定制简历数据源 | 已同步到当前活动稿，并为定制稿打开 `preserve_projects` |
| `resumes/scripts/resume_profile.py` | 共享 profile 与项目归一化逻辑 | 没有在本轮改内容，但它是理解漂移原因和测试依赖链路的关键文件 |
| `tests/test_resume_generator_sync.py` | 渲染结果与活动稿一致性的回归测试 | 新增测试，直接防止三份定制稿再次出现脚本输出回退 |
| `.claude/handoffs/2026-03-28-113912-exam-prep-resume-refresh.md` | 上一轮 handoff | 本轮所有修复都在收口它明确指出的残留风险 |

### Key Patterns Discovered

- 定制简历并不总适合复用通用项目模板顺序，部分岗位稿件需要保留手工编排的项目优先级。
- `resumes/` 当前仍被 `.gitignore` 整体忽略，所以这类生成器源码要进版本控制时必须显式 `git add -f`，否则“本地修好了但仓库里没有”的风险会重复出现。
- 当前工作树存在大量与本任务无关的已暂存和未暂存改动，不能用默认 `git commit` 直接提交整个 index；应使用 pathspec 限定提交范围。
- 在 `main` 已经 `ahead 1, behind 1` 且工作树脏的情况下，直接推 `main` 风险很高，新建分支并单独推送是更安全的落地方式。

## Work Completed

### Tasks Finished

- [x] 同步阿里、蚂蚁、小红书三份定制简历生成器中的岗位数据到当前活动稿版本
- [x] 识别并修复共享渲染器对定制项目顺序的隐藏回退问题，新增 `preserve_projects`
- [x] 新增 `tests/test_resume_generator_sync.py`，校验脚本渲染结果与当前活动稿完全一致
- [x] 运行 `py_compile` 与 7 个目标测试，确认生成链路和测试链路都通过
- [x] 将最小必要的生成器源码链路强制纳入 git，并推送到远端分支 `codex/resume-generator-sync`

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `resumes/scripts/generate_xhs_resumes.py` | 在 markdown/html 渲染路径中根据 `preserve_projects` 决定是否跳过 `normalize_projects()` | 从共享层彻底阻止定制稿 rerun 后被通用项目模板覆盖 |
| `resumes/scripts/generate_alibaba_resumes.py` | 同步第一份定制稿数据，并设置 `preserve_projects=True` | 让阿里活动稿与生成器重新对齐，且后续可安全重跑 |
| `resumes/scripts/generate_antgroup_resumes.py` | 同步第一份定制稿数据，并设置 `preserve_projects=True` | 让蚂蚁活动稿与生成器重新对齐，且后续可安全重跑 |
| `resumes/scripts/generate_xhs_resumes_tailored.py` | 同步小红书定制稿数据，并设置 `preserve_projects=True` | 修复小红书定制稿与共享渲染器之间的顺序漂移 |
| `tests/test_resume_generator_sync.py` | 新增三份定制稿的渲染回归测试 | 用自动化测试锁住本轮修复，不再依赖人工 diff |
| `resumes/scripts/resume_profile.py` | 本轮未改内容，但作为共享依赖被强制纳入 git | 让远端分支包含测试和渲染实际依赖的最小链路 |
| `resumes/scripts/generate_xiaomi_resumes.py` | 本轮未改内容，但被强制纳入 git | 保证共享 profile/生成器测试链路在远端分支上可复现 |
| `resumes/scripts/generate_netease_resumes.py` | 本轮未改内容，但被强制纳入 git | 同上，避免 pushed branch 缺依赖 |
| `resumes/scripts/generate_tencent_resumes.py` | 本轮未改内容，但被强制纳入 git | 同上，保证远端分支自洽 |
| `resumes/scripts/generate_extra_bigtech_resumes.py` | 本轮未改内容，但被强制纳入 git | 为本轮实际运行的测试集保留完整依赖 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 推到新分支 `codex/resume-generator-sync`，不直接推 `main` | 直接推 `main`；先拉平 `main` 再推；新建隔离分支 | `main` 当前存在分叉且工作树很脏，新分支推送风险最低，也最利于后续单独审阅 |
| 使用 pathspec 限定提交范围 | 直接提交整个 index；先清理或取消暂存无关改动 | 仓库里有很多用户自己的 staged 改动，不能擅自改动或混进本次提交 |
| 用 `preserve_projects` 做定制行为开关 | 直接重写 `normalize_projects()`；为三份稿件复制一套特殊渲染器 | 共享逻辑默认行为仍有价值，只需为少数定制稿开特例，改动面最小 |
| 用 `git add -f` 强制跟踪最小源码链路 | 本轮修改 `.gitignore` 策略；只推测试文件不推生成器 | 先保证当前 fix 能被远端完整保存，避免在本轮顺带扩大仓库策略变更范围 |

## Pending Work

### Immediate Next Steps

1. 决定是否基于 `codex/resume-generator-sync` 开 PR，并确定目标基线分支是不是 `main`
2. 决定 `resumes/scripts/` 这批生成器源码后续是持续纳入版本控制，还是只做本次例外追踪
3. 如果需要最新产物，基于当前分支安全重跑阿里、蚂蚁、小红书三份生成器并刷新 PDF

### Blockers/Open Questions

- [ ] `resumes/` 目录是否应该长期保持被忽略，还是只对导出产物忽略、对生成器源码改为正式跟踪
- [ ] 本轮只做了分支推送，没有代替用户创建或合并 PR，后续集成路径还需要决定
- [ ] 当前本地工作树仍有大量无关脏改动，后续任何 git 操作都必须继续避免误提交整个 index

### Deferred Items

- 本轮没有重跑 PDF 导出，因为用户先要求收口“生成器源码与推送”风险
- 本轮没有清理 `.gitignore` 的整体策略，因为这属于更大范围的仓库发布性决策
- 本轮没有处理 `main` 与 `origin/main` 的分叉，因为新分支推送已经满足“先安全备份上远端”的目标

## Context for Resuming Agent

### Important Context

最关键的事实有四个。第一，上一份 handoff 指出的“生成器数据没同步，别急着重跑”的风险，现在对阿里 / 蚂蚁 / 小红书这三份已经实质收口，但修复不只是数据同步，还包含共享渲染器上的 `preserve_projects` 逻辑。第二，这套修复当前只在 commit `cba90e3` 和远端分支 `codex/resume-generator-sync` 上被明确保存，不要假设本地 `main` 或远端 `main` 已经具备这些修复。第三，仓库当前工作树仍然很脏，而且 index 里有大量与本任务无关的 staged 变化，任何后续提交都必须继续使用 pathspec 或先做非常谨慎的拆分，不能直接 `git commit` 整个 index。第四，`resumes/` 被 `.gitignore` 忽略这一点没有在本轮彻底制度化解决，因此今后只要再改生成器源码，就仍然可能遇到“本地修改没有被 git 带走”的同类问题。

远端分支和 PR 入口已经可用：

- Branch: `codex/resume-generator-sync`
- Commit: `cba90e3`
- PR URL: `https://github.com/LouisLau-art/internship-jd-catalog/pull/new/codex/resume-generator-sync`

本轮实际通过的验证命令：

```bash
python3 -m py_compile \
  resumes/scripts/resume_profile.py \
  resumes/scripts/generate_xhs_resumes.py \
  resumes/scripts/generate_xiaomi_resumes.py \
  resumes/scripts/generate_netease_resumes.py \
  resumes/scripts/generate_tencent_resumes.py \
  resumes/scripts/generate_alibaba_resumes.py \
  resumes/scripts/generate_antgroup_resumes.py \
  resumes/scripts/generate_xhs_resumes_tailored.py \
  resumes/scripts/generate_extra_bigtech_resumes.py \
  tests/test_resume_generator_sync.py

python3 -m unittest \
  tests.test_resume_shared_profile \
  tests.test_generate_extra_bigtech_resumes \
  tests.test_resume_generator_sync -v
```

结果：7 个测试全部通过。

### Assumptions Made

- 用户要的是“安全推上远端可继续接力”，不是“直接把本地 `main` 推到 `origin/main`”
- 对这三份定制稿来说，当前活动稿中的项目顺序就是需要长期保留的目标顺序
- 本轮优先闭环生成器同步与远端备份，仓库级 `.gitignore` 治理可以后置

### Potential Gotchas

- `resumes/` 仍被忽略，后续新增或修改生成器源码时如果忘了 `git add -f`，远端就不会有这些更新
- 正常 `git commit` 会把用户之前已经 staged 的无关文件一并带上，这在当前仓库状态下非常危险
- 如果后续 agent 切回 `main` 工作，很容易误以为修复已经存在；实际上 fix 在 `codex/resume-generator-sync`
- 本轮没有刷新 PDF，所以下游如果要交付最新导出产物，还需要在当前安全分支上重跑对应生成脚本

## Environment State

### Tools/Services Used

- `git`
- `python3`
- `/home/louis/.codex/skills/session-handoff/scripts/create_handoff.py`
- `/home/louis/.codex/skills/session-handoff/scripts/validate_handoff.py`

### Active Processes

- 无长期运行服务

### Environment Variables

- `RESUME_ROOT`
- `RESUME_PHOTO`

## Related Resources

- `.claude/handoffs/2026-03-28-113912-exam-prep-resume-refresh.md`
- `.claude/handoffs/2026-03-28-231742-resume-generator-sync-and-push.md`
- `resumes/scripts/generate_xhs_resumes.py`
- `resumes/scripts/generate_alibaba_resumes.py`
- `resumes/scripts/generate_antgroup_resumes.py`
- `resumes/scripts/generate_xhs_resumes_tailored.py`
- `resumes/scripts/resume_profile.py`
- `tests/test_resume_generator_sync.py`
- `https://github.com/LouisLau-art/internship-jd-catalog/pull/new/codex/resume-generator-sync`
