# Handoff: 阿里/蚂蚁/小红书笔试辅导与定制简历-PDF刷新

## Session Metadata
- Created: 2026-03-28 11:39:12
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: 约 3 小时

### Recent Commits (for context)
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic
  - 7265dc8 feat(sync): add markdown dashboard synchronization logic

## Handoff Chain

- **Continues from**: [2026-03-28-002511-alibaba-ant-exam-cram.md](.claude/handoffs/2026-03-28-002511-alibaba-ant-exam-cram.md)
  - Previous title: 阿里 / 蚂蚁 / 小红书笔试冲刺与求职进度文档修正
- **Supersedes**: None

> Review the previous handoff for full context before filling this one.

## Current State Summary

本轮工作先围绕阿里 `AI应用研发工程师` 笔试做了方向校正和口头冲刺辅导，确认该岗位不是传统纯后端，而是 `AI 应用 + Agent 工程落地`，随后把 `doubao-batch-translator` 包装成贴岗案例，并落到阿里、蚂蚁、小红书三份实际投递简历里。三份最新可上传的 PDF 已经重新导出并覆盖到 `resumes/sources/`，可以直接用于更新已投递但仍允许改简历的岗位。当前最大残留问题不是 PDF 本身，而是阿里/蚂蚁的 `generate_*_resumes.py` 内嵌数据层仍是旧版本，后续若直接跑生成脚本，有覆盖掉本次修改的风险。

## Codebase Understanding

### Architecture Overview

这个仓库的简历体系有三层，最容易混淆。第一层是 `resumes/scripts/*.md`，这是当前最直接、最适合紧急修订后导出的活动源稿；配合 `scripts/export_resumes.py` 里的 `export_markdown_job()`，可直接转成 `styled.html + docx + pdf`。第二层是 `resumes/scripts/generate_*.py`，其中阿里和蚂蚁脚本把内容硬编码在 `RESUMES` 列表里，并会写回同名的 `resumes/scripts/*.md` 与对应 PDF，所以它们其实是“脚本驱动的上游源”。第三层是 `resumes/others/sources/*.md`，更像备份/草稿/替代版本，本轮被用于分析和对照，但不是这次最终 PDF 的直接导出来源。

笔试辅导部分没有形成太多新文件，主要是基于当前对话和外部仓库 `/home/louis/doubao-batch-translator` 做证据梳理。该仓库中的 HTML 处理器、异步客户端和漏译检测模块分别提供了 `chunk / fallback / evaluation` 的真实工程证据，被抽取进简历和口头话术里。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `resumes/scripts/alibaba-ai-application-rd-engineer-resume.md` | 阿里 AI 应用岗当前活动源稿 | 已按 `ScholarFlow + Doubao + skills` 重写，并已导出最新 PDF |
| `resumes/scripts/ant-ai-engineer-application-resume.md` | 蚂蚁 AI 应用岗当前活动源稿 | 已按同一证据链重写，并已导出最新 PDF |
| `resumes/scripts/xhs-ai-native-dev-tooling-resume.md` | 小红书产品工程师（AI应用方向）当前活动源稿 | 已改成更贴 `质效研发` 的版本，并已导出最新 PDF |
| `resumes/sources/刘新宇-阿里巴巴-AI应用研发工程师.pdf` | 阿里最终上传版 PDF | 用户当前可直接拿去更新投递 |
| `resumes/sources/刘新宇-蚂蚁-AI工程师-应用方向.pdf` | 蚂蚁最终上传版 PDF | 用户当前可直接拿去更新投递 |
| `resumes/sources/刘新宇-小红书-产品工程师-AI应用方向-质效研发.pdf` | 小红书最终上传版 PDF | 用户当前可直接拿去更新投递 |
| `resumes/scripts/generate_alibaba_resumes.py` | 阿里脚本驱动上游数据 | 仍是旧内容，后续需要同步，避免覆盖本轮修订 |
| `resumes/scripts/generate_antgroup_resumes.py` | 蚂蚁脚本驱动上游数据 | 仍是旧内容，后续需要同步，避免覆盖本轮修订 |
| `scripts/export_resumes.py` | Markdown 到 HTML/DOCX/PDF 的统一导出工具 | 本轮实际借用了其中的 `export_markdown_job()` 完成紧急 PDF 导出 |
| `/home/louis/doubao-batch-translator/processors/html_worker.py` | 翻译块级合并与 chunk 逻辑 | 简历里 `chunk strategy` 的直接证据 |
| `/home/louis/doubao-batch-translator/core/client.py` | 模型路由、限流、降级 | 简历里 `fallback / model routing / rate limit` 的直接证据 |
| `/home/louis/doubao-batch-translator/tools/check_untranslated.py` | 启发式漏译检测 | 简历里 `evaluation / repair loop` 的直接证据 |

### Key Patterns Discovered

- 对这个仓库做紧急简历修订时，优先看 `resumes/scripts/*.md`，不要先改 `resumes/others/sources/*.md` 就以为导出链已经更新。
- 阿里和蚂蚁岗位的 `generate_*_resumes.py` 会覆盖 `resumes/scripts/*.md` 和对应 PDF，所以如果上游 `RESUMES` 不同步，重新跑脚本会把新内容冲回旧版本。
- `scripts/export_resumes.py` 依赖 `pandoc + google-chrome --headless=new`，适合在已知 Markdown 正确时做快速定点导出。
- 当前工作树很脏，包含大量与本次任务无关的 `.firecrawl/`、`data/`、`docs/` 变更；本轮没有清理或回滚这些内容，后续也不应误操作。

## Work Completed

### Tasks Finished

- [x] 校正阿里 AI 应用岗准备方向，确认应以 `AI 应用工程 + Agent 工作流 + RAG/Context/Fallback/Observability` 为主线，而不是传统纯后端题库思路。
- [x] 基于 `/home/louis/doubao-batch-translator` 提炼出 `chunk / context / fallback / evaluation` 贴岗案例，并将其转成简历可用表述。
- [x] 审核阿里 AI 应用岗简历，指出项目排序、证据链和模板污染问题，并给出默认修订方案。
- [x] 重写阿里、蚂蚁、小红书三份当前活动源稿，统一到 `ScholarFlow + Doubao Batch Translator + multi-agent-skills-catalog` 的主线。
- [x] 重新导出阿里、蚂蚁、小红书三份 `styled.html + docx + pdf`，并把最终上传版 PDF 覆盖到 `resumes/sources/`。
- [x] 用 `pdftotext` 抽文本验收，确认三份 PDF 都已包含 `Doubao Batch Translator`、`Evaluation / Observability` 等新内容。

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `resumes/others/sources/alibaba-ai-application-rd-engineer-resume.md` | 先做结构性重写，验证阿里 AI 应用岗的证据链方案 | 作为分析和对照稿，沉淀贴岗表述 |
| `resumes/others/sources/ant-ai-engineer-application-resume.md` | 同步阿里面向 AI 应用岗的写法 | 保持阿里/蚂蚁口径一致 |
| `resumes/scripts/alibaba-ai-application-rd-engineer-resume.md` | 改成活动导出源稿，加入 Doubao 案例、重排项目、刷新技能栏 | 这是阿里 PDF 的直接来源 |
| `resumes/scripts/ant-ai-engineer-application-resume.md` | 改成活动导出源稿，加入 Doubao 案例、重排项目、刷新技能栏 | 这是蚂蚁 PDF 的直接来源 |
| `resumes/scripts/xhs-ai-native-dev-tooling-resume.md` | 改成更贴 `产品工程师（AI应用方向）- 质效研发` 的版本，强调评测/质效/工具链 | 这是小红书 PDF 的直接来源 |
| `resumes/scripts/alibaba-ai-application-rd-engineer-resume-styled.html` | 由更新后的 Markdown 重新导出 | 用于阿里 PDF 打印 |
| `resumes/scripts/ant-ai-engineer-application-resume-styled.html` | 由更新后的 Markdown 重新导出 | 用于蚂蚁 PDF 打印 |
| `resumes/scripts/xhs-ai-native-dev-tooling-resume-styled.html` | 由更新后的 Markdown 重新导出 | 用于小红书 PDF 打印 |
| `resumes/scripts/刘新宇-阿里巴巴-AI应用研发工程师.pdf` | 重新导出并覆盖别名 PDF | 用户直接上传的阿里版本 |
| `resumes/scripts/刘新宇-蚂蚁-AI工程师-应用方向.pdf` | 重新导出并覆盖别名 PDF | 用户直接上传的蚂蚁版本 |
| `resumes/scripts/刘新宇-小红书-产品工程师-AI应用方向-质效研发.pdf` | 重新导出并覆盖别名 PDF | 用户直接上传的小红书版本 |
| `resumes/sources/刘新宇-阿里巴巴-AI应用研发工程师.pdf` | 复制最新阿里 PDF 到公共投递路径 | 方便统一从 `resumes/sources/` 取文件 |
| `resumes/sources/刘新宇-蚂蚁-AI工程师-应用方向.pdf` | 复制最新蚂蚁 PDF 到公共投递路径 | 方便统一从 `resumes/sources/` 取文件 |
| `resumes/sources/刘新宇-小红书-产品工程师-AI应用方向-质效研发.pdf` | 复制最新小红书 PDF 到公共投递路径 | 方便统一从 `resumes/sources/` 取文件 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 以 `ScholarFlow + Doubao Batch Translator + multi-agent-skills-catalog` 作为 AI 应用岗主证据链 | 保留旧的 `skills + internship-jd-catalog + 个人主页` 三件套；只加一两句 Doubao 描述；重排为新三件套 | 阿里/蚂蚁/小红书这三类 AI 应用岗更需要业务型 AI 项目证据，不能只靠工具站和博客 |
| 紧急导出阶段优先修改 `resumes/scripts/*.md` 并直接导出 PDF | 先同步 `generate_*_resumes.py` 再统一生成；只改 `resumes/others/sources/*.md` | 用户要立刻更新已投递岗位，先拿到正确 PDF 最重要 |
| 暂不修改 `resume_profile.py` | 全局调整共享模板；仅局部修订岗位稿 | `resume_profile.py` 会影响大量非 AI 应用岗，风险大且不适合临考/临投递窗口 |
| 小红书稿保留 `AI Native 工具 / 质效` 风格，但仍并入 Doubao 案例 | 完全沿用阿里/蚂蚁文案；完全保留旧工具链导向写法 | 小红书岗位名更偏 `产品工程师（AI应用方向）- 质效研发`，需要强调评测/质效，但不能丢掉真实工程项目 |

## Pending Work

### Immediate Next Steps

1. 如果用户还要继续更新投递，直接使用 `resumes/sources/` 下的三份最新 PDF，不要重新跑阿里/蚂蚁生成脚本。
2. 在不影响现有 PDF 的前提下，补同步 `resumes/scripts/generate_alibaba_resumes.py` 和 `resumes/scripts/generate_antgroup_resumes.py` 的内嵌 `RESUMES` 数据，避免下次脚本覆盖。
3. 如果用户还要继续笔试辅导，沿着上一份 handoff 的问答节奏，继续做 `Agent / RAG / Memory / Tool Calling / Evaluation / Observability` 的短问短答强化。

### Blockers/Open Questions

- [ ] Blocker: `resumes/scripts/generate_alibaba_resumes.py` 仍保留旧内容 - Needs: 将阿里 AI 应用岗的 `summary / skills / experience / projects` 同步到脚本里的 `RESUMES` 数据。
- [ ] Blocker: `resumes/scripts/generate_antgroup_resumes.py` 仍保留旧内容 - Needs: 将蚂蚁 AI 应用岗的 `summary / skills / experience / projects` 同步到脚本里的 `RESUMES` 数据。
- [ ] Question: 是否还需要把小红书相关生成脚本或别的 AI Native 岗位一并同步到同一证据链 - Suggested: 先看用户是否还要继续投同类岗位，再决定批量同步。

### Deferred Items

- 同步阿里/蚂蚁生成脚本数据（deferred because: 当前用户的最紧急目标是拿到可直接上传的 PDF，而不是清理生成链路）
- 检查并清理 `resumes/others/sources/` 与 `resumes/scripts/` 之间的长期重复和漂移（deferred because: 当前只处理紧急投递）
- 为考试再压一版最后 5 分钟极简速记（deferred because: 本轮重点转向了简历/PDF 更新）

## Context for Resuming Agent

### Important Context

最重要的信息有四条。第一，当前用户手上已经有三份可直接上传的最终 PDF，路径分别是 `resumes/sources/刘新宇-阿里巴巴-AI应用研发工程师.pdf`、`resumes/sources/刘新宇-蚂蚁-AI工程师-应用方向.pdf`、`resumes/sources/刘新宇-小红书-产品工程师-AI应用方向-质效研发.pdf`。第二，阿里和蚂蚁的“真正上游”仍然是 `resumes/scripts/generate_alibaba_resumes.py` 和 `resumes/scripts/generate_antgroup_resumes.py` 里的 `RESUMES` 数据；当前 PDF 正确，但脚本数据没同步，所以不要直接运行这两个脚本，否则会把新内容冲回旧版。第三，小红书 `产品工程师（AI应用方向）- 质效研发` 这份本轮是直接改 `resumes/scripts/xhs-ai-native-dev-tooling-resume.md` 然后导出的，当前文件已经正确。第四，`doubao-batch-translator` 被证明是本轮最有价值的贴岗案例，证据来自外部仓库 `/home/louis/doubao-batch-translator`，尤其是其 HTML 处理模块的 chunk 逻辑、异步客户端的模型降级与限流、以及漏译检测模块的启发式修补闭环。

### Assumptions Made

- Assumption 1: 用户当前最优先的需求是立刻更新已投递但还允许替换简历的岗位，所以先交付 PDF，再处理脚本同步。
- Assumption 2: `resumes/scripts/*.md` 是本轮最安全、最快速的活动导出源，而 `resumes/others/sources/*.md` 只是辅助草稿和对照材料。
- Assumption 3: 本机仍可使用 `pandoc`、`google-chrome --headless=new` 和 `pdftotext`，因此继续导出与验收不会受环境阻塞。

### Potential Gotchas

- 运行 `resumes/scripts/generate_alibaba_resumes.py` 或 `resumes/scripts/generate_antgroup_resumes.py` 会覆盖本轮刚改好的 Markdown/PDF，因为脚本内嵌数据还没同步。
- 工作树里有大量与本轮无关的脏变更；不要为了“干净”去回滚 `.firecrawl/`、`data/`、`docs/` 等内容。
- 当前仓库根目录没有 `create_handoff.py` / `validate_handoff.py`，本轮用的是 skill 目录下的脚本：`/home/louis/.codex/skills/session-handoff/scripts/`。
- 小红书稿件名和岗位名不完全直观对应，当前目标文件是 `resumes/scripts/xhs-ai-native-dev-tooling-resume.md`，不是其它 `xhs-ecology-*` 或 `xhs-java-*` 文件。

## Environment State

### Tools/Services Used

- `python3`: 用于调用导出辅助逻辑和 handoff 脚本
- `pandoc`: 把 Markdown 导出为 `docx`
- `google-chrome --headless=new`: 把 `styled.html` 打印为 `pdf`
- `pdftotext`: 验收 PDF 是否真正包含新文案
- `git`: 查看当前工作树和分支状态

### Active Processes

- 无需要保留的后台进程；本轮所有导出与验收命令都已结束。

### Environment Variables

- `RESUME_ROOT`
- `RESUME_PHOTO`

## Related Resources

- `.claude/handoffs/2026-03-28-002511-alibaba-ant-exam-cram.md`
- `resumes/scripts/alibaba-ai-application-rd-engineer-resume.md`
- `resumes/scripts/ant-ai-engineer-application-resume.md`
- `resumes/scripts/xhs-ai-native-dev-tooling-resume.md`
- `resumes/sources/刘新宇-阿里巴巴-AI应用研发工程师.pdf`
- `resumes/sources/刘新宇-蚂蚁-AI工程师-应用方向.pdf`
- `resumes/sources/刘新宇-小红书-产品工程师-AI应用方向-质效研发.pdf`
- `resumes/scripts/generate_alibaba_resumes.py`
- `resumes/scripts/generate_antgroup_resumes.py`
- `scripts/export_resumes.py`
- `/home/louis/doubao-batch-translator/processors/html_worker.py`
- `/home/louis/doubao-batch-translator/core/client.py`
- `/home/louis/doubao-batch-translator/tools/check_untranslated.py`

---

**Security Reminder**: 本文件未写入任何密钥、token 或账号密码；若后续继续补充，仍需避免写入 secrets。
