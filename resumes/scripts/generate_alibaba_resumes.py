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
        "slug": "alibaba-ai-application-rd-engineer-resume",
        "alias": "刘新宇-阿里巴巴-AI应用研发工程师",
        "title": "刘新宇 - 阿里巴巴 AI应用研发工程师",
        "role": "AI应用研发工程师",
        "preserve_projects": True,
        "signals": [
            "AI coding / Prompt / Context Engineering",
            "ScholarFlow + Doubao + skills catalog 主线",
            "Chunk / Fallback / Evaluation / Observability",
            "MCP / Tool Calling / Agent workflow 工程实践",
        ],
        "summary": "华中师范大学计算机技术硕士在读。长期围绕 AI 应用落地、Agent 工作流和后端交付做工程实践，能够把模糊业务需求转化为可上线系统能力。实习期间独立完成 ScholarFlow 学术出版工作流系统从需求澄清、流程设计、开发联调到上线的完整闭环，也持续推进 multi-cloud-email-sender 的多云发送、追踪链路和运营稳定性建设；在 Doubao Batch Translator 项目中，围绕 EPUB / Markdown / HTML / JSON 多格式翻译场景实现 chunk 切分、上下文控制、模型降级、漏译检测与修复闭环，积累了 Prompt / Context Engineering、Fallback、Evaluation 与可观测性相关工程经验；同时维护多 Agent skills 公共 catalog，为 Codex、Claude Code、Gemini 等 CLI Agent 配置 Context7 MCP，沉淀安装 profile、能力组织与文档接入路径。适合偏 AI coding、Prompt / Context Engineering、Agent 应用交付和工程效能方向的岗位。",
        "skills": [
            ("AI 应用工程", "Prompt / Context Engineering、RAG 风格检索式工作流、Tool Calling / MCP、Agent Workflow、Fallback 设计、Evaluation、Observability"),
            ("LLM 接入与中间件", "Python、FastAPI、Asyncio、OpenAI-Compatible API、SSE、异步任务、限流与重试、模型路由"),
            ("后端与数据", "Java、Spring Boot、MyBatis、REST API、MySQL、Redis、Docker、Linux"),
            ("文档与内容处理", "PDF / DOCX / DOC 解析、HTML / EPUB / Markdown / JSON 处理、结构化提取"),
            ("稳定性与排障", "Sentry、结构化日志、Hugging Face Spaces 日志、Vercel 日志、浏览器 Console、Cloudflare、tracking diagnostics"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立完成 ScholarFlow 学术出版工作流系统开发与上线，面向学术投稿、审稿与出版流程，覆盖 9 类角色、5 条主工作流及财务门禁等关键链路。",
                    "基于 Next.js 16 + FastAPI + Supabase 构建前后端系统，采用 Vercel + Hugging Face Spaces + Docker 3 段式混合部署方案，完成从开发到上线交付的完整闭环。",
                    "与业务方持续对齐投稿、审稿、通知和财务门禁 4 类需求，实现 PDF / DOCX / DOC 解析、审稿流程状态机、Supabase 认证与 RBAC、分析看板等 5 类模块，支撑复杂业务流程落地。",
                    "接入本地 AI 审稿人匹配能力，使用 sentence-transformers + TF-IDF 双路匹配，并结合 Sentry、后端日志、浏览器 Console 与平台日志 4 类信号定位问题，提升交付稳定性。",
                ],
            }
        ],
        "projects": [
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "AI 应用工程 / 全栈交付",
                "bullets": [
                    "面向学术投稿、审稿、修回和出版场景，独立完成从需求澄清、系统设计到开发上线的完整交付，支撑 9 类角色、5 条主工作流和财务门禁，覆盖稿件提交、审稿流转、修回、通知与 AI reviewer recommendation 等核心链路。",
                    "与业务方协同梳理投稿、审稿、通知和财务门禁 4 条业务链路，将 AI reviewer recommendation 融入主流程，保证功能设计、系统实现和业务目标一致。",
                    "实现 PDF / DOCX / DOC 解析与元数据抽取、审稿流程状态机、认证与 RBAC、journal scope、财务关口与分析看板等 6 类关键能力。",
                    "通过前后端 Sentry、结构化异常日志、浏览器 Console 和平台日志 4 类信号联合排查问题，保障上线后的可观测性与稳定性。",
                ],
            },
            {
                "title": "Doubao Batch Translator（批量翻译与模型编排工具）",
                "meta": "2025.12 - 2026.01",
                "sub": "LLM 应用工程 / 中间件",
                "bullets": [
                    "基于 Python 3.13 + asyncio 构建面向 Doubao/ARK 的批量翻译工具，支持 EPUB / Markdown / HTML / JSON 多格式处理，并提供兼容 OpenAI 协议的 HTTP API 供浏览器插件接入。",
                    "围绕长文本翻译质量与上下文窗口限制，在 HTML / EPUB 处理中设计块级合并 + 按句号 / 逗号拆分的 chunk 策略，尽量避免句子、术语和结构被粗暴切断。",
                    "实现每模型 RPM 限速、快慢车道并发和模型降级机制：优先使用垂类翻译模型，遇到 context-length 或额度异常时自动切换普通模型，并在单段失败时回退原文，保证批量任务持续运行。",
                    "构建漏译检测与修复闭环，利用启发式规则扫描 EPUB 正文块、过滤 URL / 邮箱 / 代码等噪声，结合模型调用统计与运行日志定位失败模式，支撑质量评估与后续修补。",
                ],
            },
            {
                "title": "multi-agent-skills-catalog（多 Agent Skills 公开目录）",
                "meta": "持续维护",
                "sub": "Agent 工具链 / 工程效能",
                "bullets": [
                    "维护收录 123 个公共 skills 的 GitHub 仓库，并按 `core + optional profiles` 设计公开安装方案，整理 Context7 与 skills.sh 榜单、热门 docs 和按场景分组的 profile。",
                    "为 Codex、Claude Code、Gemini 等 3 类 CLI Agent 配置 Context7 MCP，沉淀统一接入路径与文档，持续实践 Tool Calling / MCP / Agent workflow 的能力组织方式。",
                    "修复 1 个 `session-handoff` 校验器标题层级兼容问题，补充回归测试并同步到多端技能副本，减少跨 session 切换时的误报和上下文损耗。",
                ],
            },
        ],
    },
    {
        "slug": "alibaba-ai-agent-rd-engineer-resume",
        "alias": "刘新宇-阿里巴巴-AI-Agent应用开发工程师",
        "title": "刘新宇 - 阿里巴巴 AI Agent应用开发工程师",
        "role": "AI Agent应用开发工程师",
        "summary": "华中师范大学计算机技术硕士在读。长期围绕 AI Agent 工作流、MCP 工具链和后端交付做工程实践，能够把模糊业务需求转化为可上线系统能力。实习期间独立完成 ScholarFlow 学术出版工作流系统从需求澄清、流程设计、开发联调到上线的完整闭环，也持续推进 multi-cloud-email-sender 的多云发送、追踪链路和运营稳定性建设；同时维护多 Agent skills 公共 catalog，为 Codex、Claude Code、Gemini 等 CLI Agent 配置 Context7 MCP，沉淀安装 profile、能力组织与文档接入路径 。适合偏 AI Agent 工作流、MCP 生态、大模型应用开发和工程效能方向的岗位。",
        "signals": [
            "Agent workflow / MCP 生态 / CLI Agents",
            "ScholarFlow + multi-cloud 双项目主线",
            "Sentry + 平台日志 + validator / handoff 修复",
            "GitHub 开源 + 个人主页 + skills/docs 收藏站",
        ],
        "skills": [
            ("AI 应用与 Agent", "MCP、Skills、Context7、CLI Agents、Agent Workflow、Prompt / Context Engineering"),
            ("后端与接口", "Python、FastAPI、Java、Spring Boot、MyBatis、REST API、SSE、异步任务"),
            ("工作流与系统设计", "RBAC、状态机、工作流设计、复杂流程拆解、分批调度、Webhook 验签"),
            ("稳定性与排障", "Sentry、Hugging Face Spaces 日志、Vercel 日志、浏览器 Console、Cloudflare"),
            ("文档与工程化", "交接 handoff、validator 修复、GitHub Actions、profile 化安装、技术博客、开源协作"),
            ("数据与部署", "MySQL、Redis、Docker、Linux、Vercel、Hugging Face Spaces、Resend"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立完成 ScholarFlow 学术出版工作流系统开发与上线，面向学术投稿、审稿与出版流程，覆盖 9 类角色、5 条主工作流及财务门禁等关键链路。",
                    "基于 Next.js 16 + FastAPI + Supabase 构建前后端系统，采用 Vercel + Hugging Face Spaces + Docker 3 段式混合部署方案，完成从开发到上线交付的完整闭环。",
                    "围绕收录 123 个公共 skills 的仓库持续实践 Agent 工作流和技能化能力组织，为多个 CLI Agent 沉淀 MCP 接入文档并修复 handoff 校验器问题。",
                    "接入本地 AI 审稿人匹配能力，使用 sentence-transformers + TF-IDF 双路匹配，并结合 Sentry、后端日志、浏览器 Console 与平台日志 4 类信号定位问题，提升交付稳定性。",
                ],
            }
        ],
        "projects": [
            {
                "title": "multi-agent-skills-catalog（多 Agent Skills 公开目录）",
                "meta": "持续维护",
                "sub": "Agent 工具链 / 工程效能",
                "bullets": [
                    "维护收录 123 个公共 skills 的 GitHub 仓库，并按 `core + optional profiles` 设计公开安装方案，整理 Context7 与 skills.sh 榜单、热门 docs 和按场景分组的 profile。",
                    "为 Codex、Claude Code、Gemini 等 3 类 CLI Agent 配置 Context7 MCP，沉淀统一接入路径与文档，持续实践 MCP、Skills、Agent workflow 的能力组织方式。",
                    "修复 1 个 `session-handoff` 校验器标题层级兼容问题，补充回归测试并同步到多端技能副本，减少跨 session 切换时的误报和上下文损耗。",
                ],
            },
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "AI 应用工程 / 全栈交付",
                "bullets": [
                    "面向学术投稿、审稿、修回和出版场景，独立完成从需求澄清、系统设计到开发上线的完整交付，支撑 9 类角色、5 条主工作流和财务门禁，覆盖稿件提交、审稿流转、修回、通知与 AI reviewer recommendation 等核心链路。",
                    "实现 PDF / DOCX / DOC 解析与元数据抽取、审稿流程状态机、认证与 RBAC、journal scope、财务关口与分析看板等 6 类关键能力。",
                    "通过前后端 Sentry、结构化异常日志、浏览器 Console 和平台日志 4 类信号联合排查问题，保障上线后的可观测性与稳定性。",
                ],
            },
            {
                "title": "multi-cloud-email-sender（内部邮件运营系统）",
                "meta": "2026.02 - 2026.03",
                "sub": "AI 辅助运营工具 / 工程交付",
                "bullets": [
                    "负责内部邮件运营系统端到端实现，基于 FastAPI + React 打通联系人导入、模板变量替换、分批调度、发送看板与追踪链路 5 个核心环节，统一接入阿里云 DirectMail 与腾讯云 SES。",
                    "面向非技术同事处理脏 CSV、多编码、多分隔符等真实运营数据问题，支持最大 30 万行联系人导入、任务草稿恢复与发送进度跟踪。",
                    "主导打开率与点击率 Tracking 的公网可用性建设，围绕固定追踪域名、Cloudflare 接管、`track_domain` 配置、启动校验与 tracking diagnostics 5 个关键环节完善链路稳定性。",
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
