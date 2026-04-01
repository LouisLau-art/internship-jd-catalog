# Handoff: 两段式大厂抓岗与选岗简历工作流落地

## Session Metadata
- Created: 2026-03-28 02:29:41
- Project: /home/louis/internship-jd-catalog
- Branch: main
- Session duration: 约 3 小时

### Recent Commits (for context)
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic
  - 7265dc8 feat(sync): add markdown dashboard synchronization logic

## Handoff Chain

- **Continues from**: [2026-03-27-232130-xiaomi-bytedance-application-status-sync.md](./2026-03-27-232130-xiaomi-bytedance-application-status-sync.md)
  - Previous title: 小米 / 字节真实投递状态同步与简历模板统一更新
- **Supersedes**: 2026-03-27-232130-xiaomi-bytedance-application-status-sync.md 作为后续 workflow 连续作业的主 handoff

> 本 handoff 已覆盖上一份 handoff 之后新增的两段式 workflow、Firecrawl 评估结论、测试与 smoke 结果。恢复时优先读这一份，再按需回看上一份。

## Current State Summary

本轮主要把“继续爬大厂技术类实习岗位 -> 每家公司挑 3 个左右最适合岗位 -> 生成对应简历 -> 更新 docs”这条链条，正式拆成了两个 skill：第一段 `campus-job-scrape` 只负责抓岗和 `docs/temp` 状态文件，第二段 `job-fit-to-resume` 负责 shortlist、简历映射/生成和主记事本同步。实现已经完成，测试和直接命令 smoke test 都通过；同时又 live 核了一遍 Firecrawl 官方 skill 集，结论是维持当前 `scrape + search + map` 三件套，不额外补装。当前没有 commit / push，本地工作树仍然很脏，其中包含这轮新改动，也包含之前就存在的大量 `.firecrawl/` 删除和数据刷新痕迹，下一位 agent 不要做任何清理式回滚。

## Codebase Understanding

### Architecture Overview

这条新 workflow 的结构现在是明确两段式：

1. `scripts/company_registry.py`
   维护公司元数据、抓取分组、数据文件路径和默认状态文档命名规则。
2. `scripts/company_fit_profiles.py`
   维护每家公司“优先投哪些岗位、对应哪个 PDF/生成脚本”的 profile。
3. `scripts/run_company_scrape.py`
   第一段总控。按 `scrape_group` 把公司拆给 `scrape_extra_bigtech.py` / `scrape_more_bigtech.py`，只更新 `data/*.json|csv` 和 `docs/temp/*crawl-status.md`。
4. `scripts/run_job_fit_resume.py`
   第二段总控。读刷新后的 `data/*`，按 fit profile 取 top N，映射到已有 PDF / generator script，必要时运行生成器，并可同步 `docs/job-search-progress.md`。
5. `.claude/skills/campus-job-scrape/SKILL.md` 与 `.claude/skills/job-fit-to-resume/SKILL.md`
   作为 repo 内可发现入口，对应这两个 orchestrator。
6. `job-sync`
   保持独立，不并入上面两段。

Firecrawl 只处于第一段底层 scraper 中的“可选抓取后端”位置，不进入第二段。最佳实践结论已经明确：API / JSON 优先，Firecrawl 只在没有稳定接口或重前端场景下兜底。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| [scripts/company_registry.py](/home/louis/internship-jd-catalog/scripts/company_registry.py) | 公司注册表、抓取分组、默认文档路径 | 两段式 workflow 的共享元数据源 |
| [scripts/company_fit_profiles.py](/home/louis/internship-jd-catalog/scripts/company_fit_profiles.py) | 公司级优先岗位和简历映射 | `job-fit-to-resume` 的决策核心 |
| [scripts/run_company_scrape.py](/home/louis/internship-jd-catalog/scripts/run_company_scrape.py) | 第一段抓岗总控 | 对外统一入口，支持 `live/cached` |
| [scripts/run_job_fit_resume.py](/home/louis/internship-jd-catalog/scripts/run_job_fit_resume.py) | 第二段 shortlist/简历总控 | 对外统一入口，支持 `--generate` 和 `--sync-progress` |
| [.claude/skills/campus-job-scrape/SKILL.md](/home/louis/internship-jd-catalog/.claude/skills/campus-job-scrape/SKILL.md) | 第一段 skill 文档 | 新入口，明确 scope boundary |
| [.claude/skills/job-fit-to-resume/SKILL.md](/home/louis/internship-jd-catalog/.claude/skills/job-fit-to-resume/SKILL.md) | 第二段 skill 文档 | 已从旧的 coverage audit skill 扩展为 orchestrator |
| [CLAUDE.md](/home/louis/internship-jd-catalog/CLAUDE.md) | 仓库级工作流说明 | 已同步成两段式流程和新命令 |
| [tests/test_run_company_scrape.py](/home/louis/internship-jd-catalog/tests/test_run_company_scrape.py) | 第一段 orchestration 测试 | 包括 `python scripts/... --help` 直跑入口测试 |
| [tests/test_run_job_fit_resume.py](/home/louis/internship-jd-catalog/tests/test_run_job_fit_resume.py) | 第二段 orchestration 测试 | 包括 top-role、resume-state 和直跑入口测试 |
| [tests/test_workflow_skill_docs.py](/home/louis/internship-jd-catalog/tests/test_workflow_skill_docs.py) | skill / CLAUDE 文档一致性测试 | 防止 skill 名和命令说明漂移 |
| [docs/plans/2026-03-28-campus-job-workflow-design.md](/home/louis/internship-jd-catalog/docs/plans/2026-03-28-campus-job-workflow-design.md) | 设计文档 | 记录为什么拆两段 |
| [docs/plans/2026-03-28-campus-job-workflow-implementation.md](/home/louis/internship-jd-catalog/docs/plans/2026-03-28-campus-job-workflow-implementation.md) | 实施计划 | 当前实现与这个 plan 基本一致 |

### Key Patterns Discovered

- 这个仓库适合“共享 core + 薄 orchestrator/skill wrapper”模式，不适合搞一个超级大而全的黑盒 skill。
- `data/*.json|csv` 仍然是 shortlist 的事实源，`docs/job-search-progress.md` 是展示层，不应该先于 data 做判断。
- 入口脚本如果要求用户按 `python scripts/foo.py` 直跑，就必须处理 `sys.path` 自举；这轮已经给两个 orchestrator 都补了这一层。
- Firecrawl 能力与 Firecrawl skill 安装是两回事：CLI 本身已经有全部命令，是否装 skill 只影响 agent 的“发现/默认调用”，不是能力可用性。
- 当前最佳实践边界已经明确：
  - stage 1: API/JSON 优先，Firecrawl 兜底
  - stage 2: 不绑定 Firecrawl

## Work Completed

### Tasks Finished

- [x] 用 `brainstorming` + `writing-plans` 明确了两段式 workflow 设计，并把计划文档落到了 `docs/plans/`
- [x] 按 TDD 先写红灯测试，再实现 `company_registry.py`、`company_fit_profiles.py`、`run_company_scrape.py`、`run_job_fit_resume.py`
- [x] 给 `xiaomi` 和 `bilibili` 补齐了 fit profile，避免 registry key 存在但 orchestrator 直接 `KeyError`
- [x] 新增 `campus-job-scrape` skill，并把 `job-fit-to-resume` 扩展为第二段 orchestrator skill
- [x] 更新 `CLAUDE.md`，把推荐工作流改为 `campus-job-scrape -> job-fit-to-resume -> job-sync`
- [x] 修复了两个 orchestrator 在 `python scripts/...` 直跑时的 import path 问题
- [x] 重新核验 Firecrawl 本地状态、官方仓库 skill 树和 `skills.sh/firecrawl/cli` 页面，结论是不新增 skill，维持 `scrape + search + map`

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| [scripts/company_registry.py](/home/louis/internship-jd-catalog/scripts/company_registry.py) | 新增公司注册表、抓取分组、默认状态文档命名 | 让第一段总控不再硬编码公司细节 |
| [scripts/company_fit_profiles.py](/home/louis/internship-jd-catalog/scripts/company_fit_profiles.py) | 新增 fit profile，后续补入 `xiaomi` 和 `bilibili` | 让第二段总控有统一 shortlist 和 resume 映射依据 |
| [scripts/run_company_scrape.py](/home/louis/internship-jd-catalog/scripts/run_company_scrape.py) | 新增第一段 orchestrator，并补 `sys.path` 自举 | 对外统一抓岗入口，支持直接命令运行 |
| [scripts/run_job_fit_resume.py](/home/louis/internship-jd-catalog/scripts/run_job_fit_resume.py) | 新增第二段 orchestrator，并补 `sys.path` 自举 | 对外统一 shortlist / resume / sync 入口 |
| [.claude/skills/campus-job-scrape/SKILL.md](/home/louis/internship-jd-catalog/.claude/skills/campus-job-scrape/SKILL.md) | 新增 skill 文档 | 把第一段 skill 化，明确只改 `data/` 和 `docs/temp/` |
| [.claude/skills/job-fit-to-resume/SKILL.md](/home/louis/internship-jd-catalog/.claude/skills/job-fit-to-resume/SKILL.md) | 从旧 audit skill 扩成 orchestrator skill | 把第二段的职责写清楚 |
| [CLAUDE.md](/home/louis/internship-jd-catalog/CLAUDE.md) | 更新 common commands、workflow、关键文件说明 | 保持仓库级上下文与实现一致 |
| [tests/test_company_registry.py](/home/louis/internship-jd-catalog/tests/test_company_registry.py) | 新增 registry 测试 | 锁定公司键、分组和状态文档路径规则 |
| [tests/test_company_fit_profiles.py](/home/louis/internship-jd-catalog/tests/test_company_fit_profiles.py) | 新增/扩展 fit profile 测试 | 锁定 `didi/oppo/kuaishou/xiaomi/bilibili` 的预期行为 |
| [tests/test_run_company_scrape.py](/home/louis/internship-jd-catalog/tests/test_run_company_scrape.py) | 新增 orchestrator 和直跑入口测试 | 防止 CLI 入口再次坏掉 |
| [tests/test_run_job_fit_resume.py](/home/louis/internship-jd-catalog/tests/test_run_job_fit_resume.py) | 新增 orchestrator 和直跑入口测试 | 防止 shortlist 逻辑和直跑入口漂移 |
| [tests/test_workflow_skill_docs.py](/home/louis/internship-jd-catalog/tests/test_workflow_skill_docs.py) | 新增文档一致性测试 | 保证 skill 文档和 `CLAUDE.md` 的命令说明同步 |
| [docs/temp/2026-03-28-job-fit-shortlist.md](/home/louis/internship-jd-catalog/docs/temp/2026-03-28-job-fit-shortlist.md) | smoke test 生成的 shortlist | 验证第二段命令真实可跑 |
| [docs/temp/2026-03-28-extra-bigtech-crawl-status.md](/home/louis/internship-jd-catalog/docs/temp/2026-03-28-extra-bigtech-crawl-status.md) | smoke test 生成的 crawl status | 验证第一段命令真实可跑 |
| [docs/temp/2026-03-28-more-bigtech-crawl-status.md](/home/louis/internship-jd-catalog/docs/temp/2026-03-28-more-bigtech-crawl-status.md) | smoke test 生成的 crawl status | 同上 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 把 workflow 拆成 `campus-job-scrape` + `job-fit-to-resume` | 一个大总控 skill；两段式 skill；继续靠会话记忆 | 两段式边界最清楚，也最符合“shared core + thin adapter” |
| `campus-job-scrape` 只更新 `data/` 和 `docs/temp/` | 顺手改主记事本；只写临时状态页 | 把抓岗和业务决策分开，避免 stage 1 越权 |
| `job-fit-to-resume` 负责 shortlist + resume + progress sync | 保持旧版只做 coverage audit；另起第三个 skill | 第二段本来就该承担决策和回写 |
| 不把 `job-sync` 并进前两段 | 三段合一；独立保留 | 投后同步和抓岗/选岗不是同一个生命周期 |
| Firecrawl 保持 `scrape + search + map`，不新增 | 继续补 `crawl/browser/agent/download/umbrella` | 当前 repo 是 API-first、Firecrawl-fallback，新增 skill 价值低于触发噪音和重叠成本 |
| 不把 Firecrawl 强绑到第二段 | 两段都绑定 Firecrawl；只第一段软绑定 | 第二段只吃已落地数据，没有必要耦合抓取后端 |

## Pending Work

### Immediate Next Steps

1. 决定是否把这轮 workflow 改动单独 commit；如果 commit，建议只收 scripts / tests / skill docs / CLAUDE / design docs，不把带个人信息的简历产物带进去。
2. 如果继续扩大厂抓取，就按新流程跑：
   先 `python scripts/run_company_scrape.py --companies ... --refresh-mode cached|live`
   再 `python scripts/run_job_fit_resume.py --companies ... --top-n-per-company 3`
3. 若未来出现“整站 docs / 分区批量离线抓取”高频需求，再重新评估是否补装 `firecrawl-crawl`；当前不要动 Firecrawl skill 集。

### Blockers/Open Questions

- [ ] Open question: 这轮 workflow 与测试改动是否现在就要 commit / push，还是继续和后续抓岗工作一起攒一轮。
- [ ] Open question: 是否要把 `campus-job-scrape` 的 Firecrawl fallback 策略再写进更多 repo 文档或脚本注释，目前已经口头与 skill 层明确，但还没有更细粒度的 per-company policy 注释。

### Deferred Items

- `firecrawl-crawl` 暂不安装。只有当“整站 / 某个 docs section 批量抓取”变成常见需求时再评估。
- `firecrawl-agent` / `firecrawl-download` / `firecrawl-browser` / umbrella `firecrawl` 暂不引入，避免重叠、黑盒化或 deprecated 路线。
- 这轮没有触碰 commit/push，也没有清理工作树里已有的大量 `.firecrawl/` 删除记录和旧临时文档删除记录。

## Context for Resuming Agent

### Important Context

这是当前最关键的恢复上下文：

- 这轮真正完成的是“把现有大厂抓取与简历链路做成可复用的两段式 workflow”，不是新增一堆岗位内容本身。
- 所有核心实现都已经写完并验证：
  - `python -m pytest tests/test_company_registry.py tests/test_company_fit_profiles.py tests/test_run_company_scrape.py tests/test_run_job_fit_resume.py tests/test_workflow_skill_docs.py tests/test_generate_unapplied_bigtech_resumes.py tests/test_scrape_extra_bigtech.py tests/test_scrape_more_bigtech.py -q`
  - 结果：`36 passed`
- 真实命令 smoke test 也过了：
  - `python scripts/run_company_scrape.py --companies netease,oppo --refresh-mode cached`
  - `python scripts/run_job_fit_resume.py --companies netease,pinduoduo,didi,kuaishou,honor,oppo,xiaomi,bilibili --top-n-per-company 3 --no-generate --no-sync-progress`
- 这两个 orchestrator 最开始都存在 `python scripts/...` 直跑时 `ModuleNotFoundError: No module named 'scripts'` 的问题，已经通过在文件头部加入 repo-root `sys.path` 自举修好了。下一位 agent 不要把这段删掉，除非同时引入更稳的包入口方案并重新补测试。
- Firecrawl 这轮也已经 live 核验过：
  - 本地安装：`firecrawl-scrape`、`firecrawl-search`、`firecrawl-map`
  - CLI：`v1.11.2`，已认证，可用
  - `skills.sh/firecrawl/cli` 显示 10 条，但 `firecrawl/cli` 官方仓库 `skills/` 当前只有 8 个真实目录，`firecrawl-experimental` 在 GitHub 是 404
  - 当前结论：不新增 Firecrawl skill
- 仓库本地没有 repo-level 的 `create_handoff.py` / `validate_handoff.py`；这次 handoff 是通过全局 skill 路径 `/home/louis/.codex/skills/session-handoff/scripts/` 下的脚本创建和校验的。

### Assumptions Made

- `data/*.json|csv` 继续被视为 shortlist 的事实源。
- 用户当前仍然偏好“最小但高价值”的 Firecrawl skill 集，不接受为了“全功能看起来完整”而装一堆重叠 skill。
- 用户仍然要求简历 PDF 与其他个人隐私产物不进入 commit / push。
- 这轮 smoke test 写回的 `data/` 和 `docs/temp/` 变更可以接受，不需要回滚。

### Potential Gotchas

- 工作树非常脏，而且不都是本轮造成的。`git status --short` 里大量 `.firecrawl/*`、旧 `docs/temp/*` 删除项和若干 `data/*` / `docs/job-search-progress.md` 的改动，很多是在当前会话开始前就存在。不要做 `git reset --hard` 或批量还原。
- `campus-job-scrape --refresh-mode cached` 依然会真实重写 `data/` 和 `docs/temp/` 文件，因为它会重跑 family scraper，只是底层 Firecrawl 部分复用 `.firecrawl/` 缓存。
- `bilibili` 现在在第二段 workflow 里只是“不会异常”的 placeholder profile；当前 live 数据仍然是 `0` 岗，不会出现在 shortlist 输出里。
- `skills.sh` 页面条目数和 GitHub 官方 `skills/` 目录数不一致，不要直接拿 catalog 卡片数当安装清单。
- 旧 handoff 里有一些“脚本已存在于 repo”式表述，针对 session-handoff 这件事已经不准确；当前 repo-local 并没有 create/list/check/validate handoff 脚本。

## Environment State

### Tools/Services Used

- Python 3.x：用于运行所有 repo scripts 和 tests
- `gh`：用于核验 `firecrawl/cli` 仓库信息与目录
- GitHub MCP：用于读取 `firecrawl/cli` 官方 `skills/` 目录和 `SKILL.md`
- Firecrawl CLI：`v1.11.2`，已认证；本地 skill 仅保留 `scrape/search/map`
- session-handoff 全局 skill 脚本：
  - `/home/louis/.codex/skills/session-handoff/scripts/create_handoff.py`
  - `/home/louis/.codex/skills/session-handoff/scripts/validate_handoff.py`

### Active Processes

- 无需要继续保持的后台进程。

### Environment Variables

- `FIRECRAWL_API_KEY`
- `QQ_EMAIL`
- `QQ_AUTH_CODE`
- `RESUME_PHOTO`

## Related Resources

- [两段式 workflow 设计文档](/home/louis/internship-jd-catalog/docs/plans/2026-03-28-campus-job-workflow-design.md)
- [两段式 workflow 实施计划](/home/louis/internship-jd-catalog/docs/plans/2026-03-28-campus-job-workflow-implementation.md)
- [第二段 smoke test 输出 shortlist](/home/louis/internship-jd-catalog/docs/temp/2026-03-28-job-fit-shortlist.md)
- [第一段 smoke test 输出 extra-bigtech 状态](/home/louis/internship-jd-catalog/docs/temp/2026-03-28-extra-bigtech-crawl-status.md)
- [第一段 smoke test 输出 more-bigtech 状态](/home/louis/internship-jd-catalog/docs/temp/2026-03-28-more-bigtech-crawl-status.md)
- [上一份 handoff](/home/louis/internship-jd-catalog/.claude/handoffs/2026-03-27-232130-xiaomi-bytedance-application-status-sync.md)
- [Firecrawl 官方仓库](https://github.com/firecrawl/cli)
- [Firecrawl 官方 skills 页面](https://skills.sh/firecrawl/cli)

---

**Security Reminder**: 本 handoff 未包含任何密钥、cookie 或个人隐私值；引用的环境变量只有名字，没有值。
