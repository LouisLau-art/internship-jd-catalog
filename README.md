# Internship JD Catalog

Collected internship job descriptions and quick-fit notes for Louis Lau.

## Snapshot

- Current snapshot date: `2026-03-20`
- Total pasted entries persisted: `29`
- Unique JD count after de-duplicating one repeated Xiaomi backend posting: `28`
- Companies covered:
  - `Xiaomi`
  - `Xiaohongshu`
- Raw export pools captured:
  - `Alibaba`: `449`
  - `Ant Group`: `96`

## What is in this repo

- [catalog.csv](./catalog.csv)
  Flat index for quick filtering by company, track, fit, and notes.
- [docs/companies/xiaomi.md](./docs/companies/xiaomi.md)
  Structured notes for Xiaomi postings, including the earlier 3 algorithm roles and the later software-R&D batch.
- [docs/companies/xiaohongshu.md](./docs/companies/xiaohongshu.md)
  Structured notes for the 2 Xiaohongshu targeted internship roles.
- [docs/companies/alibaba.md](./docs/companies/alibaba.md)
  Summary note for the Alibaba raw campus export snapshot.
- [docs/companies/antgroup.md](./docs/companies/antgroup.md)
  Summary note for the Ant Group raw campus export snapshot.
- [docs/xiaomi-top-5.md](./docs/xiaomi-top-5.md)
  Ordered shortlist of the 5 Xiaomi roles currently worth prioritizing.
- [docs/alibaba-ant-top-10.md](./docs/alibaba-ant-top-10.md)
  First reviewed top-10 shortlist from the Alibaba + Ant raw export pool.

## Raw Site Exports

- [scripts/scrape_campus_jobs.py](./scripts/scrape_campus_jobs.py)
  Bulk-export utility for the Alibaba and Ant Group campus job pages.
- [data/alibaba_positions_100000540002.csv](./data/alibaba_positions_100000540002.csv)
  Raw Alibaba 2027 internship export from `2026-03-20`.
- [data/antgroup_positions_26022600074513.csv](./data/antgroup_positions_26022600074513.csv)
  Raw Ant Group 2027 return-offer internship export from `2026-03-20`.
- [data/campus_positions_combined.csv](./data/campus_positions_combined.csv)
  Combined flat export across both sites.
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

- Xiaohongshu `生态研发工程师实习生`
- Xiaohongshu `Java 后端开发实习生（AI Agent 方向）`
- Xiaomi `服务端研发实习生—武汉`
- Xiaomi `后端研发工程师实习生`（国际小米网 AI 翻译/校对）
- Xiaomi `软件研发工程师实习生`（云平台基础服务）

### Secondary apply

- Xiaomi `数据理解研发工程师实习生`
- Xiaomi `效能工具研发工程师实习生`
- Xiaomi `电商中台软件开发实习生`
- Xiaomi `分布式系统工程师实习生`
- Xiaomi `测试开发实习—武汉`

### Usually avoid

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
