# Handoff: CCR Provider Registration Fix and AIHubMix Key Validation

## Session Metadata
- Created: 2026-03-30 01:31:13
- Project: /home/louis/internship-jd-catalog
- Branch: codex/resume-generator-sync
- Session duration: ~90 minutes

### Recent Commits (for context)
  - cba90e3 fix(resume): track generator sources and sync tailored drafts
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic

## Handoff Chain

- **Continues from**: [2026-03-30-010606-troubleshooting-claude-code-router.md](./2026-03-30-010606-troubleshooting-claude-code-router.md)
  - Previous title: Troubleshooting Claude Code Router and Model Switching
- **Supersedes**:
  - [2026-03-30-010547-claude-code-router-config-fix.md](./2026-03-30-010547-claude-code-router-config-fix.md)
  - [2026-03-30-010606-troubleshooting-claude-code-router.md](./2026-03-30-010606-troubleshooting-claude-code-router.md)

## Current State Summary

本次会话彻底厘清了 Claude Code Router 当前的核心问题。`Model 'aihubmix,coding-glm-5-free' not found` 不是 Claude Code 本地校验导致，也不是 AIHubMix model 名错误，而是 CCR 运行时根本没有把 provider 注册进去。根因是当前本机安装的 `claude-code-router 2.0.0` 在 provider 初始化阶段仍读取旧字段 `api_base_url` / `api_key`，而用户配置里大多只有 `baseUrl` / `apiKey`。我已在 `/home/louis/.claude-code-router/config.json` 为所有 provider 补齐兼容字段，并将 AIHubMix key 更新为用户提供的有效 key。现在 `/providers` 已恢复为 9 个 provider，`openrouter` 请求可正常返回消息，`aihubmix,coding-glm-5-free` 不再报 not found，而是进入上游后返回 `429 free model quota`。当前剩余阻塞不是 CCR，而是 AIHubMix 免费额度。

## Codebase Understanding

### Architecture Overview

这里涉及的是仓库外的本机配置和本机安装的 CCR，而不是 `internship-jd-catalog` 仓库代码本身。排障链路分成两层：

1. `/home/louis/.claude-code-router/config.json` 是磁盘配置来源，`/api/config` 反映的是这层内容。
2. CCR 启动后会通过 `ProviderService` 真正注册 provider，运行时的 `/providers` 才代表实际可用 provider 列表。

本次根因在于这两层出现了“表面有配置，运行时没注册”的分裂：

- `/api/config` 一直能看到 `aihubmix`
- 但修复前 `/providers` 返回 `0`
- 因此任何 `provider,model` 形式的 `/v1/messages` 请求都会在 `providerService.getProvider(providerName)` 阶段失败，报 `Provider 'xxx' not found`

另外，AIHubMix key 是否有效不能只看 CCR 报错，应该直接用官方 API 验证；本次直接请求 `https://aihubmix.com/v1/models` 已返回 `200`，并确认目标模型存在。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `/home/louis/.claude-code-router/config.json` | CCR 主配置文件 | 本次所有修复都在这里完成，包含 provider 兼容键和 AIHubMix key |
| `/home/louis/.claude-code-router/config.json.codex-pre-aihubmix-compat.bak` | 兼容键修复前备份 | 回滚参考点 |
| `/home/louis/.claude-code-router/config.json.pre-user-aihubmix-key.bak` | 写入用户提供 key 前备份 | 回滚参考点 |
| `.claude/handoffs/2026-03-30-010606-troubleshooting-claude-code-router.md` | 上一份 CCR handoff | 本次修复直接承接它，但其中关于“provider not found”的描述已过时 |
| `.claude/handoffs/2026-03-30-013113-ccr-provider-registration-aihubmix-key-fix.md` | 当前 handoff | 后续接手应以本文件为准 |

### Key Patterns Discovered

- 在当前 `claude-code-router 2.0.0` 环境下，provider 配置要同时保留 `baseUrl/apiKey` 和 `api_base_url/api_key` 两套字段，才能同时兼容 UI 展示和运行时注册。
- `/api/config` 不能证明 provider 已可用；需要看 `/providers`，或者直接测 `/v1/messages`。
- 对第三方 provider 的“key 是否有效”要独立做官方 API 直连验证，不要只看代理层错误。
- AIHubMix 免费模型的 429 表示额度或并发限制，不是 key 无效。

## Work Completed

### Tasks Finished

- [x] 读取并核对前序 handoff，确认当前问题链路
- [x] 复现 `Model 'aihubmix,coding-glm-5-free' not found`
- [x] 通过 CCR 日志证明请求已进入 CCR，但在 provider 查找阶段失败
- [x] 对比 `/api/config` 与 `/providers`，确认“磁盘配置存在但运行时未注册 provider”
- [x] 查官方文档和官方源码，定位到当前运行时仍读取 `api_base_url/api_key`
- [x] 为 `/home/louis/.claude-code-router/config.json` 的所有 provider 补齐兼容字段
- [x] 重启 CCR，并验证 `/providers` 从 `0` 恢复到 `9`
- [x] 验证 `openrouter,openrouter/free` 能返回正常消息结构
- [x] 核对用户提供的 AIHubMix key 与当前配置不同
- [x] 直连 `https://aihubmix.com/v1/models` 验证用户提供的 key 有效，且目标模型存在
- [x] 将用户提供的 AIHubMix key 写入 CCR 配置
- [x] 再次重启 CCR，验证 `aihubmix,coding-glm-5-free` 已不再报 not found，而是报 `429 free model quota`
- [x] 创建并填写新的 session handoff

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `/home/louis/.claude-code-router/config.json` | 为全部 provider 补齐 `api_base_url/api_key` 兼容键，并将 `aihubmix` 的 `apiKey/api_key` 更新为用户提供的有效 key | 修复 CCR 运行时 provider 注册失败，并同步正确的 AIHubMix 凭据 |
| `/home/louis/.claude-code-router/config.json.codex-pre-aihubmix-compat.bak` | 新增备份 | 保留补兼容键前的回滚点 |
| `/home/louis/.claude-code-router/config.json.pre-user-aihubmix-key.bak` | 新增备份 | 保留写入用户提供 key 前的回滚点 |
| `.claude/handoffs/2026-03-30-013113-ccr-provider-registration-aihubmix-key-fix.md` | 新增 handoff | 为下一位 agent 记录当前真实状态和下一步 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 先查运行时证据，再改配置 | 直接猜测模型名问题 / 直接改默认模型 / 先查日志和 API | 先锁定 root cause，避免继续在模型名或 CLI 本地校验上绕圈 |
| 先补兼容键，再考虑升级 CCR | 立刻升级包 / 在现有版本修复配置 | 当前问题已能通过配置兼容修复，风险和改动面都更小 |
| 将所有 provider 都补齐旧字段，而不是只修 `aihubmix` | 只修单一 provider / 全量补齐 | 根因影响所有 provider，`/providers=0` 说明不是单一 provider 问题 |
| 暂不切换 `Router.default` | 立刻把默认模型改去 AIHubMix / 保持现状 | AIHubMix 免费额度已触发 429，贸然改默认只会把默认路由切到一个当前不可用模型 |
| 单独验证 AIHubMix key | 只看 CCR 错误 / 直接请求官方 API | 这样可以把“key 是否有效”和“代理层是否配置正确”彻底分离 |

## Pending Work

### Immediate Next Steps

1. 让用户决定是否把 `Router.default` 从当前 `zhipu,glm-4.7-flash` 切到一个已验证可用的 provider/model，或仅配置 fallback。
2. 如果用户还想继续用 AIHubMix 免费模型，确认是等待免费额度恢复，还是改用 AIHubMix 付费模型。
3. 如果用户希望 `opencode` 侧也使用同一把 AIHubMix key，需要单独检查 `/home/louis/.config/opencode/opencode.json`，本次未动它。

### Blockers/Open Questions

- [ ] Blocker: `aihubmix,coding-glm-5-free` 当前返回 `429 free model quota` - Needs: 等额度恢复，或切换到付费模型/其他 provider
- [ ] Question: 是否要把 `Router.default` 改成已验证可用的 `openrouter` 或其他 provider - Suggested: 先由用户拍板默认路由策略
- [ ] Question: 是否要同步修正 `opencode` 相关配置 - Suggested: 仅在用户明确要求后再做，避免扩大范围

### Deferred Items

- 升级 `claude-code-router` 到支持纯 camelCase provider 配置的版本（如果后续确认为官方已修复）
- 清理或脱敏旧 handoff 中可能存在的明文 key 记录

## Context for Resuming Agent

### Important Context

最重要的结论有四个：

1. `Model 'aihubmix,coding-glm-5-free' not found` 已经不是当前问题。
2. 当前 CCR 的 provider 注册已经恢复正常，证据是 `/providers` 现在返回 9 个 provider。
3. 用户给的 AIHubMix key 是有效的；此前 401 是因为配置里存的是另一把错误的 key。
4. AIHubMix 当前剩下的是 `429 free model quota`，不是 key 失效，也不是 model 不存在。

接手时不要再把时间花在“模型名是不是写错”“Claude Code 本地是不是不认这个模型”这类假设上。本次已经证明：

- 请求能进入 CCR
- provider 注册问题已修复
- model 存在
- key 有效
- 当前仅剩上游额度限制

另外有两个容易踩坑的上下文：

- 这个仓库本地没有 `create_handoff.py` / `validate_handoff.py` 等脚本；本次是用 `/home/louis/.codex/skills/session-handoff/scripts/` 下的脚本创建和校验 handoff。
- 当前 git worktree 很脏，而且绝大多数改动与本次 CCR 任务无关。接手时不要回滚这些改动。

### Assumptions Made

- 用户暂时没有要求同步修改 `opencode` 侧配置，所以本次只修了 CCR。
- 用户当前更在意“让 CCR 能正常工作”而不是“立刻改默认路由策略”。
- AIHubMix 429 是免费额度限制而非账号封禁，因为 `/v1/models` 可正常返回。

### Potential Gotchas

- 只保留 `baseUrl/apiKey` 会让 UI 看起来正常，但当前运行时仍可能不注册 provider；兼容期间不要去掉 `api_base_url/api_key`。
- `/api/config` 和 `/providers` 可能给出相互矛盾的信号，排障时以 `/providers` 和真实请求为准。
- AIHubMix key 不能写进 handoff；本文件故意只写结论，不记录明文。
- 旧 handoff 里有内容已经过时，尤其是“provider not found 还未解决”的描述；后续以本文件为准。

## Environment State

### Tools/Services Used

- `claude-code-router 2.0.0`: 当前实际排障对象
- `Claude Code 2.1.87`: 请求入口
- `curl` / `jq`: 直接验证 `/api/config`、`/providers`、`/v1/messages`
- `node` / `python`: 对本机 JSON 配置做最小化读写和官方 API 验证
- Context7 + GitHub 官方源码: 用于交叉验证文档与实现的差异

### Active Processes

- `claude-code-router` 正在运行，PID `223154`
- 监听地址：`http://127.0.0.1:3456`

### Environment Variables

- 本次未依赖额外环境变量；关键凭据直接来自 `/home/louis/.claude-code-router/config.json`

## Related Resources

- `.claude/handoffs/2026-03-30-010547-claude-code-router-config-fix.md`
- `.claude/handoffs/2026-03-30-010606-troubleshooting-claude-code-router.md`
- `/home/louis/.claude-code-router/config.json`
- `/home/louis/.codex/skills/session-handoff/scripts/create_handoff.py`
- `/home/louis/.codex/skills/session-handoff/scripts/validate_handoff.py`
- Official docs: https://github.com/musistudio/claude-code-router/blob/main/docs/docs/cli/config/basic.md
- Official source: https://github.com/musistudio/claude-code-router/blob/main/packages/core/src/services/provider.ts

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
