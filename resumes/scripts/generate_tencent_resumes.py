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
        "slug": "tencent-ai-app-dev-resume",
        "alias": "刘新宇-腾讯-AI应用开发",
        "title": "刘新宇 - 腾讯 AI应用开发",
        "role": "AI应用开发",
        "summary": "华中师范大学计算机技术硕士在读。专注于 AI 应用落地与 Agent 工作流交付。独立完成 ScholarFlow 学术出版工作流系统，实现从需求澄清、流程设计到三段式混合部署的完整闭环。维护 123 个公共 skills 目录，深度实践 MCP、Context7 与多类 CLI Agent 的能力集成。擅长将业务逻辑抽象为 Agent 指令集，并解决 LLM 落地过程中的上下文管理难题。适合腾讯各 BG 偏 AI 应用开发与工程落地的岗位。",
        "signals": [
            "AI 应用交付 / Agent 工作流 / RAG 实践",
            "ScholarFlow AI 工作流闭环交付",
            "multi-agent-skills-catalog 核心贡献者",
            "MCP / Context 工程 / CLI Agent 深度实践",
        ],
        "skills": [
            ("AI 应用与 Agent", "MCP、Skills、Context7、CLI Agents、Agent Workflow、Prompt/Context Engineering、RAG"),
            ("后端与全栈交付", "Python、FastAPI、Next.js 16、REST API、SSE、异步任务处理、Java基础"),
            ("工程化与提效", "GitHub Actions、Docker、Linux、交接 handoff、validator 修复、profile 化安装"),
            ("稳定性与排障", "Sentry、浏览器 Console、平台日志排查、tracking diagnostics、状态机稳定性"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "在 ScholarFlow 系统开发中深度实践 AI 应用交付模式，通过 Agent 工作流实现 PDF 解析与 AI 审稿匹配的高效闭环。",
                    "主导 multi-cloud-email-sender 内部运营系统，解决 30 万量级运营数据的处理与发送，并通过自定义 diagnostics 工具保障追踪链路稳定性。",
                    "维护 123 个公共 skills 仓库，持续探索 MCP 在提升研发与业务质效方面的应用，为多个 CLI Agent 沉淀标准化接入方案。",
                ],
            }
        ],
        "projects": [
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "AI 应用工程 / 流程自动化",
                "bullets": [
                    "将 AI reviewer recommendation 融入学术投稿主流程，实现 PDF/DOCX 元数据提取与审稿人精准匹配，保障了业务目标的高效达成。",
                    "基于 Supabase 构建 RBAC 权限体系，结合三段式部署方案，确保了面向 9 类角色的复杂业务系统在生产环境的高可用。",
                ],
            },
        ],
    },
    {
        "slug": "tencent-backend-rd-resume",
        "alias": "刘新宇-腾讯-软件开发-后台开发方向",
        "title": "刘新宇 - 腾讯 软件开发-后台开发方向",
        "role": "软件开发-后台开发方向",
        "summary": "华中师范大学计算机技术硕士在读。深耕后端架构交付、工程稳定性与研发效能工具。长期围绕 AI Agent 工作流与 MCP 生态做实践，能够把模糊业务需求转化为可上线的系统能力。独立完成 ScholarFlow 学术出版系统的全栈交付，并持续推进 multi-cloud-email-sender 的稳定性建设。擅长利用 Sentry、日志分析和诊断工具进行线上排障。适合腾讯 TEG/CSIG 等部门偏后台开发、基建工具与可观测性方向的岗位。",
        "signals": [
            "后端架构 / 工程稳定性 / 研发效能",
            "ScholarFlow + multi-cloud 双项目主线",
            "MCP 生态 / CLI Agent 工具链实践",
            "Sentry + 平台日志 + 自动化排障工具",
        ],
        "skills": [
            ("后端与架构", "Java、Spring Boot、MyBatis、Python、FastAPI、REST API、SSE、异步任务、RBAC"),
            ("基建与稳定性", "Sentry、Docker、Linux、Cloudflare、tracking diagnostics、Validator、Handoff 治理"),
            ("数据与部署", "MySQL、Redis、Vercel、Hugging Face Spaces、Supabase"),
            ("AI 工程化", "MCP、Skills、Context7、CLI Agents、Agent Workflow、Prompt Engineering"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立交付 ScholarFlow 系统，实现从需求梳理到三段式混合部署的闭环，通过状态机设计保障了 5 条主工作流的严谨性。",
                    "在邮件运营系统中主导 Tracking 链路稳定性建设，开发 tracking diagnostics 工具，显著降低了线上故障的定位成本。",
                    "围绕收录 123 个公共 skills 的仓库持续实践 Agent 工作流，沉淀 MCP 接入文档并修复 handoff 校验器的逻辑漏洞。",
                ],
            }
        ],
        "projects": [
            {
                "title": "multi-cloud-email-sender（内部邮件运营系统）",
                "meta": "2026.02 - 2026.03",
                "sub": "服务端研发 / 稳定性建设",
                "bullets": [
                    "负责系统端到端实现，打通联系人导入、分批调度与追踪链路，支持最大 30 万行真实运营数据的高可靠处理。",
                    "主导打开率与点击率 Tracking 的公网可用性建设，围绕固定域名与 Cloudflare 接管完善链路，减少了 80% 的人工排障成本。",
                ],
            },
        ],
    },
    {
        "slug": "tencent-finance-ai-app-resume",
        "alias": "刘新宇-腾讯-财经线培训生-AI应用开发",
        "title": "刘新宇 - 腾讯 财经线培训生-AI应用开发",
        "role": "财经线培训生-AI应用开发",
        "summary": "华中师范大学计算机技术硕士在读。具备极强的自驱力与全栈交付能力，擅长将业务需求快速转化为 AI 驱动的自动化工具。独立完成 ScholarFlow 系统，通过 AI 审稿匹配与流程自动化提升了出版效率。持续维护多 Agent skills 目录，探索 AI 在提升组织效能方面的边界。具备处理复杂运营数据与保障系统线上稳定性的实战经验。目标是在财经与职能场景中，利用 AI 技术打造高效、可靠的生产力工具。",
        "signals": [
            "全栈交付 / 业务提效 / AI 应用创新",
            "ScholarFlow 业务系统闭环交付",
            "multi-cloud 复杂数据处理实践",
            "技术博客 / 文档沉淀 / 快速学习者",
        ],
        "skills": [
            ("AI 提效与 Agent", "MCP、Skills、Context7、Agent Workflow、Prompt Engineering、RAG、业务逻辑抽象"),
            ("后端与全栈", "Python、FastAPI、Next.js 16、Java基础、REST API、SSE、异步处理"),
            ("数据处理", "脏数据清洗、多编码处理、MySQL、Redis、Supabase"),
            ("工程化与稳定性", "GitHub Actions、Docker、Sentry、文档交接 handoff、自动化诊断"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立交付 ScholarFlow 系统，针对学术场景实现了从需求到上线的三段式混合部署闭环，体现了极强的端到端负责意愿。",
                    "负责 multi-cloud-email-sender 内部运营系统，解决非技术同事面对的脏数据与大规模发送难题，并沉淀了完整的运维文档。",
                    "持续实践 AI Coding 工作流，通过 Context 工程极大提升了需求拆解与代码生成的准确率，具备将 AI 转化为实际产出的能力。",
                ],
            }
        ],
        "projects": [
            {
                "title": "multi-agent-skills-catalog（多 Agent Skills 公开目录）",
                "meta": "持续维护",
                "sub": "效能工具 / 能力组织",
                "bullets": [
                    "整理发布 123 个公共技能，为业务团队提供标准化的 AI 能力接入路径，展现了良好的产品思维与协作精神。",
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
