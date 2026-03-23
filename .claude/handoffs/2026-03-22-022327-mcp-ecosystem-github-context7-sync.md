# Handoff: Global MCP Strategy, GitHub Discovery Layer, and Context7 Key Sync

## Session Metadata
- Created: 2026-03-22 02:23:27
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: ~2.5 hours

### Recent Commits (for context)
  - 0e282ff docs(jd): add expanded alibaba ant and bytedance top-10 shortlists
  - 8c0f4cd feat(repo): expand internship exports and remove private resumes
  - fc4ad41 feat(jd): add bytedance byteintern backend export
  - 49a6a04 feat(jd): expand campus exports and add daily shortlist
  - 38cee8e docs(jd): split alibaba and ant shortlists

## Handoff Chain

- **Continues from**: None
- **Supersedes**: None

> This handoff is about user-scope AI tooling under `/home/louis`, not the internship-jd-catalog codebase itself. The earlier JD shortlist handoff in this repo is unrelated.

## Current State Summary

This session focused on user-scope MCP and agent workflow strategy across Codex, Gemini CLI, and Claude Code, not on repository code changes in `internship-jd-catalog`. The user explored which MCPs are actually worth keeping, how GitHub MCP should be scoped when GitHub is treated as a content and discovery archive, and what is interesting in the OpenCode ecosystem (`awesome-opencode`, `oh-my-opencode`). Final runtime state is synchronized across all three agents: `github` MCP is enabled as a read-only discovery layer via a shared wrapper, `Claude` no longer has `weread`, and the latest `Context7` API key is now present across Codex, Gemini, and Claude. The main unresolved decision is whether to keep the current single read-only GitHub MCP setup or add a second write-scoped `github_write` MCP for issue and PR operations.

## Codebase Understanding

### Architecture Overview

The important system here is the user's global AI-agent tooling setup rather than this repo. Each client has its own user-scope config file: Codex uses `~/.codex/config.toml`, Gemini uses `~/.gemini/settings.json`, and Claude Code uses `~/.claude.json`. GitHub MCP is intentionally centralized through a shared wrapper at `/home/louis/.local/bin/github-mcp-codex`, which pulls the GitHub token from `gh auth token`, depends on Docker, and forwards env-based tool configuration into the official GitHub MCP server container. Context7 is configured separately as an HTTP MCP in each client. The user wants all three clients to stay behaviorally synchronized, and the instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) were updated to match the actual runtime policy: GitHub MCP is for read and discovery, while `gh`, `git`, and skills remain the main execution path.

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| /home/louis/.codex/config.toml | Codex user-scope MCP config | Holds current `context7` HTTP headers and `github` wrapper env |
| /home/louis/.gemini/settings.json | Gemini CLI user-scope config | Holds `context7` key and `github` MCP; direct JSON edits are the safest path |
| /home/louis/.claude.json | Claude Code user-scope config | Holds `context7` and `github`; `weread` has been removed |
| /home/louis/.local/bin/github-mcp-codex | Shared GitHub MCP wrapper | Uses `gh auth token`, Docker, and forwards `GITHUB_TOOLSETS` / `GITHUB_READ_ONLY` |
| /home/louis/.codex/AGENTS.md | Codex instruction policy | Updated to reflect GitHub MCP as a read-only discovery layer |
| /home/louis/.claude/CLAUDE.md | Claude instruction policy | Kept in sync with Codex and Gemini wording |
| /home/louis/.gemini/GEMINI.md | Gemini instruction policy | Kept in sync with Codex and Claude wording |
| /home/louis/internship-jd-catalog/.claude/handoffs/2026-03-22-022327-mcp-ecosystem-github-context7-sync.md | Current handoff | Resume point for the next agent |

### Key Patterns Discovered

- The user treats GitHub as a knowledge and content archive, not just a code host; issue content, comments, PRs, and search matter.
- Three-agent synchronization is a hard requirement. Any MCP kept in one client should usually be kept in all three with the same shape.
- Minimal toolsets are preferred over `all` because they reduce context noise, reduce mis-selection risk, and keep permissions narrower.
- Read-only GitHub MCP is a good default discovery layer. If write actions become frequent, split read and write into separate MCP entries instead of turning the main `github` entry into a full-access bundle.
- `gh` and `git` remain useful even when GitHub MCP exists; the right split is usually discovery via MCP, explicit execution via CLI or a narrower write MCP.
- Gemini configuration is safest through direct JSON edits rather than assuming CLI subcommands will handle every env-heavy case cleanly.
- The GitHub MCP wrapper depends on Docker health. If Docker is down, the wrapper fails even if configs are correct.

## Work Completed

### Tasks Finished

- [x] Compared MCP vs skills tradeoffs and corrected earlier overstatements about Playwright MCP being required
- [x] Evaluated Notion MCP against the user's actual workflow and recommended local Markdown plus private GitHub as the default
- [x] Researched `OpenCode`, `awesome-opencode`, and `oh-my-opencode`, focusing on orchestration, memory, safety, context pruning, and multi-agent patterns
- [x] Removed then reintroduced GitHub MCP based on the user's clarified needs, ending in a synchronized read-only setup across Codex, Gemini, and Claude
- [x] Removed `weread` from Claude Code
- [x] Updated `/home/louis/.local/bin/github-mcp-codex` to use `gh auth token` and forward GitHub MCP env controls
- [x] Updated `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` so documented policy matches runtime behavior
- [x] Rotated the `Context7` API key across all three clients and removed a stale commented key from Codex
- [x] Verified `context7` and `github` connectivity with `codex mcp list`, `gemini mcp list`, and `claude mcp list`

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| /home/louis/.local/bin/github-mcp-codex | Added env passthrough for GitHub MCP settings and standardized token sourcing via `gh auth token` | Keeps the three clients consistent and avoids hardcoding PATs |
| /home/louis/.codex/config.toml | Added and synced read-only `github` MCP config and updated `Context7` API key | Keeps Codex aligned with Claude and Gemini |
| /home/louis/.gemini/settings.json | Added and synced read-only `github` MCP config and updated `Context7` API key | Keeps Gemini aligned with Codex and Claude |
| /home/louis/.claude.json | Added and synced read-only `github` MCP config, removed `weread`, and kept `Context7` in place | Keeps Claude aligned with Codex and Gemini |
| /home/louis/.codex/AGENTS.md | Reworded GitHub usage guidance | Reflects read-only discovery via MCP plus execution via CLI and skills |
| /home/louis/.claude/CLAUDE.md | Reworded GitHub usage guidance | Keeps docs aligned across clients |
| /home/louis/.gemini/GEMINI.md | Reworded GitHub usage guidance | Keeps docs aligned across clients |
| /home/louis/internship-jd-catalog/.claude/handoffs/2026-03-22-022327-mcp-ecosystem-github-context7-sync.md | Created and completed handoff | Saves current state for the next agent |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Keep GitHub MCP as read-only across all three agents | Remove GitHub MCP entirely, full-access GitHub MCP, read-only GitHub MCP | Read-only preserves discovery and search value while keeping risk and tool noise lower |
| Do not recommend Notion MCP as a default | Notion MCP, local Markdown, private GitHub repo | The user's workflow is terminal and repo first, so local files plus Git history are a better fit |
| Do not treat Playwright MCP as required right now | Install Playwright MCP now, rely on agent-browser and skills | The user already has browser capability via `agent-browser`, so Playwright MCP is optional rather than required |
| Update instruction files to match runtime behavior | Leave docs stale, rewrite everything, make a minimal policy correction | Minimal synchronized edits preserve intent while keeping the docs truthful |
| Rotate `Context7` key everywhere and remove stale reference from Codex | Leave mixed keys in place, only update one client, keep commented old key | Three-agent sync matters and stale keys in comments are unnecessary secret residue |
| Recommend a future `github` plus `github_write` split if write actions become common | Keep only `gh`, turn the main GitHub MCP into full-access, create a split read/write setup | The split model preserves the current safe discovery layer while allowing a narrow write surface later |

## Pending Work

### Immediate Next Steps

1. Ask the user whether they want to keep the current single read-only GitHub MCP or add a second `github_write` MCP with minimal write tools.
2. If the user wants richer GitHub discovery without more write risk, consider changing `GITHUB_TOOLSETS` from `repos,issues,pull_requests` to `default,stargazers` while keeping `GITHUB_READ_ONLY=true`.
3. If the user reports any further Context7 trouble, verify whether the issue is with local client MCP usage or with the in-session developer-provided `mcp__context7__` tool, because those do not necessarily share auth and quota state.

### Blockers/Open Questions

- [ ] Open question: The user has not yet chosen between the current read-only GitHub MCP and a dual `github` / `github_write` design.
- [ ] Open question: The user may want broader GitHub discovery capabilities such as `stargazers` or `default` toolsets, but this has not been approved yet.
- [ ] Open question: Earlier in this Codex session, the developer-provided `Context7` tool returned a quota error; local CLI connectivity now looks healthy, but that discrepancy has not been fully explained.

### Deferred Items

- Creating a `github_write` MCP entry was deferred because the user has not approved the exact write-tool surface yet.
- Expanding GitHub toolsets to `default` or `default,stargazers` was deferred pending user confirmation.
- A more centralized secret-management approach for MCP keys was deferred after the immediate sync was completed.

## Context for Resuming Agent

### Important Context

This is not a repo-feature session. The actual work happened in user-scope config files under `/home/louis`, with the current repo only serving as the conversation cwd and handoff storage location. The user's high-level preference is to keep Codex, Gemini, and Claude Code synchronized. At the end of the session, all three clients are aligned on the same GitHub MCP policy: a single `github` MCP using `/home/louis/.local/bin/github-mcp-codex`, with `GITHUB_TOOLSETS="repos,issues,pull_requests"` and `GITHUB_READ_ONLY="true"`. This preserves GitHub discovery features like repo search, code search, issue reading, PR reading, and issue comment reading without exposing write actions by default. Claude no longer has `weread`. All three clients now contain the latest `Context7` API key, and `mcp list` checks showed both `context7` and `github` connected. The user's unresolved concern is legitimate: they sometimes do need write actions like modifying issues, commenting, merging, and updating PRs. The recommended next move is not to turn the main `github` MCP into a full-access `all` bundle, but to decide between keeping writes on `gh` or adding a second narrow `github_write` MCP. Also note that earlier in the conversation the developer-provided `mcp__context7__` tool returned a quota error; do not automatically assume that error reflects the local CLI Context7 setup, because local client MCP health and the in-session tool may be using different auth and quota paths.

### Assumptions Made

- The user still wants all three agents to expose equivalent MCP capabilities unless they explicitly request divergence.
- The user still prefers minimal but useful defaults over full-access kitchen-sink configurations.
- GitHub write actions are important but not dominant enough yet to justify immediately widening the main GitHub MCP.
- `gh auth` remains valid and Docker will remain available for the shared GitHub MCP wrapper.

### Potential Gotchas

- If Docker stops, `/home/louis/.local/bin/github-mcp-codex` fails even when all configs look correct.
- Gemini is best updated via direct JSON edits for MCP details; do not assume every change should go through interactive CLI commands.
- `claude mcp list` may show both `plugin:context7:context7` and the HTTP `context7` entry. Those are not the same thing.
- Old API keys can linger in comments or stale config blocks if not explicitly removed.
- This handoff lives in `internship-jd-catalog`, but the operational files are mostly outside the repo. Do not limit inspection to the repo tree.
- The automatically suggested earlier handoff in `.claude/handoffs/` is about JD shortlist work and is unrelated to this MCP and tooling thread.

## Environment State

### Tools/Services Used

- `Context7` HTTP MCP at `https://mcp.context7.com/mcp`
- Official GitHub MCP server via shared wrapper `/home/louis/.local/bin/github-mcp-codex`
- Docker for running the GitHub MCP container
- `gh auth token` as the GitHub token source for the wrapper
- `codex mcp list`, `gemini mcp list`, `claude mcp list` for verification
- GitHub official docs and the GitHub MCP official repo for toolset and read-only behavior

### Active Processes

- No known long-lived development processes were started for this task.
- All `mcp list` verification commands completed before handoff creation.

### Environment Variables

- `CONTEXT7_API_KEY`
- `GITHUB_PERSONAL_ACCESS_TOKEN`
- `GITHUB_TOOLSETS`
- `GITHUB_READ_ONLY`
- `GITHUB_TOOLS`
- `GITHUB_EXCLUDE_TOOLS`
- `GITHUB_LOCKDOWN_MODE`
- `GITHUB_INSIDERS`

## Related Resources

- /home/louis/.codex/config.toml
- /home/louis/.gemini/settings.json
- /home/louis/.claude.json
- /home/louis/.local/bin/github-mcp-codex
- /home/louis/.codex/AGENTS.md
- /home/louis/.claude/CLAUDE.md
- /home/louis/.gemini/GEMINI.md
- https://github.com/github/github-mcp-server
- https://github.com/github/github-mcp-server/blob/main/docs/server-configuration.md
- https://github.com/awesome-opencode/awesome-opencode
- https://github.com/code-yeongyu/oh-my-opencode

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
