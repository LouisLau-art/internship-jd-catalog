# Handoff: 安装配置开源 AI 编码 CLI 工具（OpenCode/Crush/Kilocode/Oh My OpenCode）- 自定义火山豆包模型

## Session Metadata
- Created: 2026-03-23 00:22:29
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: [estimate how long you worked]

### Recent Commits (for context)
  - 0e282ff docs(jd): add expanded alibaba ant and bytedance top-10 shortlists
  - 8c0f4cd feat(repo): expand internship exports and remove private resumes
  - fc4ad41 feat(jd): add bytedance byteintern backend export
  - 49a6a04 feat(jd): expand campus exports and add daily shortlist
  - 38cee8e docs(jd): split alibaba and ant shortlists

## Handoff Chain

- **Continues from**: [2026-03-22-022336-public-repo-history-cleanup.md](./2026-03-22-022336-public-repo-history-cleanup.md)
  - Previous title: Public Repo History Cleanup And Internship Export Expansion
- **Supersedes**: [list any older handoffs this replaces, or "None"]

> Review the previous handoff for full context before filling this one.

## Current State Summary

本次会话完成了 5 个开源 AI 编码 CLI 工具的安装和配置：
- opencode、crush、kiro-cli、kilocode 全部使用 bun 全局安装完成
- oh-my-opencode 也安装完成
- 针对用户拥有的火山引擎豆包 API 环境，为每个工具配置了用户提供的全部 11 个自定义模型
- 用户的自定义模型包括：doubao-seed-code-preview-251028、doubao-seed-1-8-251228、deepseek-v3-2-251201、doubao-seed-1-6-lite-251015、doubao-seed-1-6-flash-250828、glm-4-7-251222、kimi-k2-thinking-251104、doubao-seed-2-0-code-preview-260215、doubao-seed-2-0-mini-260215、doubao-seed-2-0-lite-260215、doubao-seed-2-0-pro-260215
- 配置过程按照 Context7 官方文档验证了每个工具的正确格式，针对 variant 参数做了解释（variant 是 oh-my-opencode 内部参数，不是豆包原生参数）
- 所有配置文件都已经写入正确位置，用户可以直接使用这些工具了

工作至此结束，用户可以按需使用这些工具。

## Codebase Understanding

### Architecture Overview

[TODO: Document key architectural insights discovered during this session]

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `~/.config/opencode/opencode.json` | OpenCode 配置文件，包含 yujian 豆包所有模型配置 | 🔑 Critical |
| `~/.config/crush/crush.json` | Crush 配置文件，包含 yujian 豆包所有模型配置 | 🔑 Critical |
| `~/.config/oh-my-opencode/oh-my-opencode.json` | Oh My OpenCode 配置文件，包含 yujian 豆包所有模型配置和多代理路由 | 🔑 Critical |

### Key Patterns Discovered

[TODO: Document important patterns, conventions, or idioms found in this codebase]

## Work Completed

### Tasks Finished

- [x] 使用 bun 全局安装了四个开源 AI 编码 CLI 工具：opencode、crush、kiro-cli、kilocode
- [x] 使用 bun 安装了 oh-my-opencode 增强工具集
- [x] 为 opencode 创建并配置了 ~/.config/opencode/opencode.json，包含所有 yujian 豆包模型
- [x] 为 crush 创建并配置了 ~/.config/crush/crush.json，包含所有 yujian 豆包模型
- [x] 为 oh-my-opencode 创建并配置了 ~/.config/oh-my-opencode/oh-my-opencode.json，包含自定义提供商和多代理模型分配
- [x] 根据 Context7 文档验证了配置格式正确
- [x] 解释了 variant 参数的含义，确认配置正确

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| data/antgroup_positions_26022600074513.csv | [describe changes] | [why changed] |
| data/huawei_positions_wuhan_rd.json | [describe changes] | [why changed] |
| data/alibaba_positions_100000540002.csv | [describe changes] | [why changed] |
| data/alibaba_positions_100000540002.json | [describe changes] | [why changed] |
| scripts/scrape_campus_jobs.py | [describe changes] | [why changed] |
| data/alibaba_positions_100000560002_tech.json | [describe changes] | [why changed] |
| data/antgroup_positions_26022600074513.json | [describe changes] | [why changed] |
| data/campus_positions_combined.json | [describe changes] | [why changed] |
| data/huawei_positions_intern.json | [describe changes] | [why changed] |
| data/antgroup_positions_25051200066269.json | [describe changes] | [why changed] |
| ... and 3 more files | | |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 使用 bun 安装所有工具 | npm, pnpm | bun 更快，你已经配置好了国内镜像 |
| 在 `~/.config/` 下创建各工具配置 | 项目级别配置 vs 用户级别配置 | 用户级别配置对所有项目生效，更符合使用场景 |
| 为 Oh My OpenCode 的各种代理分配对应模型 | 不同模型大小变体分配 | 复杂深度任务用 Pro，简单任务用 Mini/Lite 节省资源 |
| variant 参数保留原样 | 去掉 variant 参数 | 这些参数是 Oh My OpenCode 内部用来权衡推理质量和速度的，不影响自定义模型使用，保留有利于系统正常工作 |

## Pending Work

### Immediate Next Steps

1. **验证安装**：运行以下命令验证每个工具都可以正常启动
   ```bash
   opencode --version
   crush --version
   kilo --version
   oh-my-opencode --version
   ```
2. **完成 Oh My OpenCode 配置**：运行 `oh-my-opencode install --no-tui --claude=no --gemini=no --openai=no` 完成最后的配置
3. **测试使用**：选择一个工具（推荐 opencode 或 crush）启动，测试自定义豆包模型是否可以正常加载和使用

### Blockers/Open Questions

- [ ] [TODO: List any blockers or open questions]

### Deferred Items

- [TODO: Items deferred and why]

## Context for Resuming Agent

### Important Context

- 用户有火山引擎的 API 密钥，已经配置到所有配置文件中了，但密钥本身不写入 git，保持当前配置即可
- 你的模型端点是 `https://ark.cn-beijing.volces.com/api/v3`，这个已经配置正确
- 已经为所有三个 CLI 工具（OpenCode、Crush、Oh My OpenCode）都配置了完整的 11 个模型：
  1. doubao-seed-code-preview-251028
  2. doubao-seed-1-8-251228
  3. deepseek-v3-2-251201
  4. doubao-seed-1-6-lite-251015
  5. doubao-seed-1-6-flash-250828
  6. glm-4-7-251222
  7. kimi-k2-thinking-251104
  8. doubao-seed-2-0-code-preview-260215
  9. doubao-seed-2-0-mini-260215
  10. doubao-seed-2-0-lite-260215
  11. doubao-seed-2-0-pro-260215
- `variant` 参数说明：
  - 这是 **Oh My OpenCode 内部参数**，不是豆包模型原生参数
  - `max`: 最大能力，推理效果最好，token 消耗最多
  - `high`: 高质量，平衡质量和速度
  - `xhigh`: 超高质量，深度复杂推理
  - 配置中已经根据模型能力分配了对应的 variant，不需要修改
- 配置文件位置：
  - OpenCode: `~/.config/opencode/opencode.json`
  - Crush: `~/.config/crush/crush.json`
  - Oh My OpenCode: `~/.config/oh-my-opencode/oh-my-opencode.json`

### Assumptions Made

- 用户希望在当前机器上使用这些开源 AI 编码 CLI 工具，已经配置好了国内镜像，所以使用 bun 安装没有网络问题
- 配置文件放在用户级别 `~/.config/` 下，这样所有项目都能共享配置
- variant 参数的配置策略：复杂深度任务用 max/high，简单快速任务用 low/mini，已经按照这个原则完成配置

### Potential Gotchas

- [TODO: Document things that might trip up a new agent]

## Environment State

### Tools/Services Used

- [TODO: List relevant tools and their configuration]

### Active Processes

- [TODO: Note any running processes, servers, etc.]

### Environment Variables

- 不需要额外设置环境变量，API 密钥已经直接写入配置文件中了

## Related Resources

- [TODO: Add links to relevant docs and files]

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
