#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path

import generate_xhs_resumes as base
from resume_profile import build_common_profile


ROOT = Path(__file__).resolve().parent
EXPORT_DIR = Path(__file__).resolve().parent.parent / "sources"


COMMON = build_common_profile()


RESUMES = [
    {
        "slug": "netease-games-agent-engineer-resume",
        "alias": "刘新宇-网易互娱-Agent工程师",
        "title": "刘新宇 - 网易互娱 Agent工程师",
        "role": "Agent工程师",
        "summary": "华中师范大学计算机技术硕士在读（2027届）。专注于 AI Agent 工作流交付、RAG 能力构建与研发流程自动化。维护 123 个公共 skills 目录，深度实践 MCP 与多类 CLI Agent 的能力集成与上下文治理。独立交付 ScholarFlow 系统，实现 AI 驱动的流程自动化。擅长将复杂业务（如游戏研发、内容生产）抽象为智能体协作流，具备快速构建 Agent 原型并验证技术可行性的实战经验。目标是用 AI 重新定义游戏开发范式。",
        "signals": [
            "Agent Workflow / RAG / 流程自动化",
            "multi-agent-skills-catalog 核心维护者",
            "ScholarFlow AI 驱动闭环交付",
            "MCP / Context 工程 / CLI Agent 深度实践",
        ],
        "skills": [
            ("AI Agent & Workflow", "MCP、Skills、Context7、CLI Agents、Multi-Agent 协作、自主规划、工具调用"),
            ("RAG & 知识库", "sentence-transformers、TF-IDF、结构化元数据提取、业务上下文注入、向量库实践"),
            ("后端与全栈", "Python、FastAPI、Next.js 16、Java基础、REST API、SSE、异步任务处理"),
            ("工程化与提效", "GitHub Actions、Docker、Sentry、自动化诊断、Validator 修复、Handoff 治理"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "在 ScholarFlow 系统中深度实践 AI 驱动的工作流模式，将学术出版流程拆解为 Agent 指令集，实现 PDF 解析与 AI 匹配的自动化闭环。",
                    "维护 123 个公共 skills 仓库，探索 Agent 在复杂工程场景下的能力边界，为多种 AI 助手沉淀了标准化的能力接入与上下文管理方案。",
                    "主导 multi-cloud-email-sender 项目，解决大规模数据处理中的稳定性难题，展现了极强的工程落地与问题解决能力。",
                ],
            }
        ],
        "projects": [
            {
                "title": "multi-agent-skills-catalog（多 Agent Skills 公开目录）",
                "meta": "持续维护",
                "sub": "AI 研发效能 / Agent 协作",
                "bullets": [
                    "整理并发布 123 个公共 skills，设计 `core + optional` 架构，致力于构建标准化的 AI 插件生态，提升 Multi-Agent 协作效率。",
                    "主导“上下文治理”实践，通过修复校验器漏洞保障了跨 AI 会话的信息完整性，极大地提升了 Agent 在长程任务中的表现。",
                ],
            },
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "AI 应用交付 / 流程建模",
                "bullets": [
                    "独立交付一整套针对学术场景的 AI 工作流，成功将 LLM 融入传统审稿流程，实现了从需求澄清到三段式部署的完整闭环。",
                    "结合业务上下文构建了精准的匹配机制，并建立了一套完整的 AI 调用监控体系，确保了系统在实际交付中的稳定性。",
                ],
            },
        ],
    },
    {
        "slug": "netease-games-ai-application-engineer-resume",
        "alias": "刘新宇-网易游戏-AI应用工程师",
        "title": "刘新宇 - 网易游戏 AI应用工程师",
        "role": "AI应用工程师",
        "summary": "华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI 应用工程、Agent 工作流和后端系统交付做实战，能够把大模型能力转成可上线、可验证、可维护的产品能力。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 公共目录，为 Codex、Claude Code、Gemini 等 CLI Agent 配置 Context7 MCP。适合偏 AI 应用全栈开发、Agent 套件、模型测评与模型路由、AI Native 研发效能方向的岗位。",
        "signals": [
            "AI 应用工程 / Agent Workflow / MCP",
            "ScholarFlow + multi-cloud 双项目闭环",
            "Prompt Engineering / RAG / Function Calling",
            "Linux / Docker / 日志排障 / 稳定性交付",
        ],
        "skills": [
            ("AI 应用与 Agent", "MCP、Skills、Context7、CLI Agents、Prompt Engineering、RAG、Function Calling、Agent Workflow"),
            ("后端与服务架构", "Python、FastAPI、Java基础、REST API、SSE、异步任务、高并发接口与服务编排"),
            ("全栈与产品交付", "Next.js 16、React、Supabase、AI Native 交互设计、复杂业务流程落地"),
            ("平台与基础设施", "模型路由思维、模型测评闭环、日志诊断、Cloudflare、Docker、Linux"),
            ("工程化与协作", "GitHub Actions、handoff 治理、validator 修复、技术博客、开源协作"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立完成 ScholarFlow 学术出版工作流系统开发与上线，面向复杂业务流程完成需求澄清、系统设计、前后端联调与部署交付，支撑 9 类角色、5 条主工作流。",
                    "基于 Next.js 16 + FastAPI + Supabase 构建 AI 应用系统，将文档解析、Reviewer Recommendation、权限与状态机整合进统一产品流程，形成可用的 AI Native 业务体验。",
                    "围绕收录 123 个公共 skills 的仓库持续实践 Agent 工作流和能力组织，为多个 CLI Agent 沉淀 MCP 接入路径、profile 方案和上下文治理经验。",
                    "在真实线上环境中结合 Sentry、平台日志、浏览器 Console 与后端异常日志定位问题，持续优化服务稳定性、链路观测性和交付效率。",
                ],
            }
        ],
        "projects": [
            {
                "title": "multi-agent-skills-catalog（多 Agent Skills 公开目录）",
                "meta": "持续维护",
                "sub": "Agent 套件 / 研发效能 / 能力组织",
                "bullets": [
                    "维护收录 123 个公共 skills 的 GitHub 仓库，并按 `core + optional profiles` 设计公开安装方案，整理 Context7 与 skills.sh 榜单、热门 docs 和按场景分组的 profile。",
                    "为 Codex、Claude Code、Gemini 等 3 类 CLI Agent 配置 Context7 MCP，持续实践 Agent 套件化、能力组织、模型上下文接入与 AI Native 研发流程。",
                    "修复 `session-handoff` 校验器标题层级兼容问题并补充回归测试，减少跨 session 切换时的误报与上下文损耗。",
                ],
            },
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "AI 应用全栈开发 / 复杂流程交付",
                "bullets": [
                    "面向学术投稿、审稿、修回和出版场景，独立完成从需求澄清、系统设计到开发上线的完整交付，覆盖稿件提交、审稿流转、修回、通知与 AI reviewer recommendation 等核心链路。",
                    "实现 PDF / DOCX / DOC 解析与元数据抽取、审稿流程状态机、认证与 RBAC、journal scope、财务关口与分析看板等关键能力，把 AI 能力嵌入主业务流程。",
                    "通过前后端 Sentry、结构化异常日志、浏览器 Console 和平台日志联合排查问题，保障 AI 应用在云端环境中的稳定运行。",
                ],
            },
            {
                "title": "multi-cloud-email-sender（内部邮件运营系统）",
                "meta": "2026.02 - 2026.03",
                "sub": "AI 辅助运营工具 / 服务架构与稳定性",
                "bullets": [
                    "负责内部邮件运营系统端到端实现，基于 FastAPI + React 打通联系人导入、模板变量替换、分批调度、发送看板与追踪链路 5 个核心环节。",
                    "统一接入阿里云 DirectMail 与腾讯云 SES，支持大批量联系人导入、任务草稿恢复与发送进度跟踪，具备高并发任务编排与后端服务交付经验。",
                    "围绕固定追踪域名、Cloudflare 接管、`track_domain` 配置、启动校验与 tracking diagnostics 完善链路稳定性，降低人工排障成本。",
                ],
            },
        ],
    },
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
