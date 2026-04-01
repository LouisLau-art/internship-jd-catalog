# Handoff: Oh-My-OpenCode Free Models Configuration

## Session Metadata
- Created: 2026-03-30 00:46:11
- Project: /home/louis/internship-jd-catalog
- Branch: codex/resume-generator-sync
- Session duration: ~45 minutes

### Recent Commits (for context)
  - cba90e3 fix(resume): track generator sources and sync tailored drafts
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic

## Handoff Chain

- **Continues from**: [2026-03-30-003236-algorithm-skills-selection.md](./2026-03-30-003236-algorithm-skills-selection.md)
  - Previous title: Algorithm Skills Selection & Installation
- **Supersedes**: [2026-03-29-201545-oh-my-opencode-configuration.md](./2026-03-29-201545-oh-my-opencode-configuration.md)

> Review the previous handoff for full context before filling this one.

## Current State Summary

完成了 oh-my-opencode 插件的配置优化，将各个 agent 的模型从 OpenRouter 免费模型升级为 AIHubMix 免费模型。AIHubMix 提供更多免费模型选择（21个），包括专门的 coding 模型（coding-glm-5-free, coding-minimax-m2.5-free 等）。根据每个 agent 的角色特点分配了最适合的免费模型，并同步配置到 opencode.json 和 claude-code-router/config.json。

## Codebase Understanding

### Architecture Overview

本项目是实习职位目录和简历生成工具，本次会话主要在配置层面进行调整，未修改现有代码结构。重点是 AI 工具链的模型配置优化。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| ~/.config/opencode/opencode.json | OpenCode provider 配置 | volcengine, openrouter, aihubmix 三个 provider |
| ~/.config/opencode/oh-my-opencode.json | Oh-my-opencode agent 模型覆盖 | 18 个 agent/category 的模型分配 |
| ~/.claude-code-router/config.json | Claude Code Router provider 配置 | 同步所有 provider 和模型 |

### Key Patterns Discovered

- AIHubMix 免费模型比 OpenRouter 更丰富，有专门的 coding 模型
- 不同 agent 角色需要不同模型（编程需强推理，探索需代码理解，简单任务用轻量模型）
- 模型名称应统一使用英文（Free 而非 (免费)）
- venice provider 只有 gemini 3 flash preview 免费，不值得保留

## Work Completed

### Tasks Finished

- [x] 安装 oh-my-opencode 插件（使用 bunx，无订阅）
- [x] 配置 volcengine provider（4 个 doubao 2.0 模型）
- [x] 配置 openrouter provider（8 个免费模型）
- [x] 删除 venice provider（只有 gemini 3 flash preview 免费）
- [x] 配置 AIHubMix provider（21 个免费模型）
- [x] 将 oh-my-opencode agents 从 gpt-5-nano 替换为不同免费模型
- [x] 根据 agent 角色特点分配最佳免费模型
- [x] 同步所有配置到 claude-code-router/config.json
- [x] 将模型名称中的中文 (免费) 改为英文 Free

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| ~/.config/opencode/opencode.json | 添加 volcengine, openrouter, aihubmix provider | 用户请求配置这些 provider |
| ~/.config/opencode/oh-my-opencode.json | 替换所有模型为 AIHubMix 免费模型 | 原用 opencode/gpt-5-nano，需要更好的免费模型 |
| ~/.claude-code-router/config.json | 同步 provider 和模型配置 | 用户要求同步配置 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| **选择 AIHubMix 替代 OpenRouter** | OpenRouter / AIHubMix | AIHubMix 有更多免费模型，特别是 coding 专用模型 |
| **删除 venice provider** | 保留 / 删除 | venice 只有 gemini 3 flash preview 免费，不值得保留 |
| **不同 agent 使用不同模型** | 统一模型 / 分配模型 | 不同角色需求不同，编程需强推理，探索需代码理解 |
| **模型名称使用英文** | 中文 (免费) / 英文 Free | 用户明确要求使用英文 |

## Pending Work

### Immediate Next Steps

1. 测试配置是否正常工作（用 opencode 发送测试消息）
2. 验证各 agent 是否正确使用分配的模型
3. 如有性能问题，可调整模型分配

### Blockers/Open Questions

- 无

### Deferred Items

- 无

## Context for Resuming Agent

### Important Context

**当前配置状态：**
- oh-my-opencode 已安装并配置完成
- 18 个 agent/category 已分配免费模型
- volcengine、openrouter、aihubmix provider 已配置在 opencode.json
- claude-code-router 也已同步配置
- 所有模型名称已改为英文（Free 而非 (免费)）

**模型分配详情：**
- hephaestus (代码生成): aihubmix/coding-glm-5.1-free
- oracle (复杂推理): aihubmix/coding-glm-5.1-free
- librarian (研究查文档): aihubmix/coding-minimax-m2.7-free
- explore (代码探索): aihubmix/coding-glm-5-free
- multimodal-looker (多模态): aihubmix/gemini-3-flash-preview-free
- prometheus/metis (规划): aihubmix/coding-minimax-m2.5-free
- momus (评审): aihubmix/coding-minimax-m2.7-free
- atlas (超长context): aihubmix/coding-glm-5.1-free
- sisyphus-junior (综合): aihubmix/coding-minimax-m2.5-free
- quick/unspecified-low (简单任务): aihubmix/glm-4.7-flash-free
- visual-engineering (UI/UX): aihubmix/gemini-2.5-flash-free

**Provider 配置：**
- volcengine: 4 doubao 2.0 models
- openrouter: 8 free models
- aihubmix: 21 free models

**API Key 信息（已配置在文件中）：**
- volcengine: (redacted - configured locally)
- openrouter: (redacted - configured locally)
- aihubmix: (redacted - configured locally)

### Assumptions Made

- 用户会测试配置是否正常工作
- AIHubMix 免费模型的限速（每分钟 5 次，每天 500 次，100 万 Token/天）对当前使用足够
- 不同 agent 使用不同模型不会导致性能问题

### Potential Gotchas

- AIHubMix 免费模型有限速，大量使用可能需要等待
- coding-glm-5.1-free 是新模型，可能稳定性不如成熟模型
- gemini-3-flash-preview-free 多模态能力可能有限

## Environment State

### Tools/Services Used

- opencode: AI coding agent 工具
- bunx: 用于安装 oh-my-opencode 插件
- curl: 用于测试 API 调用
- jq: 用于解析 JSON 配置

### Active Processes

- 无

### Environment Variables

- 无（API Key 已直接配置在文件中）

## Related Resources

- [AIHubMix 免费模型列表](https://aihubmix.com) - 所有免费模型的详细信息
- [OpenRouter 免费模型](https://openrouter.ai/collections/free-models) - OpenRouter 的免费模型
- [Oh-My-OpenCode 文档](https://github.com/code-yeongyu/oh-my-openagent) - 插件官方文档
- [OpenCode 配置文档](https://opencode.ai/docs/config) - OpenCode 配置说明

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
