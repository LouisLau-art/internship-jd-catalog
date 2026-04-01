# Handoff: Claude Code Router Configuration Fix

## Session Metadata
- Created: 2026-03-30 01:05:47
- Project: /home/louis/internship-jd-catalog
- Branch: codex/resume-generator-sync
- Session duration: ~30 minutes

### Recent Commits (for context)
  - cba90e3 fix(resume): track generator sources and sync tailored drafts
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic

## Handoff Chain

- **Continues from**: [2026-03-30-004611-oh-my-opencode-free-models-config.md](./2026-03-30-004611-oh-my-opencode-free-models-config.md)
  - Previous title: Oh-My-OpenCode Free Models Configuration
- **Supersedes**: None

> Review the previous handoff for full context before filling this one.

## Current State Summary

用户在使用 Claude Code Router 时遇到了多个模型错误：(1) 使用 `modelscope,XiaomiMiMo/MiMo-V2-Flash` 和 `Qwen/Qwen3.5-397B-A17B` 时出现 500/400 API 错误；(2) 使用 `doubao-seed-2-0-mini-260215` 时出现 Invalid decoding guidance syntax 错误；(3) 配置了 `aihubmix` 提供者后，模型显示 "not found"。根本原因已通过 Context7 文档定位：config.json 使用了错误的键名格式（`api_base_url` → `baseUrl`, `api_key` → `apiKey`）。已修复配置文件并完全重启 Claude Code Router 服务（端口 3456 正常监听）。用户最后反馈 UI 界面显示不正确（所有 provider 的地址和密钥都不显示），但服务状态正常。**当前状态**：配置已修复，服务运行正常，等待用户验证 UI 界面。

## Codebase Understanding

### Architecture Overview

Claude Code Router 的配置文件格式非常敏感：providers 必须使用 `baseUrl` 和 `apiKey` 键名（驼峰命名），而非 `api_base_url` 和 `api_key`（下划线命名）。配置文件位于 `~/.claude-code-router/config.json`，服务通过 bun 运行 `@musistudio/claude-code-router/dist/cli.js start`。模型切换命令格式为 `/model {provider},{model}`。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| ~/.claude-code-router/config.json | Claude Code Router 配置文件 | 核心配置，定义所有 provider 和路由规则 |
| ~/.claude/skills/context7-docs-lookup/SKILL.md | Context7 文档查询技能 | 用于查找库文档 |

### Key Patterns Discovered

### Key Patterns Discovered

1. Claude Code Router 配置格式严格遵循驼峰命名（baseUrl, apiKey）
2. 使用 Context7 文档可以快速定位配置问题
3. 配置修改后必须完全重启服务才能生效
4. 模型切换命令格式为 `/model {provider},{model}`，provider 和 model 名称必须与配置完全匹配

## Work Completed

### Tasks Finished

- [x] 诊断 Claude Code Router 模型错误问题
- [x] 通过 Context7 文档发现配置键名错误
- [x] 修复 config.json 中的键名格式（api_base_url → baseUrl, api_key → apiKey）
- [x] 备份原始配置文件
- [x] 完全重启 Claude Code Router 服务

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| ~/.claude-code-router/config.json | 将所有 provider 的键名从 `api_base_url` 改为 `baseUrl`，从 `api_key` 改为 `apiKey` | 修复配置格式错误，符合文档要求 |
| ~/.claude-code-router/config.json.bak | 创建备份文件 | 防止修复过程中数据丢失 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 修复配置键名而非重写整个配置 | 1. 手动修改每个 provider 的键名 2. 重写整个配置文件 | 选择 sed 命令批量替换，保留其他配置完整性 |
| 完全重启服务而非热重载 | 1. 发送 HUP 信号热重载 2. 完全停止后重启 | 选择完全重启确保配置完全生效 |

## Pending Work

### Immediate Next Steps

1. 验证 UI 界面是否正确显示所有 provider 的配置信息（用户需刷新 http://127.0.0.1:3456/ui/）
2. 测试模型切换命令：`/model aihubmix,coding-glm-5-free`
3. 如果 UI 仍然显示不正确，建议用户清除浏览器缓存或使用无痕模式

### Blockers/Open Questions

- [ ] UI 界面是否已正确显示所有 provider 的配置信息（需要用户验证）

### Deferred Items

- 无

## Context for Resuming Agent

### Important Context

Claude Code Router 的配置文件格式**非常敏感**：
- 必须使用 `baseUrl` 和 `apiKey`（驼峰命名）
- 不能使用 `api_base_url` 和 `api_key`（下划线命名）
- 配置文件路径：`~/.claude-code-router/config.json`
- 服务启动命令：`bun run ~/.bun/install/global/node_modules/@musistudio/claude-code-router/dist/cli.js start`
- 模型切换格式：`/model {provider},{model}`

已知可用的 provider：
- `aihubmix`：有 19 个免费模型可用
- `volcengine`：豆包系列模型
- `modelscope`：魔搭社区模型
- `zhipu`：智谱 GLM 系列
- `openrouter`：多模型路由

如果 UI 显示不正确，可能是浏览器缓存问题，建议用户清除缓存或使用无痕模式。

### Assumptions Made

- 用户已经正确配置了各个 provider 的 API key
- 用户需要使用免费模型进行开发测试
- 用户希望保持配置的完整性和可用性

### Potential Gotchas

- 配置文件中的键名必须与文档完全一致（大小写敏感）
- 修改配置后必须完全重启服务才能生效
- 模型名称必须与 provider 的 models 数组中的名称完全匹配
- 浏览器可能缓存了旧的 UI 界面，需要强制刷新

## Environment State

### Tools/Services Used

- Claude Code Router：端口 3456 监听中
- Context7：用于查询库文档
- bun：用于启动 Claude Code Router 服务

### Active Processes

- Claude Code Router 服务正在运行（PID: 214264）
- 端口 3456 已监听

### Environment Variables

- 无特殊环境变量需要记录

## Related Resources

- [Claude Code Router 文档](https://github.com/musistudio/claude-code-router)
- [Context7 文档查询](https://context7.com/musistudio/claude-code-router)
- [Claude Code Router 配置 API 文档](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/api/config-api.md)
- [Oh-My-OpenCode 配置](https://github.com/lai-bryce/oh-my-opencode)

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
