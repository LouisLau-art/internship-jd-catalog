# Internship JD Catalog

Collected internship job descriptions and quick-fit notes for Louis Lau.

## Snapshot

- Current snapshot date: `2026-03-21`
- Total pasted entries persisted: `34`
- Unique JD count after de-duplicating one repeated Xiaomi backend posting: `33`
- Companies covered:
  - `Alibaba`
  - `Ant Group`
  - `OceanBase`
  - `Huawei`
  - `Xiaomi`
  - `Xiaohongshu`
- Raw export pools captured:
  - `Alibaba`: `455`
  - `Alibaba` daily internship technical filter: `72`
  - `Ant Group`: `96`
  - `Huawei` internship intent rows: `80`
  - `Huawei` Wuhan R&D intent rows: `73`

## What is in this repo

- [catalog.csv](./catalog.csv)
  Flat index for quick filtering by company, track, fit, and notes.
- [docs/companies/xiaomi.md](./docs/companies/xiaomi.md)
  Structured notes for Xiaomi postings, including the earlier 3 algorithm roles and the later software-R&D batch.
- [docs/companies/xiaohongshu.md](./docs/companies/xiaohongshu.md)
  Structured notes for the 2 Xiaohongshu targeted internship roles.
- [docs/companies/alibaba.md](./docs/companies/alibaba.md)
  Summary note for the Alibaba 2027 internship raw campus export snapshot.
- [docs/companies/alibaba-daily.md](./docs/companies/alibaba-daily.md)
  Summary note for the Alibaba daily internship technical-role export snapshot.
- [docs/companies/antgroup.md](./docs/companies/antgroup.md)
  Summary note for the Ant Group raw campus export snapshot.
- [docs/xiaomi-top-5.md](./docs/xiaomi-top-5.md)
  Ordered shortlist of the 5 Xiaomi roles currently worth prioritizing.
- [docs/alibaba-top-5.md](./docs/alibaba-top-5.md)
  First reviewed shortlist for Alibaba roles from the raw export pool.
- [docs/antgroup-top-5.md](./docs/antgroup-top-5.md)
  First reviewed shortlist for Ant Group roles from the raw export pool.
- [docs/daily-intern-top-5.md](./docs/daily-intern-top-5.md)
  Cross-company shortlist for the 5 highlighted `日常实习` roles.

## Raw Site Exports

- [scripts/scrape_campus_jobs.py](./scripts/scrape_campus_jobs.py)
  Bulk-export utility for the Alibaba, Ant Group, and Huawei campus job pages.
- [data/alibaba_positions_100000540002.csv](./data/alibaba_positions_100000540002.csv)
  Raw Alibaba 2027 internship export from `2026-03-21`.
- [data/alibaba_positions_100000560002_tech.csv](./data/alibaba_positions_100000560002_tech.csv)
  Raw Alibaba daily internship technical-role export from `2026-03-21`.
- [data/antgroup_positions_26022600074513.csv](./data/antgroup_positions_26022600074513.csv)
  Raw Ant Group 2027 return-offer internship export from `2026-03-21`.
- [data/huawei_positions_intern.csv](./data/huawei_positions_intern.csv)
  Huawei campus internship export expanded to intent-level JDs from `2026-03-21`.
- [data/huawei_positions_wuhan_rd.csv](./data/huawei_positions_wuhan_rd.csv)
  Filtered Huawei intent-level export for rows whose locations include `武汉` and whose family code is `JFC1` (`研发类`) from `2026-03-21`.
- [data/campus_positions_combined.csv](./data/campus_positions_combined.csv)
  Combined flat export across all captured site snapshots.
- [data/README.md](./data/README.md)
  Explains the raw-export layer and its schema.

## Fit legend

- `strong`: worth prioritizing
- `medium`: can apply if needed
- `stretch`: possible, but not a natural fit
- `low`: weak match
- `avoid`: likely waste of application bandwidth

## Current recommendation

### Priority apply

- OceanBase `AI平台研发实习生`
- 蚂蚁数字科技 `研发工程师（金融AI）`
- Xiaohongshu `生态研发工程师实习生`
- Xiaohongshu `Java 后端开发实习生（AI Agent 方向）`
- Xiaomi `服务端研发实习生—武汉`
- Xiaomi `后端研发工程师实习生`（国际小米网 AI 翻译/校对）
- Xiaomi `软件研发工程师实习生`（云平台基础服务）

### Secondary apply

- 蚂蚁数字科技 `AI PaaS平台开发（训推/知识工程）`
- Xiaomi `数据理解研发工程师实习生`
- Xiaomi `效能工具研发工程师实习生`
- Xiaomi `电商中台软件开发实习生`
- Xiaomi `分布式系统工程师实习生`
- Xiaomi `测试开发实习—武汉`

### Usually avoid

- `Algorithm Engineer Intern for AI Innovation`
- Foundation model / multimodal pretraining roles
- Vision generation / 3D / autonomous driving algorithm roles
- Speech / NLP algorithm roles that explicitly require `PyTorch`, fine-tuning, RLHF, `DeepSpeed`, `Megatron-LM`, or top-tier research output

## Notes

- This repo is intentionally evidence-driven. The fit notes are based on current projects and resumes:
  - `ScholarFlow`
  - `multi-cloud-email-sender`
  - `multi-agent-skills-catalog`
- It is meant to support application strategy and tailored resume generation, not to store fabricated claims.
- The raw `data/` exports are intentionally kept separate from the curated root `catalog.csv` so large site dumps do not pollute the reviewed shortlist.
