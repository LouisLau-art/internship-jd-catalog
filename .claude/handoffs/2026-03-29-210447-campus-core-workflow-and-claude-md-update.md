# Handoff: campus_core workflow 接入与 CLAUDE.md 定向维护

## Session Metadata
- Created: 2026-03-29 21:04:47
- Project: /home/louis/internship-jd-catalog
- Branch: codex/resume-generator-sync
- Session duration: 约 2 小时

### Recent Commits (for context)
  - cba90e3 fix(resume): track generator sources and sync tailored drafts
  - bab343f feat(scrape): add extra bigtech internship positions and scraping scripts
  - 57460d7 feat(workflow): add resume coverage audit and qq sync setup
  - 553d4db feat(workflow): wrap job sync into a reusable custom skill
  - 35f09a9 feat(sync): add markdown dashboard synchronization logic

## Handoff Chain

- **Continues from**: [2026-03-28-022941-two-stage-campus-job-workflow.md](./2026-03-28-022941-two-stage-campus-job-workflow.md)
  - Previous title: 两段式大厂抓岗与选岗简历工作流落地
- **Supersedes**: `2026-03-28-022941-two-stage-campus-job-workflow.md` 作为当前最新的 workflow 延续 handoff

> 先读这一份；只有在需要回看两段式 workflow 的最初设计理由时，再回看上一份 handoff。

## Current State Summary

本轮主要完成了三件事。第一，按用户要求回看了昨天的 handoff 和当前进度文档，给出下一轮投递建议，并明确区分了日常实习与暑期转正实习。第二，确认当前 raw data 已覆盖阿里、蚂蚁、字节、美团、京东、腾讯、小红书、华为，但它们还没接进现有两段式 workflow，于是把这 8 家正式接入 `campus-job-scrape -> job-fit-to-resume`。第三，按 `claude-md-improver` 流程审计并定向更新了 `CLAUDE.md`，补了当前三分组 workflow、stage-2 dry run 命令和 `campus_core` 共享 combined export 的 gotcha。所有本轮聚焦测试都已通过，并额外做了一次 stage-2 dry run；没有执行 stage-1 live scrape，因为那会直接打外部官网。

## Codebase Understanding

### Architecture Overview

这个仓库现在已经有两层需要区分清楚：

1. 原始数据层
   - `scripts/scrape_campus_jobs.py` 负责 Alibaba / Ant Group / Huawei 的抓取，并把 ByteDance / Meituan / JD / Tencent / Xiaohongshu 的维护导出重建进 `data/campus_positions_combined.*`
   - `scripts/scrape_extra_bigtech.py` 和 `scripts/scrape_more_bigtech.py` 分别负责另外两组公司
2. 两段式 workflow 层
   - `scripts/company_registry.py` 定义公司元数据、分组、数据文件位置，以及最关键的 `source_filters`
   - `scripts/run_company_scrape.py` 负责 stage 1 调度；新加了 `campus_core`
   - `scripts/company_fit_profiles.py` 负责每家公司 shortlist 目标岗位和简历映射
   - `scripts/run_job_fit_resume.py` 负责 stage 2；对 `campus_core` 公司从 `data/campus_positions_combined.json` 里按 `source` 过滤岗位

本轮最重要的架构决定是：不为那 8 家新造一套 per-company 聚合 JSON，而是复用现有 `data/campus_positions_combined.*`，通过 registry 的 `source_filters` 做读取隔离。这让现有 scraper 和 downstream shortlist 逻辑能共用同一份事实源。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `scripts/company_registry.py` | 公司注册表、抓取分组、共享导出过滤规则 | 本轮新增 `campus_core` 和 `source_filters` 的核心位置 |
| `scripts/run_company_scrape.py` | stage-1 总控 | 现在会把 8 家新公司路由到 `scripts/scrape_campus_jobs.py` |
| `scripts/run_job_fit_resume.py` | stage-2 总控 | 现在支持从 shared combined export 里按 `source` 过滤，并修复了 markdown 表格转义 |
| `scripts/company_fit_profiles.py` | 每家公司目标岗位和简历生成脚本映射 | 本轮补了 Alibaba / Ant Group / ByteDance / Meituan / JD / Tencent / Xiaohongshu / Huawei |
| `.claude/skills/campus-job-scrape/SKILL.md` | stage-1 skill 文档 | 已更新三分组说明和新的命令示例 |
| `.claude/skills/job-fit-to-resume/SKILL.md` | stage-2 skill 文档 | 已更新为 `campus_core` 公司的 shortlist 入口示例 |
| `CLAUDE.md` | 仓库级上下文文档 | 本轮按 `claude-md-improver` 做了 3 处定向更新 |
| `tests/test_company_registry.py` | registry 行为测试 | 锁定 `campus_core` 和 shared-export 配置 |
| `tests/test_run_company_scrape.py` | stage-1 orchestrator 测试 | 锁定 `campus_core` 不追加 Firecrawl cached flag |
| `tests/test_run_job_fit_resume.py` | stage-2 orchestrator 测试 | 锁定 shared-export 过滤、XHS 目标岗位和 markdown 表格转义 |
| `tests/test_workflow_skill_docs.py` | skill / CLAUDE 文档一致性测试 | 用于验证 CLAUDE.md 更新没有破坏现有文档契约 |
| `docs/temp/2026-03-29-campus-core-dryrun-shortlist.md` | 本轮 dry run 产物 | 可直接查看阿里 / 字节 / 小红书的 shortlist 输出 |

### Key Patterns Discovered

- 这个仓库现在有三种 scraper family：`campus_core`、`extra_bigtech`、`more_bigtech`，不要再沿用旧的“只看 extra-bigtech”心智模型。
- 对 `campus_core` 公司，stage 2 的事实源不是独立 JSON，而是 `data/campus_positions_combined.*` + `source` 过滤。
- `run_job_fit_resume.py` 适合先 dry run：`--no-generate --no-sync-progress --output-doc ...`。这一步很适合作为继续批量接公司的默认验证动作。
- location / reason 字段里可能包含 `|`，如果要继续改 shortlist 渲染逻辑，必须保留 markdown table cell escaping。
- 当前 repo-local 没有 handoff scaffold / validate 脚本；创建与校验 handoff 要用全局 skill 目录里的脚本。

## Work Completed

### Tasks Finished

- [x] 回看昨天 handoff 与当前进度文档，给出下一轮岗位投递建议，并明确区分日常实习与暑期转正实习
- [x] 核对 raw data 覆盖与 workflow 覆盖差异，确认 8 家公司已爬取但未接入两段式 workflow
- [x] 把 Alibaba / Ant Group / ByteDance / Meituan / JD / Tencent / Xiaohongshu / Huawei 接入 `campus_core`
- [x] 为上述 8 家补齐 fit profiles、generator 映射和相关测试
- [x] 修复 shortlist markdown 表格中 `|` 导致列错位的问题
- [x] 运行 stage-2 dry run，验证阿里 / 字节 / 小红书可以正常产出 shortlist
- [x] 按 `claude-md-improver` 审计 `CLAUDE.md`，输出质量报告并在用户确认后应用 3 处定向更新
- [x] 生成并校验本 handoff

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `scripts/company_registry.py` | 新增 `campus_core` 公司配置与 `source_filters`，并抽出 shared-export 过滤/计数辅助函数 | 让 8 家公司能复用 `data/campus_positions_combined.*` |
| `scripts/run_company_scrape.py` | 新增 `campus_core` family 路由，并确保 cached 模式不对该 family 追加 Firecrawl 参数 | 复用现有 `scripts/scrape_campus_jobs.py`，避免新造 scraper |
| `scripts/run_job_fit_resume.py` | 支持从 shared export 按 `source` 过滤；新增 markdown table escaping | 让 shortlist 对 `campus_core` 有效且输出稳定 |
| `scripts/company_fit_profiles.py` | 补齐 8 家公司的 shortlist 目标岗位与 generator 映射 | 让 stage 2 能真正给出岗位推荐和 PDF 映射 |
| `tests/test_company_registry.py` | 新增 `campus_core` / `source_filters` 覆盖 | 锁定 registry 设计 |
| `tests/test_run_company_scrape.py` | 新增 `campus_core` 调度测试 | 防止后续误给 `scrape_campus_jobs.py` 塞错参数 |
| `tests/test_run_job_fit_resume.py` | 新增 shared-export 过滤、XHS 标题匹配、markdown 转义测试 | 锁定本轮修复行为 |
| `tests/test_company_fit_profiles.py` | 新增 Alibaba / Ant Group / Xiaohongshu profile 测试 | 锁定新增 profile 的岗位标题与别名 |
| `tests/test_workflow_skill_docs.py` | 让文档测试覆盖新的 workflow 文案 | 保证 skill 文档和 `CLAUDE.md` 同步 |
| `.claude/skills/campus-job-scrape/SKILL.md` | 更新三分组 family 和长命令示例 | 让 skill 文档反映当前实现 |
| `.claude/skills/job-fit-to-resume/SKILL.md` | 更新 `campus_core` 公司示例 | 让 stage-2 入口说明不再只覆盖旧 6 家 |
| `CLAUDE.md` | 更新 snapshot、stage-2 dry run 命令、workflow wording、shared-export gotcha | 让仓库级上下文与当前实现一致 |
| `docs/temp/2026-03-29-campus-core-dryrun-shortlist.md` | 新增 dry run shortlist 产物 | 验证新接入公司的 stage-2 行为 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 对 8 家新公司复用 `data/campus_positions_combined.*` + `source_filters` | 为每家公司再生成独立聚合 JSON；直接读 combined 不做过滤 | 复用现有数据模型最稳，改动小且不重复造轮子 |
| 新增 `campus_core` family 并路由到 `scripts/scrape_campus_jobs.py` | 新写第三套 scraper；把 8 家塞进旧 family | `scripts/scrape_campus_jobs.py` 已经是这 8 家的事实入口，复用成本最低 |
| stage-1 不对 `campus_core` 追加 `--use-cached-firecrawl` | 所有 family 一刀切追加 cached flag；为 `campus_core` 另写伪缓存参数 | 现有 `scripts/scrape_campus_jobs.py` 没有这个参数，强加只会制造误导 |
| shortlist dry run 默认不生成 PDF、不回写主文档 | 直接跑全量 `--generate --sync-progress`；只做单测 | dry run 是最安全的功能验证路径，尤其适合继续扩公司时复用 |
| `CLAUDE.md` 只做 3 处定向更新 | 全面重写；暂时不改 | 用户调用的是 `claude-md-improver`，但当前文档总体可用，适合只修最关键过时点 |
| 不执行 stage-1 live scrape | 直接运行 `run_company_scrape.py` 全链路刷新；只依赖单测 | 真实 stage-1 会命中外部官网，本轮任务目标是接 workflow，不是刷新线上数据 |

## Pending Work

### Immediate Next Steps

1. 如果用户下一步要继续投递，优先直接使用现有 shortlist / fit profile 跑 `job-fit-to-resume` dry run 或正式 run，覆盖 `campus_core` 里的目标公司。
2. 如果用户要把这轮 workflow 改动落库，先决定是否 commit；注意大部分核心脚本和测试目前在 `git status` 里仍是 `??` 未跟踪状态。
3. 如果用户要真正刷新线上岗位，再手动跑 stage 1；对 `campus_core` 要明确这会触发 `scripts/scrape_campus_jobs.py` 的真实外部抓取，不是纯本地缓存回放。

### Blockers/Open Questions

- [ ] Open question: 这轮新增的 workflow 脚本、测试和 skill 文档要不要现在就单独 commit，还是继续和后续抓岗工作一起收口。
- [ ] Open question: 是否要把 OceanBase 单独提成 company key；当前它仍然只作为 Ant Group 额外岗位存在，没有单独接进 registry。
- [ ] Open question: 是否需要继续把 `claude-md-improver` 的思路同步到其他全局 agent 文档；本轮只更新了 repo-level `CLAUDE.md`。

### Deferred Items

- 暂未执行 `run_company_scrape.py` 的真实抓取 run；这一步留到用户明确要刷新线上数据时再做。
- 暂未生成新的 PDF；本轮 stage 2 只做了 `--no-generate --no-sync-progress` 的 dry run。
- 暂未处理工作树里大量与本轮无关的 `.firecrawl/*` 删除、旧 `docs/temp/*` 删除和既有数据改动。
- 暂未为 `campus_core` 再补更细粒度的 source-level 文档说明，当前只在 `CLAUDE.md` 和代码里说明了 shared-export 机制。

## Context for Resuming Agent

### Important Context

这份 handoff 最关键的上下文有 6 点：

1. 用户先问了“接下来应该投哪些岗位”，要求明确区分日常实习和暑期转正实习；这个部分已经基于昨天 handoff 和当前 progress 文档回答完毕，不需要重做。
2. 随后用户追问“是不是还有公司没爬取”，实际结论不是“没爬”，而是“有 8 家已存在 raw data，但没接进当前两段式 workflow”。
3. 本轮已经把这 8 家接入：`alibaba`、`antgroup`、`bytedance`、`meituan`、`jd`、`tencent`、`xiaohongshu`、`huawei`。核心实现文件很多仍是未跟踪文件，不是普通 diff。
4. 新设计的关键不是多写了几个 company entry，而是 registry 现在支持 shared export filtering；stage 2 不再假设“一公司一 JSON”。
5. dry run 时暴露出 `work_locations` 里有 `|` 会打坏 markdown 表格，这个 bug 已经修复并加了回归测试；后续如果碰到 table 渲染异常，不要重复排查旧版本代码。
6. `claude-md-improver` 审计后只对 `CLAUDE.md` 做了 3 处小改，没有做大规模重写；当前 repo 级文档已经足够继续工作。

补充的具体验证证据：

- 聚焦测试：
  - `python -m unittest tests.test_company_registry tests.test_company_fit_profiles tests.test_run_company_scrape tests.test_run_job_fit_resume tests.test_workflow_skill_docs -v`
  - 结果：`29` 项通过
- `CLAUDE.md` 文档校验：
  - `python -m unittest tests.test_workflow_skill_docs -v`
  - 结果：`3` 项通过
- stage-2 dry run：
  - `python scripts/run_job_fit_resume.py --companies alibaba,bytedance,xiaohongshu --top-n-per-company 3 --no-generate --no-sync-progress --output-doc docs/temp/2026-03-29-campus-core-dryrun-shortlist.md`
  - 结果：输出 `docs/temp/2026-03-29-campus-core-dryrun-shortlist.md`，阿里 / 字节 / 小红书 shortlist 正常

### Assumptions Made

- 当前 `data/campus_positions_combined.*` 足够作为这 8 家公司的 stage-2 事实源，不需要先重跑 live scrape 才能完成 workflow 接入。
- 用户当前更关心“现在能不能继续投”和“workflow 能不能继续复用”，不是马上要做一次全量线上刷新。
- `CLAUDE.md` 应该保持定向、克制更新，不需要为了追求“完整”把所有实现细节都塞进去。
- 继续生成 PDF 时仍会遵守“不碰用户隐私产物、不默认提交个人简历文件”的工作边界。

### Potential Gotchas

- 当前分支是 `codex/resume-generator-sync`，不是 `main`。如果下一位 agent 直接开始 commit / push，要先确认用户是否接受在这个分支继续。
- `git status` 很脏，而且大量脏文件不是本轮造成的。不要做任何清理式回滚，也不要把“未跟踪脚本很多”误判成脚本不存在。
- `campus_core` 的 `--refresh-mode cached` 只是保留统一 CLI 接口，不会给 `scripts/scrape_campus_jobs.py` 追加 Firecrawl cached flag；真正执行 stage 1 依然会触发官网抓取。
- repo 里没有 handoff scaffold / validate 脚本。如果后面继续做 handoff，要用 `/home/louis/.codex/skills/session-handoff/scripts/` 下的全局脚本。
- `git diff` 看不到未跟踪文件，所以本轮核心改动如果只看 `git diff --stat` 会严重低估范围。要同时看 `git status --short`。

## Environment State

### Tools/Services Used

- Python 3.x：运行 unittest、dry run、全局 handoff 脚本
- 全局 `session-handoff` 脚本：
  - `/home/louis/.codex/skills/session-handoff/scripts/create_handoff.py`
  - `/home/louis/.codex/skills/session-handoff/scripts/validate_handoff.py`
- repo 内 workflow 入口：
  - `scripts/run_company_scrape.py`
  - `scripts/run_job_fit_resume.py`

### Active Processes

- 无需要保留的后台进程。

### Environment Variables

- `RESUME_PHOTO`：后续如果重新打开 PDF 生成流程会用到

## Related Resources

- `scripts/company_registry.py`
- `scripts/company_fit_profiles.py`
- `scripts/run_company_scrape.py`
- `scripts/run_job_fit_resume.py`
- `.claude/skills/campus-job-scrape/SKILL.md`
- `.claude/skills/job-fit-to-resume/SKILL.md`
- `CLAUDE.md`
- `tests/test_company_registry.py`
- `tests/test_company_fit_profiles.py`
- `tests/test_run_company_scrape.py`
- `tests/test_run_job_fit_resume.py`
- `tests/test_workflow_skill_docs.py`
- `docs/plans/2026-03-28-campus-job-workflow-design.md`
- `docs/plans/2026-03-28-campus-job-workflow-implementation.md`
- `docs/temp/2026-03-29-campus-core-dryrun-shortlist.md`
- `.claude/handoffs/2026-03-28-022941-two-stage-campus-job-workflow.md`

---

**Security Reminder**: 本 handoff 未包含任何密钥、cookie 或环境变量值；只出现了变量名和公开仓库/本地文件路径。
