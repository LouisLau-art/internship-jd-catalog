# Handoff: Troubleshooting Claude Code Router and Model Switching

## Session Metadata
- Created: 2026-03-30 01:10:00
- Project: /home/louis/internship-jd-catalog
- Branch: codex/resume-generator-sync
- Session duration: 45 minutes

### Recent Commits (for context)
  - cba90e3 fix(resume): track generator sources and sync tailored drafts
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup

## Handoff Chain

- **Continues from**: [2026-03-30-010547-claude-code-router-config-fix.md](./2026-03-30-010547-claude-code-router-config-fix.md)
  - Previous title: Claude Code Router Config Fix
- **Supersedes**: None

## Current State Summary

Currently troubleshooting integration between `Claude Code` CLI and `claude-code-router`. The goal is to use free models from `aihubmix` and `modelscope`. Current blockers include:
1. `Model not found` when using `/model provider,model` in Claude Code.
2. `400 INVALID_ARGUMENT` from Gemini due to invalid `thought_signature` format in conversation history.
3. `500 Internal Error` from `XiaomiMiMo` and `Qwen` models, likely due to JSON parsing issues or proxy interference.

## Codebase Understanding

### Architecture Overview

- `claude-code-router` acts as a proxy at `http://127.0.0.1:3456`.
- `Claude Code` is configured to use this router as its API base.
- Custom models are defined in `~/.claude-code-router/config.json`.

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `~/.claude-code-router/config.json` | Main configuration for providers, models, and routing rules. | Core configuration target. |
| `~/.claude-code-router/logs/` | Debug logs for the router. | Useful for diagnosing 500 errors. |

### Key Patterns Discovered

- **Claude Code Validation**: Recent versions of Claude Code (0.2.x+) perform local validation of model names before sending requests. This prevents switching to "unknown" models like `aihubmix,coding-glm-5-free` via the internal `/model` command.
- **Thought Signature Mismatch**: When switching from a reasoning model (e.g., DeepSeek-R1) to Gemini, the router converts `thought_signature` to a timestamp string, but Gemini API expects a Base64 encoded byte stream.

## Work Completed

### Tasks Finished

- [x] Analyzed `~/.claude-code-router/config.json` for provider and model definitions.
- [x] Identified `api_base_url` formatting issue for `aihubmix` (too specific).
- [x] Diagnosed the 400 error as a protocol/signature mismatch.
- [x] Confirmed `/model` syntax failure in Claude Code 0.2.x.

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `~/.claude-code-router/config.json` | (Proposed) Update `aihubmix` base URL and `Router.default`. | Fix routing and API endpoint issues. |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| Use `ccr model` CLI | Use `/model` in Claude Code | `ccr model` bypasses Claude Code's local validation. |
| Use `/clear` | Try to fix history manually | `/clear` is the fastest way to resolve `thought_signature` protocol errors. |

## Pending Work

### Immediate Next Steps

1. **Clear History**: Run `/clear` inside Claude Code to wipe the invalid `thought_signature` from context.
2. **Fix Config**: Update `~/.claude-code-router/config.json`:
   - Change `aihubmix` `api_base_url` to `https://aihubmix.com/v1`.
   - Set `"Router": { "default": "aihubmix,coding-glm-5-free" }`.
3. **External Switch**: Run `ccr model default aihubmix,coding-glm-5-free` in a standard terminal to force the router to use the target model.
4. **Proxy Check**: Set `"PROXY_URL": ""` in `config.json` if the local proxy is not running to avoid 500 errors.

### Blockers/Open Questions

- [ ] Does `aihubmix` require specific `Accept` or `Content-Type` headers that the router isn't providing?
- [ ] Why does `XiaomiMiMo` return invalid characters after JSON? (Possible response truncation).

## Context for Resuming Agent

### Important Context

- **NEVER** use `/model provider,model` if it keeps saying "Model not found". Use the `ccr` CLI tool instead.
- The 400 error `Base64 decoding failed for "1774789446865"` is a definitive sign that the conversation history is corrupted with timestamped signatures that Gemini cannot read.
- `aihubmix` model list in `config.json` contains `coding-glm-5-free` (no `.1`).

### Potential Gotchas

- If you see `SyntaxError: Unexpected non-whitespace character after JSON`, it usually means the upstream API returned an error page (HTML) or a malformed JSON body.

## Environment State

### Tools/Services Used

- `claude-code-router` (running on port 3456)
- `Claude Code` CLI
- `ccr` CLI for router management

### Active Processes

- `claude-code-router` daemon.

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
