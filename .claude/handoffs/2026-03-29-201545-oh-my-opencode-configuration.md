# Handoff: Oh-My-OpenCode 配置与免费模型优化

## Session Metadata
- Created: 2026-03-29 20:15:45
- Project: /home/louis/internship-jd-catalog
- Branch: codex/resume-generator-sync
- Session duration: ~30 分钟

### Recent Commits (for context)
  - cba90e3 fix(resume): track generator sources and sync tailored drafts
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic

## Handoff Chain

- **Continues from**: [2026-03-28-231254-ccr-openrouter-gemini-provider-repair.md](./2026-03-28-231254-ccr-openrouter-gemini-provider-repair.md)
  - Previous title: 修复 Claude Code Router 的 OpenRouter 和 Gemini Provider 配置
- **Supersedes**: None

## Current State Summary

完成了 oh-my-opencode 插件的安装配置，并将各个 agent 的模型从默认的 `opencode/gpt-5-nano` 替换为 OpenRouter 的免费模型。根据每个 agent 的角色特点（代码生成、推理、探索、评审等），选择了最适合的免费模型。

## Work Completed

### Tasks Finished

- [x] 安装 oh-my-opencode 插件（使用 bunx，无订阅）
- [x] 配置 volcengine provider（4 个 doubao 2.0 模型）
- [x] 配置 openrouter provider（openrouter/free）
- [x] 删除 yujian provider 从 opencode 配置（保留在 claude-code-router）
- [x] 将 oh-my-opencode agents 从 gpt-5-nano 替换为不同免费模型
- [x] 根据 agent 角色特点分配最佳免费模型

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| ~/.config/opencode/opencode.json | 添加 volcengine 和 openrouter provider | 用户请求配置这两个 provider |
| ~/.config/opencode/oh-my-opencode.json | 替换所有模型为 OpenRouter 免费模型 | 原用 opencode/gpt-5-nano，需要更好的免费模型 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 选择 OpenRouter 免费模型而非 OpenCode 限时模型 | opencode/big-pickle vs openrouter/xxx-free | OpenRouter 免费模型更稳定，不依赖 OpenCode 订阅 |
| 不同 agent 使用不同模型 | 统一模型 vs 分配模型 | 不同角色需求不同，编程需强推理，探索需代码理解 |
| 保留 yujian 在 claude-code-router | 删除 vs 保留 | 用户说"没用"但 later 未确认删除 claude-code-router 版 |

## Configuration Details

### Final Model Allocation

```
# Agents (10个)
hephaestus        → openrouter/nvidia/nemotron-3-super-120b-a12b-free  (代码最强, Programming #4)
oracle            → openrouter/nvidia/nemotron-3-super-120b-a12b-free  (1M context, 复杂推理)
atlas             → openrouter/nvidia/nemotron-3-super-120b-a12b-free  (超长 context)
explore           → openrouter/qwen/qwen3-coder:free                  (480B 代码专用)
librarian         → openrouter/arcee-ai/trinity-large-preview:free     (512K, 综合研究)
multimodal-looker → openrouter/nvidia/nemotron-nano-12b-v2-vl:free     (多模态, OCR)
prometheus        → openrouter/stepfun/step-3.5-flash:free             (推理模型)
metis             → openrouter/stepfun/step-3.5-flash:free             (分析规划)
momus             → openrouter/arcee-ai/trinity-large-preview:free     (评审)
sisyphus-junior   → openrouter/minimax/minimax-m2.5:free              (SWE-Bench 80.2%)

# Categories (8个)
ultrabrain        → openrouter/nvidia/nemotron-3-super-120b-a12b-free  (硬核逻辑)
deep              → openrouter/nvidia/nemotron-3-super-120b-a12b-free  (深度问题)
visual-engineering→ openrouter/arcee-ai/trinity-large-preview:free     (UI/UX)
artistry          → openrouter/arcee-ai/trinity-large-preview:free     (创意)
writing           → openrouter/arcee-ai/trinity-large-preview:free     (文档)
unspecified-high  → openrouter/arcee-ai/trinity-large-preview:free     (通用高难度)
quick             → openrouter/google/gemma-3-4b-it:free              (轻量快速)
unspecified-low   → openrouter/google/gemma-3-4b-it:free              (简单任务)
```

### Provider Configuration

```json
// volcengine (opencode.json)
{
  "volcengine": {
    "models": {
      "doubao-seed-2-0-flash-32k-251128": { "name": "doubao-2.5-flash-32k" },
      "doubao-seed-2-0-pro-32k-251128": { "name": "doubao-2.5-pro-32k" },
      "doubao-seed-2-0-vod-32k-251128": { "name": "doubao-2.5-vod-32k" },
      "doubao-seed-2-0-thinking-pro-251128": { "name": "doubao-2.5-thinking-pro" }
    }
  }
}

// openrouter (opencode.json)
{
  "openrouter": {
    "models": {
      "openrouter/free": {}
    }
  }
}
```

## Important Context

**本次会话核心要点：**
1. oh-my-opencode 是一个 OpenCode 的插件，用于管理多个 AI agent
2. OpenRouter 的 `openrouter/free` 是特殊模型 ID，会自动路由到当前最佳免费模型
3. 每个 agent 角色不同，使用不同模型效果更好（代码用 nemotron-3-super，探索用 qwen3-coder）
4. 所有配置都在 `~/.config/opencode/` 目录下的 JSON 文件中

**当前状态：**
- oh-my-opencode 已安装并配置完成
- 18 个 agent/category 已分配免费模型
- volcengine 和 openrouter provider 已配置在 opencode.json

**需要继续时：**
- 直接在 OpenCode 中测试功能即可
- 如有模型性能问题，可在 `oh-my-opencode.json` 中调整

## Environment State

### Key Files

| File | Purpose |
|------|---------|
| ~/.config/opencode/opencode.json | OpenCode provider 配置 |
| ~/.config/opencode/oh-my-opencode.json | Oh-my-opencode agent 模型覆盖 |
| ~/.claude-code-router/config.json | Claude Code Router provider 配置 |

### API Keys (已配置)

- volcengine: (redacted - configured locally)
- openrouter: (redacted - configured locally)
- yujian: (redacted - kept only in local claude-code-router config)

## Pending Work

### Immediate Next Steps

1. 测试配置是否正常工作（用 opencode 发送测试消息）
2. 验证各 agent 是否正确使用分配的模型
3. 如有性能问题，可调整模型分配

### Blockers/Open Questions

- 无

### Deferred Items

- 无

## Potential Gotchas

- `openrouter/free` 是特殊路由 ID，会自动选择可用的免费模型（当前路由到 `google/gemma-3-4b-it:free`）
- OpenRouter 免费模型有限速，大量使用可能需要等待
- `minimax-m2.5:free` 在 opencode 模型列表中可能不显示，但 OpenRouter 支持
- volcengine API key 有地域限制（北京 endpoint）

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
