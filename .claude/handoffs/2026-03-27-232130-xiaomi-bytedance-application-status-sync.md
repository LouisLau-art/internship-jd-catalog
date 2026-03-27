# Handoff: 小米 / 字节真实投递状态同步与简历模板统一更新

## Session Metadata
- Created: 2026-03-27 23:21:30
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: 约 2 小时

### Recent Commits (for context)
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic
  - 7265dc8 feat(sync): add markdown dashboard synchronization logic
  - 653ed55 refactor(mail): implement local-first header audit engine

## Handoff Chain

- **Continues from**: [2026-03-27-083418-bytedance-seed-resume-and-job-sync-automation.md](./2026-03-27-083418-bytedance-seed-resume-and-job-sync-automation.md)
  - Previous title: ByteDance Seed 简历生成与求职同步自动化
- **Supersedes**: None

## Current State Summary

本次工作分两条线推进。第一条线是统一所有本地简历生成模板：新增共享资料模块，给所有简历补齐教育经历、语言能力、自我评价，并把重点项目统一收敛为 `multi-agent-skills-catalog`、`internship-jd-catalog`、`louislau-art.github.io` 三条主线，然后全量重导出本地 PDF。第二条线是同步真实投递状态：按用户刚刚确认的官网投递记录，把 [docs/job-search-progress.md](../../docs/job-search-progress.md) 中的小米 6 志愿和字节 3 条真实投递更新成最新状态。当前本地状态是：简历模板和 PDF 已更新完毕，进度记事本已同步，但这些改动都还没有 commit / push。

## Codebase Understanding

### Architecture Overview

这个仓库现在有两套并行但相关的工作流。其一是“公开仓库层”：`data/` 存原始岗位抓取，`docs/` 存 shortlist、投递记事本和临时分析。其二是“本地私有简历层”：`resumes/scripts/` 里的生成器负责维护各公司定向简历，`resumes/sources/` 只保留最终 PDF 成品。简历生成并不是单文件静态维护，而是多公司脚本共享公共资料和渲染逻辑；因此改教育经历/项目经历这类公共信息，最稳的方式是改共享 profile，而不是逐份手工改 Markdown。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| [docs/job-search-progress.md](../../docs/job-search-progress.md) | 求职进度总记事本 | 已同步小米 / 字节真实投递状态 |
| [resumes/scripts/resume_profile.py](../../resumes/scripts/resume_profile.py) | 简历公共资料与标准项目模板 | 本次教育/语言/项目更新的核心入口 |
| [resumes/scripts/generate_xhs_resumes.py](../../resumes/scripts/generate_xhs_resumes.py) | 小红书/字节/腾讯/阿里等共享渲染模板 | 已新增语言能力区块并统一项目归一化 |
| [resumes/scripts/generate_xiaomi_resumes.py](../../resumes/scripts/generate_xiaomi_resumes.py) | 小米简历专用模板 | 已修复外部证件照路径，支持绝对路径图片 |
| [tests/test_resume_shared_profile.py](../../tests/test_resume_shared_profile.py) | 共享简历资料回归测试 | 锁定教育/语言/项目输出，防止回退 |
| [data/xiaomi_positions_intern_tech.json](../../data/xiaomi_positions_intern_tech.json) | 小米技术实习原始落库 | 已确认包含 25 条 Miclaw 相关岗位 |
| [docs/temp/2026-03-27-xiaomi-agent-11-shortlist.md](../../docs/temp/2026-03-27-xiaomi-agent-11-shortlist.md) | 小米 Agent / Miclaw 11 岗聚类短名单 | 后续继续投小米时的直接参考 |

### Key Patterns Discovered

- 简历公共信息不能散落在各个公司脚本里，否则一次字段变更会漏改多份；现在应以 `resume_profile.py` 为单一真源。
- `generate_xhs_resumes.py` 是大量公司的共享渲染底座，很多公司脚本只是 `base.COMMON = ...` 后复用它的渲染函数。
- 小米模板是独立实现，和其他公司不同；它之前对 `RESUME_PHOTO` 只吃路径但生成相对图片 URL，已经改成绝对路径 URI。
- `resumes/sources/` 的边界要继续保持：这里只留最终 PDF，不要把 docx、slug 文件或中间产物再同步进去。
- 进度文档里“推荐优先岗位”和“已投递岗位”会相互引用，更新一处时要一起看是否出现“已投递 / 待投递”矛盾。

## Work Completed

### Tasks Finished

- [x] 新增共享简历资料模块，统一教育经历、语言能力、自我评价和标准项目模板
- [x] 给所有本地简历加入 `internship-jd-catalog（实习JD目录与简历自动化生成系统）` 项目
- [x] 修复小米简历模板对外部证件照路径的处理
- [x] 全量重导出本地各公司简历 PDF
- [x] 更新 [docs/job-search-progress.md](../../docs/job-search-progress.md) 中的小米与字节真实投递状态
- [x] 生成本次 handoff

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| [docs/job-search-progress.md](../../docs/job-search-progress.md) | 同步小米 6 志愿和字节 3 条真实投递记录；更新推荐段落和已生成简历列表 | 防止后续继续按过时状态判断 |
| [resumes/scripts/resume_profile.py](../../resumes/scripts/resume_profile.py) | 新增共享 profile、语言能力、标准项目模板和项目归一化逻辑 | 统一所有简历的公共信息入口 |
| [resumes/scripts/generate_xhs_resumes.py](../../resumes/scripts/generate_xhs_resumes.py) | 接入共享 profile；新增语言能力区块；统一项目归一化；更新 Markdown 头部联系方式 | 让字节/阿里/腾讯/网易等共用新字段 |
| [resumes/scripts/generate_xiaomi_resumes.py](../../resumes/scripts/generate_xiaomi_resumes.py) | 接入共享 profile；新增语言能力区块；统一项目归一化；修复绝对路径证件照 | 让小米简历与其余模板一致 |
| [resumes/scripts/generate_alibaba_resumes.py](../../resumes/scripts/generate_alibaba_resumes.py) | 改为复用共享 profile | 同步新教育/项目/语言字段 |
| [resumes/scripts/generate_antgroup_resumes.py](../../resumes/scripts/generate_antgroup_resumes.py) | 改为复用共享 profile | 同步新教育/项目/语言字段 |
| [resumes/scripts/generate_bytedance_resumes.py](../../resumes/scripts/generate_bytedance_resumes.py) | 改为复用共享 profile | 同步新教育/项目/语言字段 |
| [resumes/scripts/generate_huawei_resumes.py](../../resumes/scripts/generate_huawei_resumes.py) | 改为复用共享 profile | 同步新教育/项目/语言字段 |
| [resumes/scripts/generate_jd_resumes.py](../../resumes/scripts/generate_jd_resumes.py) | 改为复用共享 profile | 同步新教育/项目/语言字段 |
| [resumes/scripts/generate_meituan_resumes.py](../../resumes/scripts/generate_meituan_resumes.py) | 改为复用共享 profile | 同步新教育/项目/语言字段 |
| [resumes/scripts/generate_netease_resumes.py](../../resumes/scripts/generate_netease_resumes.py) | 改为复用共享 profile | 同步新教育/项目/语言字段 |
| [resumes/scripts/generate_tencent_resumes.py](../../resumes/scripts/generate_tencent_resumes.py) | 改为复用共享 profile | 同步新教育/项目/语言字段 |
| [resumes/scripts/generate_xhs_resumes_tailored.py](../../resumes/scripts/generate_xhs_resumes_tailored.py) | 改为复用共享 profile | 保持定制版与主模板一致 |
| [tests/test_resume_shared_profile.py](../../tests/test_resume_shared_profile.py) | 新增回归测试 | 锁定教育/语言/项目模板输出 |
| [resumes/sources](../../resumes/sources) | 全量重导出本地 PDF，现仍只有 PDF 文件 | 让最新模板进入实际投递产物 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 用共享 `resume_profile.py` 管理简历公共信息 | 逐份 Markdown / 逐公司脚本手改；抽公共模块统一维护 | 后者能一次更新所有简历，回归测试也更稳 |
| 把 `ScholarFlow` 和 `multi-cloud-email-sender` 保留在实习经历，把项目经历主线换成 3 个公开项目 | 继续把两者放在重点项目；只加 1 个新项目 | 用户明确要求项目经历以公开项目为主，实习经历已覆盖前两者 |
| 小米新增 3 个北京志愿在文档中写成第 1-3 志愿，武汉 3 个顺延成第 4-6 志愿 | 保留旧武汉 1-3 志愿编号 | 这更贴合用户刚给的官网投递记录 |
| 字节 `AI Agent服务端研发实习生-开发者服务` 在文档中拆成北京和上海两条投递 | 继续写成“北京/上海/杭州”一条 | 用户明确给出了两个独立投递记录，拆开更准确 |

## Pending Work

### Immediate Next Steps

1. 继续同步其余公司的真实投递状态，尤其是网易、拼多多、滴滴等最近新增的大厂岗位
2. 决定是否将本次文档与简历模板变更 commit 到本地分支；注意简历成品含隐私，不能公开 push
3. 如果继续投递，优先更新 [docs/job-search-progress.md](../../docs/job-search-progress.md) 和对应公司短名单，避免再次出现“真实状态与记事本漂移”

### Blockers/Open Questions

- [ ] `docs/job-search-progress.md` 里总览区的小米岗位数量仍是旧快照（`~30`），没有同步到当前 377 条技术实习落库；本次未一并重写总览口径
- [ ] 字节 `AI研发实习生-剪映CapCut用户增长` 的官网拷贝里用户未单独贴出日期，文档中按本次口述统一记为 `2026-03-27`

### Deferred Items

- 若要把“小米全部 377 条技术岗”固化成长期可用的全量优先级文档，需要单独做一份按岗位家族分层的 MD；本次只回答了 top 3 和 Miclaw 相关问题，没有落正式文档
- 如果后续要提交代码，需要先明确哪些 `resumes/scripts` 文件处于 git 跟踪边界内，当前很多本地简历文件可能被 ignore 或未纳入公开仓库

## Context for Resuming Agent

### Important Context

这次最重要的不是单份简历内容，而是“公共资料入口已经被重构”。以后再改教育经历、语言能力、自我评价、项目经历，优先改 [resumes/scripts/resume_profile.py](../../resumes/scripts/resume_profile.py)，不要再分散到各公司脚本里逐个修改。另一个关键点是 [docs/job-search-progress.md](../../docs/job-search-progress.md) 现在已与用户最新口述同步：小米共 6 志愿已投（北京 3、武汉 3），字节已投 3 条（北京/上海 AI Agent 服务端各 1，上海剪映 1）。如果下个 agent 继续做投递管理，一定要基于这个新状态，而不是基于更早的“字节 0 投 / 小米只投武汉 3 志愿”旧认知。

### Assumptions Made

- 用户刚给出的官网投递记录优先于仓库旧文档
- 字节 `AI研发实习生-剪映CapCut用户增长` 未显式贴出日期，但因用户说“刚刚投了”，文档按 `2026-03-27` 记
- 小米 `Miclaw-AI agent开发实习生` 暂时复用 [刘新宇-小米-AI Agent开发实习生.pdf](../../resumes/sources/刘新宇-小米-AI%20Agent开发实习生.pdf)

### Potential Gotchas

- `session-handoff` skill 自带脚本不在仓库 `scripts/` 下，而在 `/home/louis/.codex/skills/session-handoff/scripts/`；直接跑仓库相对路径会报 `No such file or directory`
- 小米模板之前吃 `RESUME_PHOTO` 但生成相对图片 URL，外部照片路径会失效；这个问题已修，但如果后续回退代码要注意别把它带回去
- `resumes/sources/` 目前本地有 43 个 PDF 且无非 PDF 文件，继续导出时要守住这个边界
- 很多简历相关文件可能不在 git 跟踪里，`git status` 不一定能完整反映本地简历层改动

## Environment State

### Tools/Services Used

- `pandoc`：用于 Markdown -> docx
- `google-chrome --headless=new`：用于 HTML -> PDF
- `pdftotext`：用于抽检 PDF 内文本是否包含新字段
- `pytest`：已跑共享简历 profile 回归测试
- `gh` 与 GitHub MCP：本次用于核对公开仓库状态与 README / 提交记录

### Active Processes

- 无需长期保留的活跃进程；本次 PDF 批量导出已跑完

### Environment Variables

- `RESUME_PHOTO`
- `RESUME_ROOT`

## Related Resources

- [前一份 handoff：2026-03-27-083418-bytedance-seed-resume-and-job-sync-automation.md](./2026-03-27-083418-bytedance-seed-resume-and-job-sync-automation.md)
- [求职进度记事本](../../docs/job-search-progress.md)
- [小米 Agent / Miclaw 11 岗短名单](../../docs/temp/2026-03-27-xiaomi-agent-11-shortlist.md)
- [共享简历资料模块](../../resumes/scripts/resume_profile.py)
- [共享渲染模板（XHS/字节等）](../../resumes/scripts/generate_xhs_resumes.py)
- [小米渲染模板](../../resumes/scripts/generate_xiaomi_resumes.py)
- [小米技术实习原始数据](../../data/xiaomi_positions_intern_tech.json)

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
