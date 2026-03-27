# Handoff: 阿里 / 蚂蚁 / 小红书笔试冲刺与求职进度文档修正

## Session Metadata
- Created: 2026-03-28 00:25:11
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: 约 1 小时

### Recent Commits (for context)
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic
  - 7265dc8 feat(sync): add markdown dashboard synchronization logic
  - 653ed55 refactor(mail): implement local-first header audit engine

## Handoff Chain

- **Continues from**: [2026-03-27-232130-xiaomi-bytedance-application-status-sync.md](./2026-03-27-232130-xiaomi-bytedance-application-status-sync.md)
  - Previous title: 小米 / 字节真实投递状态同步与简历模板统一更新
- **Supersedes**: None

## Current State Summary

本次先从上一份 handoff 恢复上下文，并用 `check_staleness.py` 确认 [2026-03-27-232130-xiaomi-bytedance-application-status-sync.md](./2026-03-27-232130-xiaomi-bytedance-application-status-sync.md) 为 `FRESH`。随后发现当前仓库缺少 `.env`，`/sync-jobs` 无法继续跑通，且本地不存在 `data/job_emails.json`，因此没有硬推同步链路，而是先手工修正 [docs/job-search-progress.md](../../docs/job-search-progress.md) 里明显过期的总览数字。之后用户把重心切到 `2026-03-28` 阿里、`2026-03-29` 小红书和已进入流程的蚂蚁笔试准备，本次基于 GitHub MCP 和现有邮件内容产出了 3 份本地冲刺材料。最后用户反馈“看了还是一点都不会”，所以下一个 agent 不该继续堆文档，而应该直接进入“临考救火式一问一答辅导”。

## Codebase Understanding

### Architecture Overview

这个仓库至少有三条并行链路。第一条是岗位数据链路：`data/` 存各公司抓取落库，`scripts/` 存爬取与清洗脚本，`docs/job-search-progress.md` 作为人工维护的总览记事本。第二条是 handoff / 临时分析链路：`.claude/handoffs/` 保存续接上下文，`docs/temp/` 用于阶段性分析文档和临时决策材料。第三条是 QQ 邮件同步链路：依赖本地 `.env` 和邮件侧数据文件，当前环境不满足，因此本次没有继续推 `sync-jobs` 自动同步。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| [docs/job-search-progress.md](../../docs/job-search-progress.md) | 求职进度总记事本 | 本次手工修正了小米 / 网易 / 滴滴和总览统计 |
| [docs/temp/2026-03-28-29-exam-cram-pack.md](../../docs/temp/2026-03-28-29-exam-cram-pack.md) | 完整笔试冲刺包 | 汇总 GitHub 真题源、题型判断和冲刺顺序 |
| [docs/temp/2026-03-28-29-exam-priority-checklist.md](../../docs/temp/2026-03-28-29-exam-priority-checklist.md) | 最短执行版 checklist | 直接给出今晚和明天的刷题顺序与直达链接 |
| [docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md](../../docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md) | 阿里 / 蚂蚁临考速记 | 浓缩算法 / MySQL / TCP / Redis 高频点 |
| [.claude/handoffs/2026-03-27-232130-xiaomi-bytedance-application-status-sync.md](./2026-03-27-232130-xiaomi-bytedance-application-status-sync.md) | 上一份恢复上下文的 handoff | 本次先验证其 staleness，再在其基础上继续推进 |

### Key Patterns Discovered

- `docs/job-search-progress.md` 很容易和原始 `data/` 落库数量漂移，尤其在多公司批量爬取后；总览数字不能默认可信。
- 这个仓库允许在 `docs/temp/` 下快速生成“临时但可复用”的作战文档，适合短时间高压任务。
- GitHub 上关于校招笔试最有用的材料常常不是完整题解仓库，而是“真题索引仓库 + 归档牛客标题页”的组合。
- 当前脏工作区里存在大量和本次任务无关的未提交文件，写 handoff 时必须只记录本次真实触及的文件，不能把自动 scaffold 带出的噪音照抄进去。

## Work Completed

### Tasks Finished

- [x] 用 `check_staleness.py` 验证上一份 handoff 为 `FRESH`，确认可直接续接
- [x] 识别出 `.env` 缺失与 `data/job_emails.json` 缺失，停止继续尝试 `/sync-jobs`
- [x] 手工修正 [docs/job-search-progress.md](../../docs/job-search-progress.md) 中过期的总览数字
- [x] 用 GitHub MCP 提取阿里 / 蚂蚁 / 小红书笔试真题索引与关键直达链接
- [x] 新建完整冲刺包、优先级 checklist、阿里 / 蚂蚁临考速记 3 份文档
- [x] 生成本次 handoff

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| [docs/job-search-progress.md](../../docs/job-search-progress.md) | 把小米原始岗位数从 `~30` 改为 `377`，网易从 `1` 改为 `61`，滴滴从 `15` 改为 `75`，总 raw export 从 `约 1781` 改为 `约 2231`，并移除一处多余的尾部 `|` | 修正明显过期的总览统计，避免后续继续按旧数字判断 |
| [docs/temp/2026-03-28-29-exam-cram-pack.md](../../docs/temp/2026-03-28-29-exam-cram-pack.md) | 新建完整冲刺包，汇总阿里 / 蚂蚁 / 小红书真题索引、GitHub 归档线索、题型判断与冲刺顺序 | 把分散的 GitHub 信息收拢成可执行文档 |
| [docs/temp/2026-03-28-29-exam-priority-checklist.md](../../docs/temp/2026-03-28-29-exam-priority-checklist.md) | 新建最短执行版 checklist，给出 Nowcoder 直达链接和 2 小时刷题顺序 | 降低用户临考前的信息负担 |
| [docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md](../../docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md) | 新建临考速记卡，浓缩算法题型判断、MySQL、TCP、Redis 高频结论 | 面向最后 15-20 分钟速看，不再让用户翻长文 |
| [.claude/handoffs/2026-03-28-002511-alibaba-ant-exam-cram.md](./2026-03-28-002511-alibaba-ant-exam-cram.md) | 记录本次恢复、修正和笔试冲刺准备上下文 | 便于后续 agent 无缝续接 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 不在 `.env` 缺失时强行推进 `/sync-jobs` | 继续尝试同步链路；先停下并人工修正文档 | 当前环境条件不满足，强推只会浪费时间并引入更多不确定性 |
| 先修正总览数字，再切到笔试准备 | 继续深挖求职同步链路；转去更紧急的笔试 | 用户明确表示近两天至少 3 家笔试，时间优先级更高 |
| 笔试资料优先使用 GitHub 真题索引仓库 `DerekLin924/bat_code` | 直接刷大而全面经库；普通 Web 搜索 | 前者更贴近真实笔试入口和场次，效率更高 |
| 对小红书题型只做“推断”，不当作官方事实写死 | 直接断言固定题型；完全不作判断 | 现有证据来自 GitHub 归档标题和用户邮件域名 `test.acmcoder.com`，足以指导准备，但不够作为官方确认 |
| 从“继续堆资料”切换到“后续应做互动式救火辅导” | 继续扩写文档；再补更多题库 | 用户已明确反馈“看了还是一点都不会”，继续堆资料收益很低 |

## Pending Work

### Immediate Next Steps

1. 不要再继续补文档，直接带用户做 `30-45` 分钟的临考救火问答，目标是保住选择题和基础编程题的分数
2. 若用户还有时间，再从 [docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md](../../docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md) 提炼成“最后 5 分钟极简版”
3. 等笔试阶段过去后，再回到 `.env` / `data/job_emails.json` 缺失问题，恢复 `/sync-jobs` 这条自动同步链路

### Blockers/Open Questions

- [ ] 当前仓库缺少 `.env`，无法直接继续 QQ 邮件同步相关流程
- [ ] 当前本地不存在 `data/job_emails.json`，说明邮件数据侧准备也不完整
- [ ] 用户当前对笔试材料吸收度很低，继续给文档不一定有效
- [ ] 蚂蚁邮件片段未给出这轮明确开考时间，当前只能确认已进入笔试链路

### Deferred Items

- 对 `.mcp.json`、`README.md`、大量 `data/*.json/csv` 和 `scripts/*.py` 的未提交改动，本次未审查来源，也未尝试整理
- 对 GitHub 归档牛客页面，没有进一步抓正文内容；本次只提取标题和直达链接，已足够支持临时冲刺
- 对小红书题型没有做更重的外部验证，因为当下最重要的是给用户提供可执行的救火方案

## Context for Resuming Agent

### Important Context

最关键的事实有三个。第一，这次已经产出了足够多的静态材料：[完整冲刺包](../../docs/temp/2026-03-28-29-exam-cram-pack.md)、[优先级 checklist](../../docs/temp/2026-03-28-29-exam-priority-checklist.md)、[阿里 / 蚂蚁临考速记](../../docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md)，所以后续不要再继续收集链接或补更多文档。第二，用户在看完后明确说“我看了 我一点都不会啊”，说明现在真正缺的是“把这些材料转成能记住的最小集合”，而不是更多来源。第三，前面用于恢复上下文的同步线索仍然没有真正恢复：`.env` 缺失、`data/job_emails.json` 缺失，所以如果后续又切回岗位同步，不要误以为这条链已经打通。

### Assumptions Made

- 用户当前最紧急的是 `2026-03-28` 阿里笔试和接下来 `2026-03-29` 小红书笔试，而不是继续维护岗位同步自动化
- 小红书更像 `选择题 + ACMCoder 编程题` 的混合模式，这个判断来自 GitHub 归档标题和用户邮件域名，不是官方规则原文
- 用户当前需要的是“有人带着过一遍高频点”，不是再看一轮长文档

### Potential Gotchas

- `hxh5/nowcoder` 仓库里很多页面只是牛客标题归档，不是完整帖子正文；不要把它当成完整题解库
- 自动 scaffold 会把当前脏工作区里很多无关未提交文件塞进模板，写 handoff 时必须手工清理
- [docs/job-search-progress.md](../../docs/job-search-progress.md) 只修了最明显的几处总览数字，并没有做一轮全仓对账
- 用户上一条真实状态是焦虑且低准备度，如果恢复后直接继续发长清单，效果大概率很差

## Environment State

### Tools/Services Used

- `python /home/louis/.codex/skills/session-handoff/scripts/check_staleness.py`：验证上一份 handoff 是否可直接恢复
- `python /home/louis/.codex/skills/session-handoff/scripts/create_handoff.py`：生成本次 handoff scaffold
- `python /home/louis/.codex/skills/session-handoff/scripts/validate_handoff.py`：校验 handoff 完整性与安全性
- GitHub MCP `get_file_contents`：读取 `DerekLin924/bat_code` 的公司笔试索引文件
- `sed` / `ls` / `git status --short`：读取本地文档和工作区状态

### Active Processes

- 没有需要保留的长期进程
- 用户中断了上一条回复，没有后台服务需要接管

### Environment Variables

- 无已确认的可用环境变量
- 需要注意的是仓库根目录 `.env` 当前缺失

## Related Resources

- [上一份 handoff](./2026-03-27-232130-xiaomi-bytedance-application-status-sync.md)
- [求职进度总记事本](../../docs/job-search-progress.md)
- [完整笔试冲刺包](../../docs/temp/2026-03-28-29-exam-cram-pack.md)
- [优先级 Checklist](../../docs/temp/2026-03-28-29-exam-priority-checklist.md)
- [阿里 / 蚂蚁临考速记](../../docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md)

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
