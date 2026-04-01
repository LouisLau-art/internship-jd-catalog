# Handoff: 阿里/蚂蚁笔试 2 小时抢分冲刺与项目证据同步

## Session Metadata
- Created: 2026-03-28 12:15:00
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: 约 1 小时

### Recent Commits (for context)
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill

## Handoff Chain

- **Continues from**: [.claude/handoffs/2026-03-28-113912-exam-prep-resume-refresh.md](.claude/handoffs/2026-03-28-113912-exam-prep-resume-refresh.md)
  - Previous title: 阿里/蚂蚁/小红书笔试辅导与定制简历-PDF刷新
- **Supersedes**: None

## Current State Summary

本轮对话完成了 14:00 阿里笔试前的最后一次密集补强。我们跳出了长文档，通过“短问短答”和“场景模拟”覆盖了：1. 基础八股（MySQL 联合索引原则、TCP 4 次挥手原因、Redis 缓存击穿比喻）；2. 操作系统（进程 vs 线程比喻、kill -9 机制）；3. AI 应用岗进阶（RAG 向量检索 HNSW、Python GIL 与异步 IO、API 限流与 Jitter）。同时，确认了简历修订已完成且 PDF 已导出至 `resumes/sources/`，重点项目 `doubao-batch-translator` 的工程证据（Chunk/Fallback/Evaluation）已作为笔试/面试的核心话术。

## Codebase Understanding

### Architecture Overview

虽然本轮主要是知识辅导，但涉及了两个关键代码源。第一是本项目简历生成链，`resumes/sources/` 存有最新 PDF；第二是外部仓库 `/home/louis/doubao-batch-translator`，其中的异步限流和漏译修复循环被提炼成了 AI 应用岗的专业答案。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `resumes/sources/刘新宇-阿里巴巴-AI应用研发工程师.pdf` | 最终版简历 | 包含最新的 Doubao 翻译项目证据，考前可扫一眼项目描述 |
| `docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md` | 临考速记卡 | 包含 MySQL/TCP/Redis 的最简结论，进场前 5 分钟首选 |
| `docs/temp/2026-03-28-29-exam-priority-checklist.md` | 刷题 Checklist | 包含阿里 0917、0910 场真题链接，若有时间可看一眼题目大意 |

### Key Patterns Discovered

- 阿里笔试偏向**原理（How/Why）**，而不仅是 API 调用；例如会问“为什么 TCP 不是 2 次握手”或“联合索引失效的场景”。
- AI 应用岗考题趋向于 **Agent 编排与工程稳定性**，需要准备好关于“死循环处理”和“模型降级”的话术。

## Work Completed

### Tasks Finished

- [x] 完成 MySQL/Redis/TCP 高频八股的白话文复习。
- [x] 完成进程/线程/Linux 信号机制的基础复习。
- [x] 提炼 AI 应用岗专属考点：RAG 向量检索原理、并发模型（GIL）、API 鲁棒性。
- [x] 验证简历 PDF 刷新成功，项目证据链已统一至 `ScholarFlow + Doubao + multi-agent-skills-catalog`。
- [x] 生成本次 handoff。

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 停止看长文档，转向“救火模式”问答 | 继续按 Checklist 刷 GitHub 真题；直接进行考点互考 | 距离开考不足 3 小时，用户感到“看不进去”，口头问答和比喻记忆效率更高 |
| 重点挖掘 `doubao-batch-translator` 细节 | 只用 `ScholarFlow` 一个项目；加入 Doubao 细节 | 后者提供了更多“工程稳定性”和“大模型降级”的真实证据，符合阿里 AI 应用岗的偏好 |

## Pending Work

### Immediate Next Steps

1. **考前 30 分钟：** 扫一遍 `docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md` 里的加粗部分。
2. **笔试中：** 遇到算法题先判题型（滑窗/二分/哈希），先把 $O(N)$ 或 $O(N \log N)$ 的思路理顺再动手。
3. **笔试后：** 记录下没见过的知识点或做不出来的编程题，方便回来复盘小红书和蚂蚁。

### Blockers/Open Questions

- [ ] 当前阿里和蚂蚁的 `generate_*.py` 脚本数据仍未同步，但在考试前不建议处理，因为 PDF 已经生成好了。

## Context for Resuming Agent

### Important Context

用户即将在 2026-03-28 14:00 参加阿里笔试。当前的复习状态是：基础知识已用“比喻法”过了一遍，心态从焦虑转向积极抢分。如果用户在笔试后回来，**第一件事应该是帮他复盘**。重点关注他提到的“没见过的题”，那大概率是接下来小红书（29日）和蚂蚁的重点。

### Assumptions Made

- 用户已经下载或打印了最新的简历 PDF。
- 用户理解了“最左前缀原则”、“缓存击穿”和“进程/线程工厂比喻”。

## Environment State

### Tools/Services Used

- `session-handoff` skill: 用于创建、填写和验证本交接文档。
- `write_file`: 用于更新文档内容。

## Related Resources

- [.claude/handoffs/2026-03-28-113912-exam-prep-resume-refresh.md](.claude/handoffs/2026-03-28-113912-exam-prep-resume-refresh.md)
- [阿里笔试临考速记卡](../../docs/temp/2026-03-28-alibaba-ant-last-minute-notes.md)
- [最新版阿里 PDF](../../resumes/sources/刘新宇-阿里巴巴-AI应用研发工程师.pdf)
