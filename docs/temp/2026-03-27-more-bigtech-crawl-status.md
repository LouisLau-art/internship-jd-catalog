# 额外大厂技术实习抓取状态

更新时间：`2026-03-28`

## 本轮已正式落库

| 公司 | 官方入口 | 当前结果 | 导出文件 |
| --- | --- | --- | --- |
| 快手 | `https://zhaopin.kuaishou.cn/recruit/#/official/trainee/` | 技术类实习 `286` 个 | [kuaishou_positions_intern_tech.json](/home/louis/internship-jd-catalog/data/kuaishou_positions_intern_tech.json) |
| 荣耀 | `https://career.honor.com/SU61b9b9992f9d24431f5050a5/pb/interns.html` | 研发类实习 `18` 个 | [honor_positions_intern_tech.json](/home/louis/internship-jd-catalog/data/honor_positions_intern_tech.json) |
| OPPO | `https://careers.oppo.com/university/oppo/campus/post?recruitType=Intern` | 技术类实习 `74` 个 | [oppo_positions_intern_tech.json](/home/louis/internship-jd-catalog/data/oppo_positions_intern_tech.json) |
| 哔哩哔哩 | `https://jobs.bilibili.com/campus/positions?practiceTypes=1&type=0` | 当前实习页 `0` 个 | [bilibili_positions_intern_tech.json](/home/louis/internship-jd-catalog/data/bilibili_positions_intern_tech.json) |

同日也刷新了另一组未投公司数据：
- 网易：`63`
- 拼多多：`6`
- 滴滴：`75`
- 小米：`376`

汇总导出：
- [more_bigtech_positions.json](/home/louis/internship-jd-catalog/data/more_bigtech_positions.json)
- [more_bigtech_positions.csv](/home/louis/internship-jd-catalog/data/more_bigtech_positions.csv)

## 口径说明

- 只保留 `技术类 / 实习`。
- 快手按官方接口中的 `工程类`、`算法类` 过滤，并额外剔除了少量 `剧情策划 / 设计师 / 技术美术` 这类边缘岗。
- 荣耀按官方接口中的 `研发类 + 实习` 过滤。
- OPPO 按官方接口中的 `AI/算法类 / 标准研究类 / 软件类 / 硬件类 / 工程技术类` 过滤。
- 哔哩哔哩当前官方实习页明确显示 `职位列表（0）`，所以本地也显式导出了零结果，而不是留空不处理。

## 当前脚本

- [scrape_more_bigtech.py](/home/louis/internship-jd-catalog/scripts/scrape_more_bigtech.py)
- [test_scrape_more_bigtech.py](/home/louis/internship-jd-catalog/tests/test_scrape_more_bigtech.py)

## 下一波候选

- `百度`：官网明确有实习入口，但当前还没稳定拿到可持续复跑的职位接口。
- `vivo`：目前确认到的是社招职位接口，不是校园实习口径，暂时不并入。

## 你回来后最值得先看

1. [2026-03-27-xiaomi-agent-11-shortlist.md](/home/louis/internship-jd-catalog/docs/temp/2026-03-27-xiaomi-agent-11-shortlist.md)
2. [more_bigtech_positions.json](/home/louis/internship-jd-catalog/data/more_bigtech_positions.json)
