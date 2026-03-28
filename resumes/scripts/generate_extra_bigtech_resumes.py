#!/usr/bin/env python3
from __future__ import annotations

import copy
import shutil
from pathlib import Path

import generate_alibaba_resumes as alibaba
import generate_netease_resumes as netease
import generate_tencent_resumes as tencent
import generate_xhs_resumes as base


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
        slug="netease-youdao-ai-app-dev-intern-resume",
        alias="刘新宇-网易有道-AI应用开发实习生",
        title="刘新宇 - 网易有道 AI应用开发实习生",
        role="AI应用开发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI Agent、LLM 应用开发和全栈工程交付做实战，能够把需求澄清、工作流设计、工具调用和后端服务串成可上线的 AI Native 产品。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 公共目录并为 Codex、Claude Code、Gemini 等 CLI Agent 配置 Context7 MCP。与网易有道这条 JD 的 AI Agent 产品设计、Agent Workflow、RAG / Function Calling、多智能体和 AI Coding 工具使用要求高度匹配。",
        signals=[
            "AI Agent 产品开发 / Workflow / MCP",
            "Prompt Engineering / RAG / Function Calling",
            "ScholarFlow + multi-cloud 双项目闭环",
            "Full-stack 交付 + AI Coding 工具深度使用",
        ],
    ),
    clone_resume(
        alibaba.RESUMES,
        "alibaba-ai-agent-rd-engineer-resume",
        slug="xiaomi-ai-agent-dev-intern-resume",
        alias="刘新宇-小米-AI Agent开发实习生",
        title="刘新宇 - 小米 AI Agent开发实习生",
        role="AI Agent开发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI Agent 工作流、代码检索、工具调用和工程自动化做实践，能够把模糊需求转化为可运行、可验证、可持续优化的 AI 编码系统。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，维护多 Agent skills 公共 catalog，并持续实践多 Agent 协作、上下文治理和评测闭环。与小米这条 AI Agent 开发 JD 中的 AI 编码 Agent、多 Agent 协作、代码语义检索、自动化评测与生成代码质量验证方向强匹配。",
        signals=[
            "AI Coding Agent / Multi-Agent 协作",
            "代码检索 / 工具调用 / 评测闭环",
            "MCP / Skills / CLI Agent 深度实践",
            "工程自动化 + 真实业务系统交付",
        ],
    ),
    clone_resume(
        alibaba.RESUMES,
        "alibaba-ai-agent-rd-engineer-resume",
        slug="xiaomi-llm-agent-engineer-intern-resume",
        alias="刘新宇-小米-大模型Agent开发工程师实习生",
        title="刘新宇 - 小米 大模型Agent开发工程师实习生",
        role="大模型Agent开发工程师实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。长期围绕 AI Agent 平台、MCP 协议、RAG、工具调用和工程化交付做实践，能够把复杂任务拆解、工作流编排、上下文接入和服务部署整合成可落地的智能体系统。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条完整业务链路，持续维护多 Agent skills 公共 catalog，并为 Codex、Claude Code、Gemini 等 CLI Agent 配置 Context7 MCP。与小米这条 Miloco / 家庭智能 Agent JD 里的 MCP、A2A、RAG、LangChain、Docker、微服务和 Agent 平台化方向高度匹配。",
        signals=[
            "MCP / A2A / RAG / Agent 平台化",
            "Miloco 类家庭智能 Agent 高匹配",
            "LangChain / Workflow / Tool Use 实践",
            "Docker / 微服务 / CLI Agent 工程落地",
        ],
    ),
    clone_resume(
        tencent.RESUMES,
        "tencent-backend-rd-resume",
        slug="pdd-server-side-rd-intern-resume",
        alias="刘新宇-拼多多-服务端研发实习生",
        title="刘新宇 - 拼多多 服务端研发实习生",
        role="服务端研发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。深耕后端系统交付、工程稳定性和数据链路治理，能够把需求分析、接口开发、批量任务处理和线上排障整合成可上线的后端能力。独立完成 ScholarFlow 学术出版系统与 multi-cloud-email-sender 的端到端交付，具备真实数据导入、任务调度、接口联调和日志诊断经验。对拼多多技术专场里的服务端研发岗位是更稳的主投选择，匹配点在于后端开发、数据处理、稳定性建设和高效率执行。",
        signals=[
            "后端开发 / 数据处理 / 接口联调",
            "ScholarFlow + multi-cloud 双项目主线",
            "MySQL / Redis / 异步任务 / 日志排障",
            "工程稳定性 + 高执行力",
        ],
    ),
    clone_resume(
        tencent.RESUMES,
        "tencent-backend-rd-resume",
        slug="didi-ride-platform-backend-intern-resume",
        alias="刘新宇-滴滴-网约车平台公司-后端研发实习生",
        title="刘新宇 - 滴滴 网约车平台公司后端研发实习生",
        role="网约车平台公司-后端研发实习生",
        summary="华中师范大学计算机技术硕士在读（2027届）。深耕后端交付、接口对接、问题排查和技术文档沉淀，能够围绕业务平台完成功能开发、现有模块维护和异常问题定位。独立交付 ScholarFlow 与 multi-cloud-email-sender 两条核心系统链路，具备 MySQL、Python / Java、接口联调、缺陷修复和交付文档维护经验。与滴滴这条网约车平台后端研发岗的功能开发、内部系统接口对接、用户问题排查和文档协作要求更贴合，也比滴滴当前若干自动驾驶 C++ 岗更适合你优先投递。",
        signals=[
            "后端功能开发 / 内部系统接口对接",
            "MySQL / Python / Java / Debug 工具",
            "问题定位 / 缺陷修复 / 文档沉淀",
            "业务系统交付 + 线上稳定性经验",
        ],
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
