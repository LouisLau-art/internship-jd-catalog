#!/usr/bin/env python3
from __future__ import annotations

import copy
import shutil
from pathlib import Path

import generate_alibaba_resumes as alibaba
import generate_extra_bigtech_resumes as extra
import generate_netease_resumes as netease
import generate_tencent_resumes as tencent
import generate_xhs_resumes as base
import generate_xhs_resumes_tailored as xhs_tailored


ROOT = Path(__file__).resolve().parent
EXPORT_DIR = ROOT.parent / "sources"
COMMON = netease.COMMON


def clone_resume(source_resumes: list[dict], source_slug: str, **updates: object) -> dict:
    for resume in source_resumes:
        if resume["slug"] == source_slug:
            data = copy.deepcopy(resume)
            data.update(updates)
            return data
    raise KeyError(source_slug)


RESUMES = [
    clone_resume(
        netease.RESUMES,
        "netease-games-ai-application-engineer-resume",
        slug="netease-ai-app-dev-intern-resume",
        alias="刘新宇-网易-AI应用开发实习生",
        title="刘新宇 - 网易 AI应用开发实习生",
        role="AI应用开发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI Agent、LLM 应用开发和全栈工程交付做实战，能够把任务规划、工具调用、知识检索与后端服务串成可上线的 AI Native 产品。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 目录并为 Codex、Claude Code、Gemini 等 CLI Agent 配置 MCP。与网易这条 JD 里的 AI Agent、RAG、Function Calling、Tool Use、Multi-Agent、AI Coding 等要求高度匹配。",
        signals=[
            "AI Agent / Multi-Agent / MCP",
            "RAG / Function Calling / Tool Use",
            "全栈交付 + AI Native 应用落地",
            "AI Coding 工具深度使用",
        ],
        self_evaluation="偏 AI 应用与后端工程落地，能够把业务需求拆成可实现、可验证、可迭代的工作流与服务能力。做过多格式内容处理、模型路由、降级兜底、评测与可观测性建设，适合 AI 应用研发、产品化落地和业务场景工程化方向岗位。",
    ),
    clone_resume(
        netease.RESUMES,
        "netease-games-ai-application-engineer-resume",
        slug="netease-ai-platform-rd-engineer-resume",
        alias="刘新宇-网易-AI平台研发工程师",
        title="刘新宇 - 网易 AI平台研发工程师",
        role="AI平台研发工程师",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI 应用工程、Agent 平台、模型评测与服务编排做实践，能够把大模型能力转成可部署、可观测、可持续优化的产品与平台能力。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 公共目录，并在 MCP、RAG、模型路由和复杂工作流落地方面积累了较多工程经验。与网易这条游戏研发管线 AI 应用、Agent 套件、模型测评与模型路由 JD 强匹配。",
        signals=[
            "AI 平台 / Agent 套件 / 模型评测",
            "模型路由 / RAG / Workflow 编排",
            "高可用服务交付与问题排查",
            "MCP / Skills / CLI Agent 实战",
        ],
    ),
    clone_resume(
        tencent.RESUMES,
        "tencent-backend-rd-resume",
        slug="netease-server-side-rd-engineer-resume",
        alias="刘新宇-网易-服务端开发工程师",
        title="刘新宇 - 网易 服务端开发工程师",
        role="服务端开发工程师",
        summary="华中师范大学计算机技术硕士在读（2027届）。深耕后端系统交付、工程稳定性与服务链路治理，能够围绕业务平台完成需求理解、接口开发、缺陷修复与线上问题排查。独立完成 ScholarFlow 与 multi-cloud-email-sender 两条完整系统链路，具备 MySQL、Redis、异步任务、日志分析与云端部署经验。与网易这条高性能、高可用服务平台方向的服务端岗位更贴近，适合强调后端开发、自动化、可观测性与 AIOps 相关实践。",
        signals=[
            "后端开发 / 高可用服务 / 接口联调",
            "MySQL / Redis / 异步任务 / 日志排障",
            "自动化 / 可观测性 / AIOps 认知",
            "真实业务系统端到端交付",
        ],
    ),
    clone_resume(
        tencent.RESUMES,
        "tencent-backend-rd-resume",
        slug="pdd-server-side-rd-intern-resume",
        alias="刘新宇-拼多多-服务端研发实习生",
        title="刘新宇 - 拼多多 服务端研发实习生",
        role="服务端研发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。深耕后端系统交付、工程稳定性和数据链路治理，能够把需求分析、接口开发、批量任务处理和线上排障整合成可上线的后端能力。独立完成 ScholarFlow 与 multi-cloud-email-sender 的端到端交付，具备真实数据导入、任务调度、接口联调和日志诊断经验。对拼多多技术专场里的服务端研发岗位是更稳的主投选择，匹配点在于后端开发、数据处理、稳定性建设和高效率执行。",
        signals=[
            "后端开发 / 数据处理 / 接口联调",
            "MySQL / Redis / 异步任务 / 调度链路",
            "工程稳定性 + 日志排障",
            "交付闭环 + 执行力强",
        ],
    ),
    clone_resume(
        alibaba.RESUMES,
        "alibaba-ai-agent-rd-engineer-resume",
        slug="pdd-llm-algorithm-intern-resume",
        alias="刘新宇-拼多多-大模型算法实习生",
        title="刘新宇 - 拼多多 大模型算法实习生",
        role="大模型算法实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI Agent、Prompt Engineering、RAG、工具调用与复杂工作流落地做工程实践，能够把大模型能力转化为真实可用的应用与自动化系统。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 公共目录，并在 MCP、上下文管理与模型应用评估方面形成稳定实践。虽然不是纯论文型算法背景，但在 LLM 应用、智能体和工程化落地方面证据更强，适合冲拼多多的大模型算法实习生岗位。",
        signals=[
            "LLM 应用 / Agent / RAG 实践",
            "Prompt Engineering / 工具调用 / 评估",
            "开源项目持续维护与工程化落地",
            "AI 能力从原型到产品的闭环交付",
        ],
    ),
    clone_resume(
        xhs_tailored.RESUMES,
        "xhs-ai-native-dev-tooling-resume",
        slug="pdd-web-front-end-rd-intern-resume",
        alias="刘新宇-拼多多-web前端研发实习生",
        title="刘新宇 - 拼多多 web前端研发实习生",
        role="web前端研发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。具备完整的全栈交付经验，能够围绕复杂业务场景完成界面设计、前后端联调、状态流转与线上部署。独立完成 ScholarFlow 与 multi-cloud-email-sender 两条完整系统链路，具备 Next.js、React、SSE、权限体系、复杂表单与仪表盘开发经验。适合拼多多这类偏产品与业务承载的 web 前端研发岗位，能够用 AI 工具提升需求拆解、组件实现与调试效率。",
        signals=[
            "Next.js / React / TypeScript / 全栈交付",
            "复杂业务界面 + 状态流转 + 联调",
            "AI Coding + 需求拆解 + 调试提效",
            "前后端协作与上线闭环经验",
        ],
    ),
    clone_resume(
        tencent.RESUMES,
        "tencent-backend-rd-resume",
        slug="didi-ride-tech-backend-intern-resume",
        alias="刘新宇-滴滴-网约车技术部-后端研发实习生",
        title="刘新宇 - 滴滴 网约车技术部后端研发实习生",
        role="网约车技术部-后端研发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕后端服务、链路可观测性、稳定性治理与问题排查做实践，能够把业务系统中的风险识别、日志诊断、指标跟踪和自动化工具串成稳定性保障链路。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条核心系统链路，并沉淀过 tracking diagnostics、异常日志定位、跨系统排障和自动化脚本经验。与滴滴这条稳定性平台、SLA/SLO/SLOI、监控报警、故障应急和 AIOps 方向高度贴近。",
        signals=[
            "稳定性平台 / 监控告警 / 故障排查",
            "日志分析 / 诊断工具 / 自动化治理",
            "后端服务 / MySQL / Redis / Docker",
            "AIOps / 可观测性 / 线上问题定位",
        ],
    ),
    clone_resume(
        tencent.RESUMES,
        "tencent-backend-rd-resume",
        slug="didi-ride-platform-backend-intern-resume",
        alias="刘新宇-滴滴-网约车平台公司-后端研发实习生",
        title="刘新宇 - 滴滴 网约车平台公司后端研发实习生",
        role="网约车平台公司-后端研发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。深耕后端交付、接口对接、问题排查和技术文档沉淀，能够围绕业务平台完成功能开发、现有模块维护和异常问题定位。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条核心系统链路，具备 MySQL、Python / Java、接口联调、缺陷修复和交付文档维护经验。与滴滴这条网约车平台后端研发岗的功能开发、内部系统接口对接、用户问题排查和文档协作要求更贴合。",
        signals=[
            "后端功能开发 / 内部系统接口对接",
            "MySQL / Python / Java / Debug 工具",
            "问题定位 / 缺陷修复 / 文档沉淀",
            "业务系统交付 + 线上稳定性经验",
        ],
    ),
    clone_resume(
        tencent.RESUMES,
        "tencent-backend-rd-resume",
        slug="didi-enterprise-service-backend-intern-resume",
        alias="刘新宇-滴滴-企业服务事业群-后端研发实习生",
        title="刘新宇 - 滴滴 企业服务事业群后端研发实习生",
        role="企业服务事业群-后端研发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。具备扎实的后端系统交付能力，能够围绕协同办公、内部平台和复杂业务需求完成设计、开发和交付。独立完成 ScholarFlow 与 multi-cloud-email-sender 两条完整系统链路，积累了接口设计、状态流转、结构化数据处理、日志诊断与跨角色协作经验。与滴滴企业服务协同办公平台方向的后端岗位匹配点在于后台服务、产品需求理解、技术文档沉淀与工程化交付。",
        signals=[
            "协同办公 / 内部平台 / 后台服务",
            "接口设计 / 状态流转 / 功能交付",
            "技术文档 / 问题处理手册 / 沟通协作",
            "Java 基础 / Python / 工程化落地",
        ],
    ),
    clone_resume(
        extra.RESUMES,
        "xiaomi-ai-agent-dev-intern-resume",
        slug="kuaishou-ai-agent-rd-engineer-intern-resume",
        alias="刘新宇-快手-AI-Agent研发工程师-实习生",
        title="刘新宇 - 快手 AI Agent研发工程师（实习生）",
        role="AI Agent研发工程师（实习生）",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 Multi-Agent 框架、Memory 机制、RAG、Prompt、工具调用和复杂工作流落地做实践，能够把模糊需求转成可运行、可验证、可持续优化的 AI Agent 系统。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 公共目录，并在 MCP、上下文治理和 Agent 协作方面形成稳定工程经验。与快手这条 Multi-Agent、Memory、RAG、Prompt、上下文机制和 Agentic AI 的 JD 强匹配。",
        signals=[
            "Multi-Agent / Memory / RAG / Prompt",
            "MCP / Skills / 上下文治理",
            "Agent 框架落地 + 工程稳定性",
            "开源维护 + 真实业务系统交付",
        ],
        self_evaluation="偏 AI Agent 系统与工作流工程落地，习惯从真实问题出发设计任务拆解、上下文管理、工具调用和结果校验闭环。做过 MCP、Skills、多 Agent 协作、评测与可观测性建设，适合 Agent 应用研发、Agent 平台和复杂工作流方向岗位。",
    ),
    clone_resume(
        extra.RESUMES,
        "xiaomi-ai-agent-dev-intern-resume",
        slug="kuaishou-ai-agentops-intern-resume",
        alias="刘新宇-快手-AI-Agent研发实习生-AgentOps方向",
        title="刘新宇 - 快手 AI Agent研发实习生（AgentOps方向）",
        role="AI Agent研发实习生（AgentOps方向）",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 Agent 工作流的评测、可观测性、回归校验和上下文治理做工程实践，能够把行为轨迹、工具调用、异常日志和质量指标串成可持续优化的 Agent 质量保障体系。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，并持续维护多 Agent skills 公共目录，补过 handoff 校验、resume coverage audit 和同步链路脚本。与快手这条 Agent 质量评估、链路可观测性、成本治理、回归测试和 LLMOps / AgentOps 方向非常贴合。",
        signals=[
            "Agent 评测 / 可观测性 / 质量保障",
            "回归测试 / 指标体系 / 日志诊断",
            "MCP / Agent 调用链路 / 上下文管理",
            "自动化审计与工程稳定性建设",
        ],
        self_evaluation="偏 AgentOps 与工程治理，关注评测、回归、可观测性、成本控制和复杂流程稳定性，能够把 AI Agent 从“能跑”推进到“可验证、可持续优化”。做过 validator 修复、日志排障、交接治理和多 Agent 协作，适合 AgentOps、评测与质效研发方向岗位。",
    ),
    clone_resume(
        netease.RESUMES,
        "netease-games-ai-application-engineer-resume",
        slug="kuaishou-ai-app-dev-efficiency-intern-resume",
        alias="刘新宇-快手-AI应用开发实习生-效率工程部",
        title="刘新宇 - 快手 AI应用开发实习生（效率工程部）",
        role="AI应用开发实习生（效率工程部）",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI 工程化落地、Prompt Engineering、Multi-Agent 上下文工程和业务提效工具做实践，能够把大模型能力转成可上线、可验证、可持续优化的生产力系统。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 公共目录，并在复杂上下文管理、工具调用和 AI Coding 提效方面积累了稳定经验。与快手这条效率工程部的 AI 工程化、提示词工程和 Multi-Agent 上下文工程岗位高度匹配。",
        signals=[
            "AI 工程化 / 提示词工程 / Multi-Agent",
            "上下文工程 / Tool Use / 生产提效",
            "Python / 异步编程 / 复杂问题定位",
            "AI Native 应用从原型到产品落地",
        ],
        self_evaluation="偏 AI 应用工程与研发提效落地，能够把业务需求拆成可实现、可验证、可迭代的工作流、接口和工具链能力。做过 Prompt / Context Engineering、MCP 接入、自动化工作流和排障闭环，适合 AI 应用开发、效率工程和研发工具方向岗位。",
    ),
    clone_resume(
        alibaba.RESUMES,
        "alibaba-ai-agent-rd-engineer-resume",
        slug="honor-ai-model-eval-engineer-resume",
        alias="刘新宇-荣耀-AI模型能力评测工程师",
        title="刘新宇 - 荣耀 AI模型能力评测工程师",
        role="AI模型能力评测工程师",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 LLM 应用评测、Agent 质量审计、工作流验证和复杂系统稳定性交付做实践，能够把指标、测试、用户反馈和日志分析沉淀为可复用的评测与优化闭环。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 公共目录，并围绕 handoff 校验、resume coverage audit 与调试链路做过多次自动化治理。对荣耀这类 AI 模型能力评测岗位，最强证据在于评估思维、质量保障和工程化验证能力。",
        signals=[
            "模型评测 / 质量审计 / 自动化验证",
            "日志分析 / 回归测试 / 评估闭环",
            "LLM / Agent 应用优化与指标化",
            "工程稳定性与复杂问题定位",
        ],
    ),
    clone_resume(
        alibaba.RESUMES,
        "alibaba-ai-application-rd-engineer-resume",
        slug="honor-internet-algorithm-engineer-resume",
        alias="刘新宇-荣耀-互联网算法工程师",
        title="刘新宇 - 荣耀 互联网算法工程师",
        role="互联网算法工程师",
        summary="华中师范大学计算机技术硕士在读（2027届）。虽然不是纯论文型算法路径，但长期围绕 AI 应用、RAG、知识检索、Prompt Engineering 和工作流优化做实践，能够把模型能力与真实业务场景结合并完成工程化落地。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 目录，并在推荐式匹配、知识检索与结果优化方面积累了较多经验。对荣耀互联网算法工程师岗位，更适合以应用型 AI 算法、工程化验证和系统落地作为主叙事。",
        signals=[
            "应用型 AI 算法 / 检索 / 优化",
            "RAG / Prompt / 工具调用 / Workflow",
            "数据处理 + 工程化落地 + 评估思维",
            "开源项目持续维护与快速学习",
        ],
    ),
    clone_resume(
        tencent.RESUMES,
        "tencent-backend-rd-resume",
        slug="honor-robot-software-system-engineer-resume",
        alias="刘新宇-荣耀-机器人软件系统开发工程师",
        title="刘新宇 - 荣耀 机器人软件系统开发工程师",
        role="机器人软件系统开发工程师",
        summary="华中师范大学计算机技术硕士在读（2027届）。具备扎实的软件系统交付能力，能够围绕复杂业务流程完成系统设计、模块开发、联调排障和文档沉淀。独立完成 ScholarFlow 与 multi-cloud-email-sender 两条完整系统链路，积累了后端服务、数据链路、接口开发、部署运维和稳定性治理经验。虽然机器人方向不是最核心主线，但对荣耀的软件系统开发岗仍有较强工程匹配度，适合强调软件系统实现、复杂模块协作和问题定位能力。",
        signals=[
            "软件系统开发 / 模块设计 / 联调排障",
            "后端服务 / 数据链路 / 工程交付",
            "复杂系统问题定位与稳定性治理",
            "技术文档与跨角色协作能力",
        ],
    ),
    clone_resume(
        extra.RESUMES,
        "xiaomi-llm-agent-engineer-intern-resume",
        slug="oppo-ai-agent-application-engineer-resume",
        alias="刘新宇-OPPO-应用开发工程师-AI-Agent方向",
        title="刘新宇 - OPPO 应用开发工程师（AI Agent方向）",
        role="应用开发工程师（AI Agent方向）",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI Agent 系统、MCP、Agent Skills、FastAPI、TypeScript 与开源项目维护做实践，能够把 AIGC/LLM 能力工程化、平台化落到研发全流程场景。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 公共目录，并深度使用 Codex、Claude Code、Gemini、Cursor 等 AI 开发工具。与 OPPO 这条 JD 中对命令行代码助手、Rules/Prompt/MCP、Agent Skills、FastAPI、前端经验、开源项目和 RAG 的要求几乎逐条对齐。",
        signals=[
            "Claude Code / Codex / MCP / Agent Skills",
            "FastAPI / TypeScript / 全栈工程交付",
            "RAG / Prompt 工程 / 开源持续维护",
            "AI Agent 系统工程化与平台化",
        ],
        self_evaluation="偏 AI Agent 与开发者工具工程落地，习惯从真实研发场景出发设计任务拆解、上下文组织、工具调用和结果校验闭环。做过 MCP、Skills、CLI Agent、多 Agent 协作和开源工具链维护，适合 AI Agent 应用开发、研发效能与 AI 工具平台方向岗位。",
    ),
    clone_resume(
        extra.RESUMES,
        "xiaomi-llm-agent-engineer-intern-resume",
        slug="oppo-ai-infra-aiops-engineer-resume",
        alias="刘新宇-OPPO-应用开发工程师-AI-Infra-AIOps方向",
        title="刘新宇 - OPPO 应用开发工程师（AI Infra/AIOps方向）",
        role="应用开发工程师（AI Infra/AIOps方向）",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI 工具链、研发效能自动化、日志诊断与平台治理做实践，能够把 AIGC/LLM 技术接入 DevOps 全生命周期，形成可观测、可调试、可持续优化的工程体系。独立完成 ScholarFlow 与 multi-cloud-email-sender 两条完整系统链路，持续维护多 Agent skills 公共目录，并在 CLI Agent、Rules、MCP、RAG、Prompt 工程和复杂问题定位方面积累了稳定证据。与 OPPO 这条 AI Infra/AIOps 岗位的 JD 高度契合。",
        signals=[
            "AI Infra / AIOps / 研发效能自动化",
            "Codex / Claude Code / Gemini CLI / MCP",
            "Linux / 日志诊断 / 复杂问题定位",
            "RAG / Prompt / 开源项目持续维护",
        ],
        self_evaluation="偏工程效能与 AI Infra/AIOps 落地，能够把 AI 能力接到命令行工具、服务接口、稳定性治理和研发自动化流程中。做过异步任务、限流重试、日志排障、回归校验和多服务协同，适合 AI 基础设施、研发效能和平台工程方向岗位。",
    ),
    clone_resume(
        tencent.RESUMES,
        "tencent-backend-rd-resume",
        slug="oppo-backend-engineer-resume",
        alias="刘新宇-OPPO-后端工程师",
        title="刘新宇 - OPPO 后端工程师",
        role="后端工程师",
        summary="华中师范大学计算机技术硕士在读（2027届）。深耕后端系统交付、平台服务开发、数据链路治理和稳定性建设，能够围绕业务平台与 AI 场景完成模块设计、接口开发、性能与可靠性优化。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整系统链路，具备 Python、Java 基础、MySQL、Redis、Linux、Docker、日志诊断和线上排障经验。与 OPPO 这条覆盖平台服务、大模型训练推理框架、机器学习平台和多模态服务的后端工程师岗位更贴合。",
        signals=[
            "后端服务 / 平台开发 / 系统稳定性",
            "Python / Java / MySQL / Redis / Linux",
            "AI 场景接入 + 工程化交付",
            "高并发链路 / 调试排障 / 可观测性",
        ],
    ),
    clone_resume(
        extra.RESUMES,
        "xiaomi-ai-agent-dev-intern-resume",
        slug="bilibili-ai-app-dev-application-engineering-intern-resume",
        alias="刘新宇-哔哩哔哩-AI开发实习生-应用工程方向",
        title="刘新宇 - 哔哩哔哩 AI开发实习生（应用工程方向）",
        role="AI开发实习生（应用工程方向）",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI Agent 系统、Agentic Workflow、MCP、Skills 与多 Agent 协作做工程实践，能够把真实业务需求拆成可实现、可验证、可迭代的 AI Native 产品能力。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 公共目录，并在 Prompt / Context Engineering、工具调用和评测闭环上积累了稳定证据。与哔哩哔哩这条应用工程方向 JD 里提到的 Agent 开发、MCP 服务器、Skills、Hooks、多 Agent 协作和评测体系高度匹配。",
        signals=[
            "AI Agent / Agentic Workflow / Multi-Agent",
            "MCP / Skills / Hooks / Tool Use",
            "Prompt / Context Engineering / 评测闭环",
            "AI Native 应用从原型到交付",
        ],
        self_evaluation="偏 AI Agent 应用工程与研发提效落地，习惯从真实问题出发设计任务拆解、上下文组织、工具调用和结果校验闭环。做过 MCP、Skills、多 Agent 协作、Prompt / Context Engineering 和评测治理，适合 AI 应用开发、Agent 平台与自动化工作流方向岗位。",
    ),
    clone_resume(
        netease.RESUMES,
        "netease-games-ai-application-engineer-resume",
        slug="bilibili-ai-creative-dev-intern-resume",
        alias="刘新宇-哔哩哔哩-AI创作开发实习生",
        title="刘新宇 - 哔哩哔哩 AI创作开发实习生",
        role="AI创作开发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI 应用工程、自动化工作流与多模态内容生产场景做实践，能够把大模型能力落到具体产品链路和创作者工具链中。独立完成 ScholarFlow 与 multi-cloud-email-sender 两条完整系统链路，持续维护多 Agent skills 公共目录，并在 Agent / Tool / Workflow 架构、自动化流程和 AI Coding 提效方面积累了较多证据。与哔哩哔哩这条 AI 创作开发岗位强调的 AI Agent 视频创作系统、内容生产自动化和工具链建设方向很贴合。",
        signals=[
            "AI 应用工程 / Workflow / 自动化工具链",
            "Agent / Tool / Workflow 架构实践",
            "AI Coding / 快速原型 / 产品化落地",
            "复杂业务系统端到端交付",
        ],
        self_evaluation="偏 AI 应用工程与自动化工作流落地，能够把需求拆成可实现、可验证、可持续迭代的系统与工具链能力。做过复杂业务流程建模、AI 能力接入、自动化交付和问题排查，适合 AI 创作工具、AI Native 产品与内容生产效率方向岗位。",
    ),
    clone_resume(
        tencent.RESUMES,
        "tencent-backend-rd-resume",
        slug="bilibili-ai-creative-backend-intern-resume",
        alias="刘新宇-哔哩哔哩-AI创作系统后端实习生-Python-Flask",
        title="刘新宇 - 哔哩哔哩 AI创作系统后端实习生（Python/Flask）",
        role="AI创作系统后端实习生（Python/Flask）",
        summary="华中师范大学计算机技术硕士在读（2027届）。深耕 Python 后端开发、业务系统交付和工程稳定性治理，能够围绕复杂应用完成接口设计、数据模型整理、缓存使用、调试排障和文档沉淀。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整系统链路，具备 FastAPI、Redis、状态流转、接口联调和上线问题定位经验。对哔哩哔哩这条 AI 创作系统后端岗位，最强证据在于 Python Web 开发、服务模块抽象、Redis 基础能力和工程规范意识。",
        signals=[
            "Python 后端 / Web 框架 / 接口开发",
            "Redis / 数据模型 / service-repository 思维",
            "日志排障 / 文档沉淀 / 工程规范",
            "复杂业务系统交付与持续迭代",
        ],
        self_evaluation="偏 Python 后端工程与 AI 应用支撑能力，习惯把复杂需求拆成稳定的接口、数据模型和可维护的服务模块。做过异步任务、日志排障、状态流转、权限与部署交付，适合后端研发、平台服务和 AI 应用支撑方向岗位。",
    ),
]


def main() -> None:
    photo = base.resolve_photo()
    if not base.PANDOC:
        raise RuntimeError("pandoc not found")
    if not base.CHROME:
        raise RuntimeError("google-chrome not found")

    base.COMMON = COMMON

    for data in RESUMES:
        md_path = ROOT / f"{data['slug']}.md"
        html_path = ROOT / f"{data['slug']}-styled.html"
        docx_path = ROOT / f"{data['slug']}.docx"
        pdf_path = ROOT / f"{data['slug']}.pdf"
        alias_docx = ROOT / f"{data['alias']}.docx"
        alias_pdf = ROOT / f"{data['alias']}.pdf"

        md_path.write_text(base.render_markdown(data, photo))
        html_path.write_text(base.render_html(data, photo))

        base.run(["pandoc", str(md_path), "-o", str(docx_path)], ROOT)
        base.run(
            [
                base.CHROME,
                "--headless=new",
                "--disable-gpu",
                "--allow-file-access-from-files",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_path}",
                html_path.resolve().as_uri(),
            ],
            ROOT,
        )

        shutil.copy2(docx_path, alias_docx)
        shutil.copy2(pdf_path, alias_pdf)
        base.publish_public_resume_pdf(EXPORT_DIR, alias_pdf)


if __name__ == "__main__":
    main()
