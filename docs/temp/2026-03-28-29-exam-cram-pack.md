# 2026-03-28 / 2026-03-29 笔试冲刺包

## 已确认考试

- 阿里巴巴在线笔试：2026-03-28 14:00（北京时间）
- 小红书在线考试：2026-03-29 19:00-21:00（北京时间）
- 蚂蚁集团：已进入笔试链路，邮件未给出本轮明确开考时点

## 最高优先 GitHub 真题源

### 1. 公司笔试真题索引

- 阿里真题索引：
  [DerekLin924/bat_code 阿里笔试](https://github.com/DerekLin924/bat_code/blob/83adffda48ad1dd5edae4f7b00acd49423805589/%E9%98%BF%E9%87%8C%E7%AC%94%E8%AF%95/alibaba.md)
  - 已收录：0315、0322、0824、0902、0909、0910、0917、0918、0920 等多场
- 蚂蚁真题索引：
  [DerekLin924/bat_code 蚂蚁金服笔试](https://github.com/DerekLin924/bat_code/blob/83adffda48ad1dd5edae4f7b00acd49423805589/%E8%9A%82%E8%9A%81%E9%87%91%E6%9C%8D%E7%AC%94%E8%AF%95/mayi.md)
  - 已收录：0404、0420、0905、0914A、0914B、0919
- 小红书真题索引：
  [DerekLin924/bat_code 小红书笔试](https://github.com/DerekLin924/bat_code/blob/83adffda48ad1dd5edae4f7b00acd49423805589/%E5%B0%8F%E7%BA%A2%E4%B9%A6%E7%AC%94%E8%AF%95/red.md)
  - 已收录：0326、0723、0806、0819

### 2. GitHub 归档的牛客帖子线索

- 小红书归档页：
  [hxh5/nowcoder 2023-08-06](https://github.com/hxh5/nowcoder/blob/009b4cb4603baad53e0cfde837f5ebe7755f0aac/20230806/230035_1691334035678_9044.md)
  - 这页能看到这些标题：`小红书前端笔试20道选择，3道编程赛码`、`小红书正式pi后端第一场笔试题`、`2023/8/6 小红书秋招Java后端笔试（AK）`
- 近期归档页：
  [hxh5/nowcoder 2024-04-09](https://github.com/hxh5/nowcoder/blob/009b4cb4603baad53e0cfde837f5ebe7755f0aac/20240409/110050_1712631650263_9178.md)
  - 这页能看到这些标题：`小红书前端笔试4.7+3.26（附题解）`、`阿里一面完后发了笔试`
- 蚂蚁归档页：
  [hxh5/nowcoder 2024-03-23](https://github.com/hxh5/nowcoder/blob/009b4cb4603baad53e0cfde837f5ebe7755f0aac/20240323/210035_1711198835414_8057.md)
  - 这页能看到这些标题：`蚂蚁集团笔试`、`3/23 蚂蚁笔试`、`有友友做了2024/3/23日蚂蚁的笔试`

### 3. 大而全模拟库

- 总库：
  [0voice/Campus_recruitment_interview_questions](https://github.com/0voice/Campus_recruitment_interview_questions)
  - README 标明收录 1000+ 真实面试题/面经，覆盖阿里、蚂蚁、小红书等
- 阿里专题：
  [0voice 阿里题库入口](https://github.com/0voice/Campus_recruitment_interview_questions/blob/main/%E9%98%BF%E9%87%8C/readme.md)
- 小红书专题：
  [0voice 小红书题库入口](https://github.com/0voice/Campus_recruitment_interview_questions/blob/main/%E5%B0%8F%E7%BA%A2%E4%B9%A6%E9%9D%A2%E8%AF%95%E9%A2%98%E8%A7%86%E9%A2%91%E8%AE%B2%E8%A7%A3/readme.md)
- 蚂蚁专题：
  [0voice 蚂蚁题库入口](https://github.com/0voice/Campus_recruitment_interview_questions/blob/main/%E8%9A%82%E8%9A%81%E9%9D%A2%E8%AF%95%E9%A2%98%E8%A7%86%E9%A2%91%E8%AE%B2%E8%A7%A3/readme.md)

## 题型判断

## 方向校正

### 之前找到的阿里真题，是否就是这个方向？

- 不是严格意义上的“`AI应用研发工程师` 定向真题”。
- 之前的主真题源 [DerekLin924/bat_code 阿里笔试](https://github.com/DerekLin924/bat_code/blob/83adffda48ad1dd5edae4f7b00acd49423805589/%E9%98%BF%E9%87%8C%E7%AC%94%E8%AF%95/alibaba.md) 里，主要是：
  - 阿里云笔试 0910
  - 阿里云研发岗 0917
  - 阿里云算法岗 0917
  - 淘天 / 达摩院 / 国际业务等场次
- 也就是说，这批题更像“阿里技术岗通用研发笔试题池”，不是 GitHub 上明确标注 `AI应用研发工程师` 的专门卷。

### 但你的岗位也不是纯算法岗

- 结合仓库本地 JD，`AI应用研发工程师` 的要求明显偏 `AI应用开发 / Agent工程落地`，不是纯大模型训练或纯算法研究：
  - 要求重度使用 `Cursor`、`Claude Code`
  - 强调 `Prompt Engineering`、`Context Engineering`
  - 强调 `Agent`、`工具/函数调用`
  - 提到 `LangChain`
  - 明确要求考虑 `幻觉`、`Prompt 注入` 的工程化应对
  - 加分项直接写了 `RAG`、`多智能体`、`MCP`、`Skill`
- 仓库里的 `AI应用开发工程师实习生` 也明确写了：
  - `Agent系统`
  - `LangChain / LlamaIndex`
  - `Prompt`
  - `RAG`
  - `知识图谱`
  - `效果评估`

### 当前最合理的准备比例

- `60%`：阿里通用研发笔试基础
  - 算法
  - 数据结构
  - 计算机网络
  - 操作系统
  - 常见后端基础
- `40%`：AI应用 / Agent 方向补充
  - Prompt / Context Engineering
  - RAG 基本链路
  - Tool Calling / Function Calling
  - Agent / Multi-Agent
  - 幻觉 / Prompt 注入 / 评测 / 兜底

### 阿里 / 蚂蚁

- 高概率不是纯算法卷，至少会混入后端基础。
- 依据：
  `0voice` 的阿里部分首页就把 MySQL、B+ 树、TCP、Redis、系统设计类问题放在前面。
- 备考重心：
  - 数组 / 字符串 / 哈希 / 双指针
  - 排序 / 贪心 / 二分 / 基础 DP
  - MySQL 索引 / 事务 / 执行流程
  - TCP 三次握手 / 四次挥手 / 可靠传输
  - Redis 常见数据结构与缓存一致性

### 小红书

- 推断更像 `选择题 + ACMCoder 编程题` 的混合模式。
- 依据：
  GitHub 归档标题里反复出现 `20道选择，3道编程赛码`、`Java后端笔试`、`正式pi后端第一场笔试题`。
- 你的邮件也明确落在 `test.acmcoder.com`，并要求摄像头、录屏、Chrome 作答。
- 备考重心：
  - 赛码风格基础编程题：数组、字符串、哈希、栈、队列、滑窗、基础 DP
  - JS / 浏览器 / 网络 / 工程化 / 测试基础
  - 120 分钟内做题节奏，而不是单题深挖

## AI 应用方向补充 GitHub 源

### 这些不是阿里定向真题，但更贴近你的岗位要求

- [adongwanai/AgentGuide](https://github.com/adongwanai/AgentGuide)
  - 明确把岗位拆成 `算法工程师线` 和 `开发工程师线`
  - 直接覆盖 `LangChain`、`LangGraph`、`RAG`、`Multi-Agent`、`Memory`、`系统设计`、`面试题库`
- [wdndev/llm_interview_note](https://github.com/wdndev/llm_interview_note)
  - 主题就是 `LLMs 算法（应用）工程师相关知识及面试题`
- [WeThinkIn/AIGC-Interview-Book](https://github.com/WeThinkIn/AIGC-Interview-Book)
  - 覆盖 `AIGC`、`AI Agent`、机器学习、NLP、强化学习与大厂高频算法题
- [liguodongiot/llm-action](https://github.com/liguodongiot/llm-action)
  - 偏 `大模型工程化 / 应用落地`
  - 仓库里明确有 `大模型应用常见面试题`
- [liyupi/ai-code-helper](https://github.com/liyupi/ai-code-helper)
  - 不是真题库，但项目栈非常像 `AI应用研发`
  - 覆盖 `Prompt`、`RAG`、`向量数据库`、`Tool Calling`、`MCP`

### 怎么用这些补方向

- 不要把这些仓库当成“刷完整教程”。
- 只用来补 5 类最可能被问到的方向词：
  - `Prompt`
  - `RAG`
  - `Agent`
  - `Tool Calling`
  - `MCP / Memory / 评测`

## 冲刺顺序

### 今晚：阿里优先，蚂蚁补位

1. 阿里 0910
2. 阿里 0917 研发岗
3. 蚂蚁 0914A
4. 还有时间再做蚂蚁 0919

### 明天阿里笔试结束后：切到小红书

1. 小红书 0806
2. 小红书 0326
3. 打开 `hxh5/nowcoder` 的小红书归档页，只看带这些词的帖子标题：
   - `赛码`
   - `3道编程`
   - `Java后端`
   - `正式pi`

## 最小可执行版本

- 如果时间已经不够，至少完成这 6 个入口：
  - 阿里 0910
  - 阿里 0917 研发岗
  - 蚂蚁 0914A
  - 小红书 0806
  - 小红书 0326
  - 0voice 阿里题库入口

## 注意

- 这里的“题型判断”里，小红书部分是基于 GitHub 归档标题和你的考试邮件做的推断，不是官方规则原文。
- 真题索引仓库最有用；大而全题库只拿来补薄弱点，不要反过来主刷大题库。
