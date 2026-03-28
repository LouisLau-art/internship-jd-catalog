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
        "slug": "xhs-ai-native-dev-tooling-resume",
        "alias": "刘新宇-小红书-产品工程师-AI应用方向-质效研发",
        "title": "刘新宇 - 小红书 产品工程师（AI应用方向）- 质效研发",
        "role": "产品工程师（AI应用方向）- 质效研发",
        "preserve_projects": True,
        "signals": [
            "AI Native Tooling / Agent Workflow / 质效研发",
            "ScholarFlow + Doubao + skills catalog 主线",
            "Prompt / Context / Fallback / Evaluation",
            "MCP / Context7 / CLI Agent 工具链实践",
        ],
        "summary": "华中师范大学计算机技术硕士在读。长期围绕 AI Native 研发工具链、Agent 工作流和工程交付做实践，能够把复杂需求拆成可执行的 AI 工作流与可上线系统能力。独立交付 ScholarFlow 学术出版系统，实现 AI 驱动的审稿工作流闭环；在 Doubao Batch Translator 项目中，围绕 EPUB / Markdown / HTML / JSON 多格式翻译场景实现 chunk 切分、上下文控制、模型降级、漏译检测与修复闭环，积累了 Prompt / Context Engineering、Fallback、Evaluation 与可观测性相关工程经验；同时维护多 Agent skills 公共 catalog，持续实践 MCP、Context7 与多类 CLI Agent 的能力组织。适合偏 AI Native 工具、Agent 工作流、评测与质效研发方向的岗位。",
        "skills": [
            ("AI Native 与 Agent", "Prompt / Context Engineering、Tool Calling / MCP、Agent Workflow、RAG 风格检索式工作流、Fallback 设计、Evaluation、Observability"),
            ("研发效能与工具", "AI Coding、AI Testing、LLM 工程化落地、自动化工作流、Skill 插件化开发、CLI Agents"),
            ("后端与内容处理", "Python、FastAPI、Asyncio、Next.js 16、REST API、SSE、HTML / EPUB / Markdown / JSON 处理"),
            ("工程化与稳定性", "GitHub Actions、Docker、Sentry、结构化日志、平台日志排查、Validator 修复、Handoff 治理"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立完成 ScholarFlow 学术出版工作流系统开发与上线，通过 Agent 工作流实现 PDF / DOCX / DOC 解析、AI 审稿匹配与复杂业务流转的高效闭环。",
                    "围绕收录 123 个公共 skills 的仓库持续实践 MCP、Context7 与 CLI Agent 能力组织，为多个 Agent 沉淀标准化接入方案和可复用 workflow。",
                    "在实际交付中通过 Context 工程、自定义 Skills、Sentry 与平台日志联合排障，持续优化复杂多步骤任务的生成确定性与研发质效。",
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
                "sub": "AI Native 工具链 / 工程效能",
                "bullets": [
                    "维护 `louislau-art.github.io/multi-agent-skills-catalog/` 与 `github.com/LouisLau-art/multi-agent-skills-catalog`，系统整理多 Agent skills、Context7 文档、安装方案与按场景划分的 profile。",
                    "围绕 skills catalog、MCP 接入、可安装性校验和多端兼容性持续迭代，沉淀出适合 Codex、Claude Code、Gemini 等 CLI Agent 的能力组织方式。",
                    "将公开资料站与开源仓库联动维护，形成可展示、可复用、可持续更新的 AI 工具链作品集。",
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
