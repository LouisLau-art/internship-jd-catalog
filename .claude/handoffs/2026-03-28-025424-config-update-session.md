# Handoff: 全局配置与模型路由更新

## Session Metadata
- Created: 2026-03-28 02:54:24
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: ~30 分钟

### Recent Commits (for context)
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic
  - 7265dc8 feat(sync): add markdown dashboard synchronization logic

## Handoff Chain

- **Continues from**: [2026-03-28-022941-two-stage-campus-job-workflow.md](./2026-03-28-022941-two-stage-campus-job-workflow.md)
  - Previous title: 两段式大厂抓岗与选岗简历工作流落地
- **Supersedes**: None

## Current State Summary

本次会话主要完成了三项配置更新工作：(1) 检查并更新了 bun 全局安装的 19 个包至最新版本；(2) 探索了 GitHub 官方的 spec-kit 项目（规范驱动开发工具包）；(3) 在全局配置和路由配置中添加了智谱AI GLM 免费模型支持。所有配置文件已更新完毕，用户需要自行填写智谱 API Key。

## Codebase Understanding

### Architecture Overview

项目的全局配置架构：
```
~/.claude/CLAUDE.md ─────┐
~/.gemini/GEMINI.md ────┼──→ /home/louis/context7-skills-curated-pack/global-context/AGENTS.md (唯一真源)
~/.codex/AGENTS.md ─────┘

~/.claude-code-router/config.json ──→ 独立的路由配置，控制模型切换
```

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `/home/louis/context7-skills-curated-pack/global-context/AGENTS.md` | 三端共享的全局指令文件 | 所有 Agent 行为规范的唯一真源 |
| `~/.claude-code-router/config.json` | Claude Code Router 模型路由配置 | 控制模型切换、Provider 定义 |
| `~/.codex/AGENTS.md` | Codex CLI 配置入口 | 符号链接，实际指向上述 AGENTS.md |

### Key Patterns Discovered

1. **配置文件命名**：Codex CLI 使用 `AGENTS.md`（带 S），而非 `AGENT.md`
2. **符号链接架构**：三个平台的配置文件都是符号链接，指向同一个源文件，保持三端同步
3. **Router 配置结构**：`Providers` 数组定义 API 端点，`Router` 对象定义默认路由

## Work Completed

### Tasks Finished

- [x] 检查 npm 全局包（仅有 npm 自身）
- [x] 更新 bun 全局包至最新版本（19 个包）
- [x] 使用 GitHub MCP 查看 github/spec-kit 项目
- [x] 在 AGENTS.md 中添加 GitHub 网址处理规则
- [x] 删除多余的 ~/.codex/AGENT.md 符号链接
- [x] 在 AGENTS.md 中添加智谱AI GLM 模型配置信息
- [x] 在 ~/.claude-code-router/config.json 中添加 zhipu provider

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `/home/louis/context7-skills-curated-pack/global-context/AGENTS.md` | 添加 GitHub 规则和智谱AI模型配置 | 统一三端配置 |
| `~/.claude-code-router/config.json` | 添加 zhipu provider | 支持智谱免费模型路由 |
| `~/.codex/AGENT.md` | 删除此多余符号链接 | 仅保留 AGENTS.md |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 使用 AGENTS.md 而非 AGENT.md | AGENT.md / AGENTS.md | Context7 文档确认 Codex CLI 使用 AGENTS.md |
| 配置放在 AGENTS.md vs config.json | 两者都更新 | AGENTS.md 用于行为指令，config.json 用于模型路由 |
| 智谱模型添加到独立 provider | 添加到 ModelScope / 新建 zhipu | 独立 provider 更清晰，便于管理 API Key |

## Pending Work

### Immediate Next Steps

1. 用户需前往 https://bigmodel.cn/usercenter/proj-mgmt/apikeys 获取智谱 API Key
2. 替换 `~/.claude-code-router/config.json` 中的 `<填写你的智谱API Key>`
3. 使用 `/model zhipu,glm-4.7-flash` 测试模型切换

### Blockers/Open Questions

- [ ] 智谱 API Key 尚未填写，无法测试连接

### Deferred Items

- 无

## Context for Resuming Agent

### Important Context

1. **三端配置同步机制**：修改 `/home/louis/context7-skills-curated-pack/global-context/AGENTS.md` 即可同步更新 Claude、Gemini、Codex 三个平台的配置
2. **模型路由配置分离**：全局行为指令在 AGENTS.md，但模型路由必须在 `~/.claude-code-router/config.json` 中配置
3. **智谱免费模型**：`glm-4.7-flash` 和 `glm-4.6v-flash`（视觉多模态）是免费的

### Assumptions Made

- 用户会自行获取并填写智谱 API Key
- 智谱 API 兼容 OpenAI 格式（使用 `OpenAI` transformer）

### Potential Gotchas

- 不要误创建 `AGENT.md`，正确文件名是 `AGENTS.md`
- 修改配置后无需重启服务，claude-code-router 会自动加载
- 智谱 API Base URL 是 `https://open.bigmodel.cn/api/paas/v4/chat/completions`

## Environment State

### Tools/Services Used

- `bun pm list -g` - 查看/更新 bun 全局包
- GitHub MCP (`mcp__plugin_github_github__*`) - 查看 GitHub 项目
- Context7 MCP (`mcp__context7__*`) - 查询库文档
- claude-code-router - 模型路由服务（端口 3456）

### Active Processes

- claude-code-router 服务运行在 127.0.0.1:3456

### Environment Variables

- 无特殊环境变量变更

## Related Resources

- 智谱 API Key 获取：https://bigmodel.cn/usercenter/proj-mgmt/apikeys
- 智谱 API 文档：https://bigmodel.cn/dev/api/normal-model/glm-4
- claude-code-router 文档：https://github.com/musistudio/claude-code-router
- GitHub spec-kit 项目：https://github.com/github/spec-kit

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.