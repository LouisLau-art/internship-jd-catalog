from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TargetRoleProfile:
    title: str
    fit: str
    reason: str
    resume_alias: str
    generator_script: str | None = None
    fallback_alias: str | None = None


@dataclass(frozen=True)
class CompanyFitProfile:
    key: str
    preferred_lanes: tuple[str, ...]
    boost_keywords: tuple[str, ...]
    downrank_titles: tuple[str, ...]
    default_top_n: int
    targets: tuple[TargetRoleProfile, ...]


FIT_PROFILES: dict[str, CompanyFitProfile] = {
    "xiaomi": CompanyFitProfile(
        key="xiaomi",
        preferred_lanes=("agent", "backend", "efficiency"),
        boost_keywords=("Agent", "AI编码", "研发效能", "MCP", "RAG", "平台"),
        downrank_titles=("测试开发实习—武汉",),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="AI Agent开发实习生",
                fit="very strong",
                reason="AI 编码 Agent、多 Agent 协作、代码检索与质量验证都和当前主线高度贴合。",
                resume_alias="刘新宇-小米-AI Agent开发实习生",
                generator_script="resumes/scripts/generate_extra_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="Miclaw-AI agent开发实习生",
                fit="very strong",
                reason="Miclaw 里的编码 Agent / 工程体系方向与 AI coding、任务拆解、自动验证这条线一致。",
                resume_alias="刘新宇-小米-AI Agent开发实习生",
                generator_script="resumes/scripts/generate_extra_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="大模型Agent开发工程师实习生",
                fit="very strong",
                reason="偏 MCP、RAG、Agent 平台化、推理链路与工具编排，也是当前很强的匹配点。",
                resume_alias="刘新宇-小米-大模型Agent开发工程师实习生",
                generator_script="resumes/scripts/generate_extra_bigtech_resumes.py",
            ),
        ),
    ),
    "alibaba": CompanyFitProfile(
        key="alibaba",
        preferred_lanes=("agent", "ai_application", "efficiency"),
        boost_keywords=("AI应用", "AI Agent", "AI Coding", "Prompt", "Context", "工程效能"),
        downrank_titles=("AI产品经理", "AI应用产品经理", "AI Agent产品经理"),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="AI应用研发工程师",
                fit="very strong",
                reason="JD 同时覆盖 LLM 应用开发、RAG、上下文工程和 AI 编程工具协同，是阿里主线里最贴的一条。",
                resume_alias="刘新宇-阿里巴巴-AI应用研发工程师",
                generator_script="resumes/scripts/generate_alibaba_resumes.py",
            ),
            TargetRoleProfile(
                title="AI Agent应用开发工程师",
                fit="very strong",
                reason="更偏 Agent workflow、工具链编排和工程化落地，和当前 MCP/Skills/CLI Agent 叙事高度一致。",
                resume_alias="刘新宇-阿里巴巴-AI-Agent应用开发工程师",
                generator_script="resumes/scripts/generate_alibaba_resumes.py",
            ),
            TargetRoleProfile(
                title="AI应用开发工程师实习生",
                fit="strong",
                reason="偏 AI 应用开发实习落地，虽然没有前两个聚焦，但依然能用现有 AI 应用工程证据支撑。",
                resume_alias="刘新宇-阿里巴巴-AI应用研发工程师",
                generator_script="resumes/scripts/generate_alibaba_resumes.py",
            ),
        ),
    ),
    "antgroup": CompanyFitProfile(
        key="antgroup",
        preferred_lanes=("agent", "ai_application", "platform"),
        boost_keywords=("AI", "Agent", "PaaS", "知识工程", "金融AI", "研发效能"),
        downrank_titles=("【转正实习】AI客户端", "【转正实习】AI产品经理"),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="【转正实习】AI工程师-应用方向",
                fit="very strong",
                reason="转正线里最贴近 AI 应用研发、Agent workflow 和工具链落地，适合继续主攻。",
                resume_alias="刘新宇-蚂蚁-AI工程师-应用方向",
                generator_script="resumes/scripts/generate_antgroup_resumes.py",
            ),
            TargetRoleProfile(
                title="蚂蚁数字科技-研发工程师（金融AI）",
                fit="very strong",
                reason="偏垂直业务 AI 应用工程，能直接承接你做过的复杂业务流程 + AI 工具链交付叙事。",
                resume_alias="刘新宇-蚂蚁-研发工程师-金融AI",
                generator_script="resumes/scripts/generate_gap_resumes.py",
            ),
            TargetRoleProfile(
                title="蚂蚁数字科技-AI PaaS平台开发（训推/知识工程）",
                fit="very strong",
                reason="偏知识工程、平台层和 Agent 能力组织，与 MCP/Skills/上下文治理这条线高度匹配。",
                resume_alias="刘新宇-蚂蚁-AI-PaaS平台开发-训推知识工程",
                generator_script="resumes/scripts/generate_gap_resumes.py",
            ),
        ),
    ),
    "bytedance": CompanyFitProfile(
        key="bytedance",
        preferred_lanes=("agent", "backend", "ai_application"),
        boost_keywords=("AI Agent", "Dev Agent", "开发者服务", "用户增长", "后端"),
        downrank_titles=("Seed团队-大模型研发实习生",),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="AI Agent服务端研发实习生-开发者服务",
                fit="very strong",
                reason="直接命中 AI Agent 服务端、开发者服务和效能工具链方向，是字节里最强的一条。",
                resume_alias="刘新宇-字节跳动-AI-Agent服务端研发实习生",
                generator_script="resumes/scripts/generate_bytedance_resumes.py",
            ),
            TargetRoleProfile(
                title="Dev Agent后端开发实习生-开发者服务",
                fit="very strong",
                reason="同样偏开发者服务和 Agent 后端编排，和当前工作流治理、自动化、工具调用高度相关。",
                resume_alias="刘新宇-字节跳动-Dev-Agent后端开发实习生",
                generator_script="resumes/scripts/generate_bytedance_resumes.py",
            ),
            TargetRoleProfile(
                title="AI研发实习生-剪映CapCut用户增长",
                fit="strong",
                reason="偏 AI 应用增长和产品落地，虽然没有前两个纯工程效能那么贴，但依旧是可打的强匹配。",
                resume_alias="刘新宇-字节跳动-AI研发实习生-剪映CapCut用户增长",
                generator_script="resumes/scripts/generate_bytedance_resumes.py",
            ),
        ),
    ),
    "meituan": CompanyFitProfile(
        key="meituan",
        preferred_lanes=("efficiency", "backend", "ai_application"),
        boost_keywords=("工程基建", "AI产品", "AI Coding", "后端", "研发效能"),
        downrank_titles=("AI方向后端开发工程师（实习）",),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="开发工程师实习生（工程基建方向）",
                fit="very strong",
                reason="研发效能、工程基建和内部基础设施方向与你当前的 skills/catalog/自动化经验最贴。",
                resume_alias="刘新宇-美团-开发工程师实习生-工程基建方向",
                generator_script="resumes/scripts/generate_meituan_resumes.py",
            ),
            TargetRoleProfile(
                title="基础技术-AI Coding项目实习生",
                fit="very strong",
                reason="AI Coding 和开发者提效几乎就是当前主线，适合直接打 Agent workflow 与 AI 编程叙事。",
                resume_alias="刘新宇-美团-基础技术-AI-Coding项目实习生",
                generator_script="resumes/scripts/generate_meituan_resumes.py",
            ),
            TargetRoleProfile(
                title="AI产品服务端开发实习生",
                fit="strong",
                reason="偏 AI 产品后端服务编排和业务落地，能用现有后端与工具链工程经验支撑。",
                resume_alias="刘新宇-美团-AI产品服务端开发实习生",
                generator_script="resumes/scripts/generate_gap_resumes.py",
            ),
        ),
    ),
    "jd": CompanyFitProfile(
        key="jd",
        preferred_lanes=("ai_application", "backend", "fullstack"),
        boost_keywords=("AI创新应用", "业务落地", "工作流", "全栈"),
        downrank_titles=(),
        default_top_n=1,
        targets=(
            TargetRoleProfile(
                title="AI创新应用（人力资源方向）",
                fit="strong",
                reason="偏垂直业务 AI 创新落地，和你擅长把复杂流程抽象成可交付系统的能力比较匹配。",
                resume_alias="刘新宇-京东-AI创新应用-人力资源方向",
                generator_script="resumes/scripts/generate_jd_resumes.py",
            ),
        ),
    ),
    "tencent": CompanyFitProfile(
        key="tencent",
        preferred_lanes=("ai_application", "backend", "platform"),
        boost_keywords=("AI应用", "后台开发", "Agent", "业务提效"),
        downrank_titles=("AI IT Engineer Intern 106786",),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="AI应用开发",
                fit="very strong",
                reason="腾讯里最标准的 AI 应用工程岗位，可以直接承接 Agent workflow、RAG 和 AI Native 交付叙事。",
                resume_alias="刘新宇-腾讯-AI应用开发",
                generator_script="resumes/scripts/generate_tencent_resumes.py",
            ),
            TargetRoleProfile(
                title="软件开发-后台开发方向",
                fit="strong",
                reason="更稳的后台工程入口，能用现有复杂业务系统和稳定性排障经验讲清楚。",
                resume_alias="刘新宇-腾讯-软件开发-后台开发方向",
                generator_script="resumes/scripts/generate_tencent_resumes.py",
            ),
            TargetRoleProfile(
                title="财经线培训生-AI应用开发",
                fit="strong",
                reason="偏职能和业务提效侧 AI 应用落地，也能承接产品化和复杂流程自动化的故事。",
                resume_alias="刘新宇-腾讯-财经线培训生-AI应用开发",
                generator_script="resumes/scripts/generate_tencent_resumes.py",
            ),
        ),
    ),
    "xiaohongshu": CompanyFitProfile(
        key="xiaohongshu",
        preferred_lanes=("agent", "ai_application", "fullstack"),
        boost_keywords=("AI Native", "产品工程师", "Java后端", "全栈", "研发工具链"),
        downrank_titles=("AI音频音乐算法实习生", "【26/27届实习】计算机视觉&多模态算法实习生-智能创作"),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="【27届实习】Product Engineer-产品工程师（AI应用方向）-质效研发",
                fit="very strong",
                reason="AI Native 研发工具链、代码生成、测试验证和独立交付都和当前主线几乎完全对齐。",
                resume_alias="刘新宇-小红书-产品工程师-AI应用方向-质效研发",
                generator_script="resumes/scripts/generate_xhs_resumes_tailored.py",
            ),
            TargetRoleProfile(
                title="【27届实习】Product Engineer-产品工程师（AI/全栈/应用研发方向）-商业技术",
                fit="strong",
                reason="偏 AI 应用 + 全栈交付，虽然不是质效研发那条最强主线，但仍然适合用同套产品工程师叙事去打。",
                resume_alias="刘新宇-小红书-产品工程师-AI应用方向-质效研发",
                generator_script="resumes/scripts/generate_xhs_resumes_tailored.py",
            ),
            TargetRoleProfile(
                title="Java后端开发实习生",
                fit="strong",
                reason="是更稳的后端入口，能结合复杂流程系统、稳定性治理和接口交付经验来讲。",
                resume_alias="刘新宇-小红书-Java后端AI Agent实习生",
                generator_script="resumes/scripts/generate_xhs_resumes.py",
            ),
        ),
    ),
    "huawei": CompanyFitProfile(
        key="huawei",
        preferred_lanes=("agent", "ai_application", "backend"),
        boost_keywords=("Agent", "AI应用", "通用软件", "后端", "系统软件"),
        downrank_titles=("AI模型工程师 - 多模态大模型",),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="AI模型工程师 - Agent技术",
                fit="very strong",
                reason="Agent 技术方向和你当前的 MCP/Skills/多步骤工作流工程实践高度一致。",
                resume_alias="刘新宇-华为-AI模型工程师-Agent技术",
                generator_script="resumes/scripts/generate_huawei_resumes.py",
            ),
            TargetRoleProfile(
                title="AI应用工程师 - AI技术应用",
                fit="very strong",
                reason="偏 AI 应用落地、模型能力集成和工程实现，和当前最成熟的项目证据贴合度很高。",
                resume_alias="刘新宇-华为-AI应用工程师-AI技术应用",
                generator_script="resumes/scripts/generate_huawei_resumes.py",
            ),
            TargetRoleProfile(
                title="软件开发工程师 - 通用软件",
                fit="strong",
                reason="通用软件是更稳的工程入口，能用全栈交付、后端实现和稳定性建设能力覆盖。",
                resume_alias="刘新宇-华为-软件开发工程师-通用软件",
                generator_script="resumes/scripts/generate_huawei_resumes.py",
            ),
        ),
    ),
    "netease": CompanyFitProfile(
        key="netease",
        preferred_lanes=("agent", "ai_application", "backend"),
        boost_keywords=("AI", "Agent", "应用开发", "平台", "服务端"),
        downrank_titles=("LLM/VLM研究型 Agent 实习生（开放世界游戏方向）", "Agent模型算法实习生"),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="AI 应用开发实习生",
                fit="very strong",
                reason="JD 直接点名 Agent、RAG、Function Calling、Tool Use、Multi-Agent 和 AI Coding，和当前主线最贴。",
                resume_alias="刘新宇-网易-AI应用开发实习生",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="AI平台研发工程师（27届+广）",
                fit="strong",
                reason="偏 AI 应用基础设施、Agent 套件、模型测评和模型路由，和平台化叙事匹配。",
                resume_alias="刘新宇-网易-AI平台研发工程师",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="服务端开发工程师（27届+广）",
                fit="strong",
                reason="更偏后端平台、高可用服务和自动化，适合后端工程与稳定性交付路线。",
                resume_alias="刘新宇-网易-服务端开发工程师",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
        ),
    ),
    "pinduoduo": CompanyFitProfile(
        key="pinduoduo",
        preferred_lanes=("backend", "ai_application", "frontend"),
        boost_keywords=("服务端", "大模型", "前端"),
        downrank_titles=("安全实习生",),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="服务端研发实习生",
                fit="strong",
                reason="最稳的主投岗位，和后端开发、数据处理、接口联调经验最一致。",
                resume_alias="刘新宇-拼多多-服务端研发实习生",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="大模型算法实习生",
                fit="medium",
                reason="不是纯论文型路径，但 LLM / Agent / RAG 工程实践足以支撑一轮冲刺。",
                resume_alias="刘新宇-拼多多-大模型算法实习生",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="web前端研发实习生",
                fit="medium",
                reason="有真实的 Next.js / React 全栈交付经验，可走复杂业务系统前后端闭环叙事。",
                resume_alias="刘新宇-拼多多-web前端研发实习生",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
        ),
    ),
    "didi": CompanyFitProfile(
        key="didi",
        preferred_lanes=("stability", "backend", "platform"),
        boost_keywords=("后端", "稳定性", "平台", "企业服务", "网约车"),
        downrank_titles=("Artificial Intelligence-后端研发实习生", "技术/后端研发实习生"),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="网约车技术部-后端研发实习生",
                fit="strong",
                reason="已核详情，偏稳定性平台、SLA/SLO、监控报警、故障应急和 AIOps。",
                resume_alias="刘新宇-滴滴-网约车技术部-后端研发实习生",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="网约车平台公司-后端研发实习生",
                fit="strong",
                reason="已核详情，偏功能开发、接口对接、MySQL 查询处理与问题排查，是更稳的业务后端坑位。",
                resume_alias="刘新宇-滴滴-网约车平台公司-后端研发实习生",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="企业服务事业群（3）-后端研发实习生",
                fit="strong",
                reason="已核详情，偏协同办公平台、后台服务、功能交付和技术文档沉淀。",
                resume_alias="刘新宇-滴滴-企业服务事业群-后端研发实习生",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
        ),
    ),
    "kuaishou": CompanyFitProfile(
        key="kuaishou",
        preferred_lanes=("agent", "efficiency", "ai_application"),
        boost_keywords=("Agent", "AI应用", "效率工程", "研发效能", "AgentOps"),
        downrank_titles=("AI游戏客户端开发实习生",),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="AI Agent 研发工程师 - 实习生",
                fit="very strong",
                reason="JD 直接要求 Multi-Agent、Memory、RAG、Prompt、上下文机制和 Agentic AI，几乎就是当前主线。",
                resume_alias="刘新宇-快手-AI-Agent研发工程师-实习生",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="AI Agent研发实习生（AgentOps方向）",
                fit="very strong",
                reason="偏 Agent 评测、可观测性、成本治理、回归测试和 LLMOps / AgentOps，与你做过的审计、校验和治理非常贴。",
                resume_alias="刘新宇-快手-AI-Agent研发实习生-AgentOps方向",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="AI应用开发实习生 - 【效率工程部】",
                fit="very strong",
                reason="偏 AI 工程化、提示词工程、Multi-Agent 上下文工程和研发提效，是另一条非常强的叙事。",
                resume_alias="刘新宇-快手-AI应用开发实习生-效率工程部",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
        ),
    ),
    "honor": CompanyFitProfile(
        key="honor",
        preferred_lanes=("evaluation", "algorithm", "software"),
        boost_keywords=("AI", "算法", "评测", "软件系统"),
        downrank_titles=("机器人整机架构师", "机器人硬件开发工程师"),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="AI模型能力评测工程师",
                fit="medium",
                reason="荣耀里最值得先投的一条，和评测、回归、诊断、质量保障这条线最贴。",
                resume_alias="刘新宇-荣耀-AI模型能力评测工程师",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="互联网算法工程师",
                fit="medium",
                reason="更像应用型算法 + 工程落地路线，不是最强主线但还能讲通。",
                resume_alias="刘新宇-荣耀-互联网算法工程师",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="机器人软件系统开发工程师",
                fit="medium",
                reason="机器人不是核心主线，但比纯硬件或强化学习更适合当前背景。",
                resume_alias="刘新宇-荣耀-机器人软件系统开发工程师",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
        ),
    ),
    "oppo": CompanyFitProfile(
        key="oppo",
        preferred_lanes=("agent", "efficiency", "backend"),
        boost_keywords=("AI Agent", "AIOps", "后端", "应用开发", "AI系统"),
        downrank_titles=("AI研究员（AI智能体）", "AI研究员（智能体检索）"),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="应用开发工程师（AI Agent方向）",
                fit="very strong",
                reason="JD 明写 Claude Code / Codex / MCP / Agent Skills / FastAPI / 前端经验 / 开源项目，几乎逐条对齐。",
                resume_alias="刘新宇-OPPO-应用开发工程师-AI-Agent方向",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="应用开发工程师（AI Infra/AIOps方向）",
                fit="very strong",
                reason="偏 AI DevOps、Agent Skills、CLI 助手、Linux、复杂问题定位和研发效能自动化，也极强匹配。",
                resume_alias="刘新宇-OPPO-应用开发工程师-AI-Infra-AIOps方向",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="后端工程师",
                fit="strong",
                reason="覆盖平台服务、大模型训练推理框架、机器学习平台和 AI 业务后端，也值得投。",
                resume_alias="刘新宇-OPPO-后端工程师",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
        ),
    ),
    "bilibili": CompanyFitProfile(
        key="bilibili",
        preferred_lanes=("agent", "ai_application", "backend"),
        boost_keywords=("Agent", "AI开发", "应用工程", "Python", "Flask", "创作"),
        downrank_titles=("视频生成大模型算法实习生", "算法实习生（推荐算法）", "搜索大语言模型算法实习生【2027届】"),
        default_top_n=3,
        targets=(
            TargetRoleProfile(
                title="AI开发实习生（应用工程方向）【2027届】",
                fit="very strong",
                reason="JD 直接点名 AI Agent、Agentic Workflow、MCP、Skills、多 Agent 协作和评测体系，几乎就是当前主线。",
                resume_alias="刘新宇-哔哩哔哩-AI开发实习生-应用工程方向",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="AI创作开发实习生【2027届】",
                fit="strong",
                reason="偏 AI Agent 视频创作系统、自动化工作流和工具链建设，适合讲 AI Native 产品与 workflow 落地。",
                resume_alias="刘新宇-哔哩哔哩-AI创作开发实习生",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
            TargetRoleProfile(
                title="AI创作系统后端实习生（Python/Flask）",
                fit="strong",
                reason="更稳的 Python 后端入口，service/repository、Redis、接口与文档规范都能用现有项目证据支撑。",
                resume_alias="刘新宇-哔哩哔哩-AI创作系统后端实习生-Python-Flask",
                generator_script="resumes/scripts/generate_unapplied_bigtech_resumes.py",
            ),
        ),
    ),
}


def get_fit_profile(company_key: str) -> CompanyFitProfile:
    normalized = company_key.strip().lower()
    try:
        return FIT_PROFILES[normalized]
    except KeyError as exc:
        raise KeyError(f"unknown fit profile: {normalized}") from exc
