# Handoff: ByteDance Seed 简历生成与求职同步自动化

## Session Metadata
- Created: 2026-03-27 08:34:18
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: 2.5 小时

### Recent Commits (for context)
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic
  - 7265dc8 feat(sync): add markdown dashboard synchronization logic
  - 653ed55 refactor(mail): implement local-first header audit engine
  - f3def60 docs(plan): add automated job sync system design and secure .env

## Handoff Chain

- **Continues from**: [2026-03-26-173543-job-search-progress-update-resume-organization.md](./2026-03-26-173543-job-search-progress-update-resume-organization.md)
  - Previous title: 求职进度更新与简历目录整理
- **Supersedes**: None

## Current State Summary

本会话完成了简历目录的极致清理、ByteDance Seed 团队顶级简历的生成以及 `/sync-jobs` 自动化系统的全链路部署。通过分析 `report.html`，识别并沉淀了 **AI 原生研发证据挖掘** 工作流。目前，求职进度看板已具备一键同步 QQ 邮箱面试邀请的能力，字节跳动 Seed 团队的高端简历已就绪并存入 `resumes/sources/`。

## Codebase Understanding

### Architecture Overview

- **数据层**：`data/` 目录仍存储原始岗位数据，但小米数据目前主要通过脚本硬编码和文档记录。
- **工具层**：简历脚本迁移至 `resumes/scripts/`，生成的 PDF 统一存放于 `resumes/sources/`（中文命名）。
- **自动化层**：新增 `/sync-jobs` Custom Skill，通过本地正则审计（Local Header Audit）绕过 IMAP 编码顽疾。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `CLAUDE.md` | 核心工作流定义 | 🔑 新增了 Recommended Workflow |
| `.claude/skills/job-sync/SKILL.md` | 自动化同步指令 | 🛠️ 定义了 `/sync-jobs` |
| `scripts/parse_qq_job_emails.py` | 邮件审计引擎 | 🛠️ 重构为本地审计逻辑 |
| `scripts/sync_md_dashboard.py` | 看板对齐工具 | 🛠️ 实现表格去重同步 |
| `resumes/scripts/` | 简历生成脚本目录 | 📂 统一管理生成逻辑 |
| `resumes/sources/` | PDF 简历成品目录 | 📂 仅包含中文名 PDF |
| `.env` | 隐私凭证 | 🔒 存储 QQ 授权码（Git 已忽略） |

### Key Patterns Discovered

- **Deep Diver 审计**：生成高端 AI 岗位简历时，必须强制检索 Handoff 全文提取“修复逻辑”证据。
- **本地过滤优先**：IMAP 协议在处理中文字符搜索时极不可靠，应拉取 metadata 后由 Python 本地过滤。

## Work Completed

### Tasks Finished

- [x] 清理 `Downloads` 临时目录，备份笔记至 `resumes/notes/`。
- [x] 重构简历目录架构：`resumes/scripts/` (脚本), `resumes/sources/` (PDF), `resumes/others/` (归档)。
- [x] 分析 `report.html` 并更新 `CLAUDE.md` 推荐流。
- [x] 创建 `ai-native-resume-generation` Skill (Deep Diver 模式)。
- [x] 生成 `刘新宇-字节跳动-Seed团队-大模型研发实习生.pdf`。
- [x] 实现并部署 `/sync-jobs` 自动化系统。

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `CLAUDE.md` | 新增 Recommended Workflow | 沉淀 AI 专家级研发习惯 |
| `scripts/parse_qq_job_emails.py` | 彻底重构 | 修复 IMAP SEARCH 编码报错 |
| `scripts/sync_md_dashboard.py` | 从无到有实现 | 自动化看板同步核心逻辑 |
| `resumes/scripts/generate_bytedance_resumes.py` | 新增 Seed 岗位配置 | 录入顶级 AI 工程证据 |
| `.gitignore` | 增加 `.env` 保护 | 确保隐私不外泄 |
| `resumes/sources/` | 物理清理与重构 | 保持目录极致纯净 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 弃用 IMAP SEARCH | 搜索模式 A (SEARCH) / B (本地审计) | B 模式能彻底解决中文编码报错 |
| 脚本零依赖解析 .env | 用 dotenv 库 / 手动解析 | 保持工具链轻量，不增加安装负担 |
| 强制中文命名 PDF | 全部保留 / 分类清理 | 提升 sources 目录的索引效率与视觉整洁 |

## Pending Work

### Immediate Next Steps

1. **配置 `.env` 并运行 `/sync-jobs`**：实战验证邮件同步效果。
2. **投递字节 Seed**：使用新生成的 `Seed团队-大模型研发实习生` 简历。
3. **挖掘小米非武汉岗位**：基于“AI 玩得溜”人设生成小米 MiMo 简历。

### Blockers/Open Questions

- [ ] 自动化同步是否能完美识别所有公司的面试邀请模板？（需通过实战积累正则）。

## Context for Resuming Agent

### Important Context

- **简历审计逻辑**：生成高端简历时，AI 必须被提醒去读 `.claude/handoffs/`，否则会忽略关键的修复逻辑证据。
- **授权码有效性**：用户的 QQ 邮箱授权码依然有效，配置 `.env` 即可一键自动化。

### Assumptions Made

- 用户偏好通过 CLI 指令（如 `/sync-jobs`）完成日常琐事。
- 简历成品必须位于 `resumes/sources/` 且只能是中文 PDF。

### Potential Gotchas

- 脚本路径变更：`generate_*.py` 现已移至 `resumes/scripts/`，运行前需注意工作目录。

## Environment State

### Tools/Services Used

- `imaplib` (Python 标准库)
- `pandoc`
- `google-chrome`

### Active Processes

- 无（自动化指令已就绪）

### Environment Variables

- `QQ_EMAIL`
- `QQ_AUTH_CODE`

## Related Resources

- `docs/plans/2026-03-26-job-sync-design.md`: 系统设计文档
- `docs/plans/2026-03-26-job-sync-implementation.md`: 实施计划
- `report.html`: AI 工具链使用数据报告
