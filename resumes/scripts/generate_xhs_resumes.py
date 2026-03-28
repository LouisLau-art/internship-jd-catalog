#!/usr/bin/env python3
from __future__ import annotations

import html
import os
import shutil
import subprocess
from pathlib import Path

from resume_profile import build_common_profile, normalize_projects


ROOT = Path(os.environ["RESUME_ROOT"]).expanduser() if os.environ.get("RESUME_ROOT") else Path(__file__).resolve().parent
PHOTO_CANDIDATES = [
    Path(os.environ["RESUME_PHOTO"]).expanduser() if os.environ.get("RESUME_PHOTO") else None,
    ROOT / "louis-profile-photo.png",
    Path("/home/louis/Downloads/resume-refresh-20260319/louis-profile-photo.png"),
    Path("/home/louis/Downloads/Image_1755245899996.png"),
]
CHROME = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
PANDOC = shutil.which("pandoc")


CSS = """
      @page {
        size: A4;
        margin: 9mm 10mm;
      }

      :root {
        --ink: #1f2a36;
        --muted: #6b7482;
        --line: #e9e7ea;
        --accent: #e15271;
        --accent-soft: #fff2f5;
        --sidebar: #fcf7f8;
      }

      * { box-sizing: border-box; }

      body {
        margin: 0;
        color: var(--ink);
        background: #ffffff;
        font-family: "Source Han Sans SC", "Noto Sans CJK SC", "IBM Plex Sans", "PingFang SC", "Microsoft YaHei", sans-serif;
        font-size: 9.2pt;
        line-height: 1.33;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }

      .page {
        break-after: page;
      }
      .page:last-child {
        break-after: auto;
      }

      .page-one {
        display: grid;
        grid-template-columns: 212px 1fr;
        gap: 16px;
        align-items: start;
      }

      .sidebar {
        background: var(--sidebar);
        border: 1px solid #f3dde3;
        border-radius: 18px;
        padding: 14px 12px;
      }

      .sidebar-top {
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .name {
        margin: 0;
        font-size: 24pt;
        line-height: 1;
        font-weight: 800;
        letter-spacing: 0.2px;
      }

      .role {
        display: inline-block;
        margin-top: 6px;
        color: var(--accent);
        font-size: 9.4pt;
        font-weight: 800;
      }

      .photo-frame {
        width: 94px;
        height: 112px;
        padding: 3px;
        border-radius: 14px;
        background: #ffffff;
        border: 1px solid #e8d5db;
      }

      .photo-frame img {
        width: 100%;
        height: 100%;
        display: block;
        object-fit: cover;
        border-radius: 10px;
      }

      .sidebar-title {
        margin: 12px 0 6px;
        color: var(--accent);
        font-size: 10pt;
        font-weight: 800;
      }

      .contact-line,
      .sidebar-note,
      .skill-value,
      .work-item {
        color: #485262;
        font-size: 8.7pt;
      }

      .contact-line + .contact-line,
      .work-item + .work-item {
        margin-top: 3px;
      }

      .skill-group + .skill-group {
        margin-top: 8px;
      }

      .skill-label {
        display: block;
        color: #304154;
        font-size: 8.8pt;
        font-weight: 800;
        margin-bottom: 2px;
      }

      .edu-block + .edu-block {
        margin-top: 9px;
      }

      .edu-school {
        font-size: 9.2pt;
        font-weight: 800;
      }

      .edu-meta,
      .footer-note {
        color: var(--muted);
        font-size: 8.4pt;
      }

      .main-pane {
        min-width: 0;
      }

      .section {
        margin-bottom: 12px;
      }

      .section-title {
        margin: 0 0 6px;
        color: var(--accent);
        font-size: 10.3pt;
        font-weight: 800;
        padding-left: 8px;
        border-left: 3px solid var(--accent);
      }

      .summary {
        color: #2d3947;
      }

      .signal-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px 10px;
        margin-top: 7px;
      }

      .signal {
        color: #3f5870;
        font-size: 8.5pt;
        font-weight: 700;
      }

      .entry,
      .panel {
        padding: 9px 10px;
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #ffffff;
        break-inside: avoid;
      }

      .entry + .entry {
        margin-top: 8px;
      }

      .entry-head {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        align-items: baseline;
        margin-bottom: 3px;
      }

      .entry-title {
        margin: 0;
        font-size: 10.1pt;
        font-weight: 800;
      }

      .entry-meta {
        color: var(--muted);
        font-size: 8.5pt;
        white-space: nowrap;
      }

      .entry-sub {
        margin: 0 0 4px;
        color: var(--muted);
        font-size: 8.5pt;
      }

      ul {
        margin: 4px 0 0 14px;
        padding: 0;
      }

      li + li {
        margin-top: 2px;
      }

      .page-two {
        padding-top: 2px;
      }

      .split-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
      }

      .opensource-list {
        padding: 8px 10px;
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #fff;
      }

      @media print {
        .entry, .panel, .opensource-list { break-inside: avoid; }
      }
"""


COMMON = build_common_profile()


RESUMES = [
    {
        "slug": "xhs-ecology-rd-intern-resume",
        "alias": "刘新宇-小红书-生态研发工程师实习生",
        "title": "刘新宇 - 小红书生态研发工程师实习生",
        "role": "生态研发实习生（后端）",
        "summary": "华中师范大学计算机技术硕士在读，长期在武汉，可长期实习。具备 Java / Spring Boot / MyBatis 等后端开发能力，也能用 Python / FastAPI / Asyncio 支撑 AI 应用接口层和内部工具交付。实习期间独立完成 ScholarFlow 学术出版工作流系统从需求澄清、流程设计、开发联调到上线的完整闭环，并持续负责 multi-cloud-email-sender 的多云发送、追踪链路和运营稳定性建设。能够与业务、产品和技术同学协作推进需求定义，把模糊诉求沉淀成可上线系统能力，关注系统设计、稳定性建设和自动化校验。",
        "signals": [
            "需求澄清到上线交付闭环",
            "multi-cloud 追踪链路与 Cloudflare 接管",
            "Sentry + 平台日志 + 启动预检",
        ],
        "opensource": [
            "VueUse：修复 useMagicKeys 中键盘事件 key 为 undefined 时的边界情况问题，PR #5225 已合并。",
            "Naive UI：为 DatePicker 组件添加 date slot 与 prefix slot 支持，PR #7382 / #7379。",
        ],
        "skills": [
            ("后端与语言", "Java、Spring Boot、MyBatis、Python、FastAPI、JavaScript、面向对象"),
            ("系统设计与交付", "REST API、RBAC、状态机、工作流设计、需求拆解、Docker、Linux、部署上线"),
            ("数据与性能", "MySQL、Redis、索引、事务、缓存治理、批量导入、分批调度"),
            ("AI 与业务接口", "OpenAI-Compatible API、Asyncio、SSE、sentence-transformers、TF-IDF、本地 AI 推荐"),
            ("稳定性与协作", "Sentry、Hugging Face Spaces 日志、Vercel 日志、Cloudflare、Resend、Webhook 验签、启动预检、tracking diagnostics"),
            ("加分项", "GitHub 开源、个人技术博客、开源协作、需求澄清、跨角色协作"),
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
                "sub": "全栈开发 / 独立交付",
                "bullets": [
                    "面向学术投稿、审稿、修回和出版场景，独立完成从需求澄清、系统设计到开发上线的完整交付，支撑 9 类角色、5 条主工作流和财务门禁，覆盖稿件提交、审稿流转、修回、通知与 AI reviewer recommendation 等核心链路。",
                    "与业务方协同梳理投稿、审稿、通知和财务门禁 4 条业务链路，将 AI reviewer recommendation 融入主流程，保证功能设计、系统实现和业务目标一致。",
                    "实现 PDF / DOCX / DOC 解析与元数据抽取、审稿流程状态机、认证与 RBAC、journal scope、财务关口与分析看板等 6 类关键能力，支撑复杂业务状态与角色权限控制。",
                    "通过前后端 Sentry、结构化异常日志、浏览器 Console 和平台日志 4 类信号联合排查问题，保障上线后的可观测性与稳定性。",
                ],
            },
            {
                "title": "multi-cloud-email-sender（内部邮件运营系统）",
                "meta": "2026.02 - 2026.03",
                "sub": "全栈开发 / 工程交付",
                "bullets": [
                    "负责内部邮件运营系统端到端实现，基于 FastAPI + React 打通联系人导入、模板变量替换、分批调度、发送看板与追踪链路 5 个核心环节，统一接入阿里云 DirectMail 与腾讯云 SES。",
                    "面向非技术同事处理脏 CSV、多编码、多分隔符等真实运营数据问题，支持最大 30 万行联系人导入、任务草稿恢复与发送进度跟踪。",
                    "主导打开率与点击率 Tracking 的公网可用性建设，围绕固定追踪域名、Cloudflare 接管、`track_domain` 配置、启动校验与 tracking diagnostics 5 个关键环节完善链路稳定性，并减少人工排障成本。",
                    "面向普通同事、技术同事和后续接手方 3 类对象沉淀文档与交接材料，推动系统从“可用工具”演进为“可维护、可交接”的内部基础设施。",
                ],
            },
            {
                "title": "Doubao Batch Translator（高并发异步翻译中间件）",
                "meta": "2025.12 - 2026.01",
                "sub": "",
                "bullets": [
                    "基于 Python 3.13 + Asyncio 构建高性能中间件，解决大规模文本处理中的 API 限流与资源调度问题。",
                    "设计“快慢双车道”动态路由策略，免费模型严格限制 80 RPM，高性能模型自动解锁 500+ 并发，CPU 利用率提升 300%。",
                ],
            },
        ],
    },
    {
        "slug": "xhs-java-backend-ai-agent-intern-resume",
        "alias": "刘新宇-小红书-Java后端AI Agent实习生",
        "title": "刘新宇 - 小红书 Java 后端 AI Agent 实习生",
        "role": "Java 后端开发实习生（AI Agent 方向）",
        "summary": "华中师范大学计算机技术硕士在读，长期在武汉，可长期实习。具备 Java / Spring Boot / MyBatis、MySQL、Redis 基础，并完成过基于 Spring Boot 的 O2O 餐饮系统等后端实践。实习期间独立完成 ScholarFlow 学术出版工作流系统开发与上线，也持续推进多云发送、追踪链路和外部服务稳定性建设。同时围绕 Multi Agent、MCP、Skills 和公开 skills catalog 做持续工程实践，能够把后端基础、AI 接口层、外部服务调度与智能体工作流理解结合起来。",
        "signals": [
            "Java / Spring Boot / MyBatis 基础",
            "ScholarFlow + multi-cloud 双项目主线",
            "Multi Agent / MCP / Skills 持续实践",
            "Sentry + Cloudflare + Tracking 链路",
        ],
        "skills": [
            ("Java 后端核心", "Java、Spring Boot、MyBatis、面向对象、REST API、接口开发"),
            ("数据与缓存", "MySQL、Redis、索引、事务、缓存治理、读写分离"),
            ("AI Agent 工程实践", "Multi Agent、MCP、Skills、Context7、OpenAI-Compatible API、Asyncio、SSE、能力组织"),
            ("后端交付与稳定性", "Docker、Linux、Sentry、日志排障、Webhook 验签、Cloudflare、Resend、启动预检"),
            ("系统设计与协作", "RBAC、状态机、工作流设计、分批调度、Tracking 链路"),
            ("加分项", "GitHub 开源、个人技术博客、Agent 工作流治理"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立完成 ScholarFlow 学术出版工作流系统开发与上线，面向学术投稿、审稿与出版流程，支撑 9 类角色、5 条主工作流及财务门禁等关键链路。",
                    "基于 Next.js 16 + FastAPI + Supabase 构建前后端系统，采用 Vercel + Hugging Face Spaces + Docker 3 段式混合部署方案，完成从开发到上线交付的完整闭环。",
                    "实现投稿 PDF / DOCX / DOC 解析、审稿流程状态机、认证与 RBAC、财务关口与分析看板等 5 类模块，并结合前后端 Sentry 与平台日志定位问题。",
                    "围绕 Multi Agent、MCP、Skills 3 类能力组织方式进行持续工程实践，沉淀可复用的工作流经验、技能库治理方法与上下文压缩思路。",
                ],
            }
        ],
        "projects": [
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "全栈开发 / 独立交付",
                "bullets": [
                    "独立完成学术投稿、审稿、修回和出版流程系统的需求澄清、系统设计、开发联调与上线交付，支撑 9 类角色、5 条主工作流和财务门禁，覆盖稿件提交、审稿流转、修回、通知与 AI reviewer recommendation 等核心链路。",
                    "实现 PDF / DOCX / DOC 解析与元数据抽取、审稿流程状态机、Supabase 认证与 RBAC、journal scope、财务关口与分析看板等 6 类关键模块。",
                    "集成本地 AI reviewer recommendation，使用 sentence-transformers + TF-IDF 双路匹配，并通过 Sentry、后端异常日志和浏览器 Console 3 类信号提高问题定位效率。",
                ],
            },
            {
                "title": "multi-cloud-email-sender（内部邮件运营系统）",
                "meta": "2026.02 - 2026.03",
                "sub": "后端服务 / 工程交付",
                "bullets": [
                    "基于 FastAPI + React 打通联系人导入、模板变量替换、分批调度、发送看板与追踪链路 5 个核心环节，统一接入阿里云 DirectMail 与腾讯云 SES 双通道发信。",
                    "围绕固定追踪域名、Cloudflare 接管、`track_domain` 配置、启动校验与 Resend 域名配置等 5 个关键环节完善外部服务调用链路和公网追踪链路稳定性。",
                    "处理脏 CSV、多编码、多分隔符等真实运营数据问题，支持最大 30 万行联系人导入与发送进度跟踪。",
                ],
            },
            {
                "title": "Skills 仓库治理与 Agent 工作流优化",
                "meta": "持续维护",
                "sub": "Multi Agent / MCP / Skills 实践",
                "bullets": [
                    "维护收录 123 个公共 skills 的 GitHub 仓库，并为 Codex、Claude Code、Gemini 等 3 类 CLI Agent 配置 Context7 MCP，持续实践 Multi Agent、MCP 与 Skills 的能力组织方式。",
                    "参考 SkillsBench 思路治理本地与公共技能集，清理高重叠和高噪音 skill，并修复 1 个 session-handoff validator 标题层级兼容缺陷，优化任务匹配与上下文负担。",
                ],
            },
        ],
    },
]


def render_list(items: list[str]) -> str:
    return "\n".join(f"            <li>{html.escape(item)}</li>" for item in items)


def render_entry(entry: dict) -> str:
    sub = f'\n          <div class="entry-sub">{html.escape(entry["sub"])}</div>' if entry.get("sub") else ""
    return f"""
        <article class="entry">
          <div class="entry-head">
            <h3 class="entry-title">{html.escape(entry['title'])}</h3>
            <div class="entry-meta">{html.escape(entry['meta'])}</div>
          </div>{sub}
          <ul>
{render_list(entry['bullets'])}
          </ul>
        </article>"""


def render_html(data: dict, photo: Path) -> str:
    # Some tailored resumes intentionally preserve a hand-curated project order.
    projects = data["projects"] if data.get("preserve_projects") else normalize_projects(data["projects"])
    sidebar_skills = "\n".join(
        f"""          <div class="skill-group">
            <span class="skill-label">{html.escape(label)}</span>
            <div class="skill-value">{html.escape(value)}</div>
          </div>"""
        for label, value in data["skills"]
    )
    experience = "\n".join(render_entry(e) for e in data["experience"])
    featured_project = render_entry(projects[0])
    remaining_projects = "\n".join(render_entry(e) for e in projects[1:])
    education = "\n".join(
        f"""          <div class="edu-block">
            <div class="edu-school">{html.escape(e['school'])}</div>
            <div class="edu-meta">{html.escape(e['meta'])}</div>
            {f'<div class="footer-note">{html.escape(e["note"])}</div>' if e.get('note') else ''}
          </div>"""
        for e in COMMON["education"]
    )
    works = "\n".join(
        f"""          <div class="work-item">{html.escape(label)}：{html.escape(value)}</div>"""
        for label, value in COMMON["works"]
    )
    language = "\n".join(
        f"""          <div class="edu-block">
            <div class="edu-school">{html.escape(item)}</div>
          </div>"""
        for item in COMMON["language"]
    )
    open_source = render_list(data.get("opensource", COMMON["opensource"]))
    signals = "\n".join(f'            <div class="signal">{html.escape(s)}</div>' for s in data["signals"])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(data['title'])}</title>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <main class="resume">
      <section class="page page-one">
        <aside class="sidebar">
          <div class="sidebar-top">
            <div>
              <h1 class="name">{COMMON['name']}</h1>
              <div class="role">{html.escape(data['role'])}</div>
            </div>
            <div class="photo-frame">
              <img src="{photo.resolve().as_uri()}" alt="刘新宇证件照" />
            </div>
          </div>
          <div class="sidebar-title">联系方式</div>
          <div class="contact-line">{COMMON['contact_line']}</div>
          <div class="contact-line">{COMMON['phone_email']}</div>
          <div class="contact-line">GitHub: {COMMON['github']}</div>
          <div class="contact-line">Homepage: {COMMON['homepage']}</div>

          <div class="sidebar-title">作品链接</div>
{works}

          <div class="sidebar-title">技能栈</div>
{sidebar_skills}

        </aside>

        <div class="main-pane">
          <section class="section">
            <h2 class="section-title">个人简介</h2>
            <div class="summary">{html.escape(data['summary'])}</div>
            <div class="signal-row">
{signals}
            </div>
          </section>

          <section class="section">
            <h2 class="section-title">自我评价</h2>
            <div class="panel">{html.escape(COMMON['self_evaluation'])}</div>
          </section>

          <section class="section">
            <h2 class="section-title">实习经历</h2>
{experience}
          </section>

          <section class="section">
            <h2 class="section-title">教育经历</h2>
            <div class="panel">
{education}
            </div>
          </section>

          <section class="section">
            <h2 class="section-title">语言能力</h2>
            <div class="panel">
{language}
            </div>
          </section>

          <section class="section">
            <h2 class="section-title">重点项目</h2>
{featured_project}
          </section>
        </div>
      </section>

      <section class="page page-two">
        <section class="section">
          <h2 class="section-title">重点项目</h2>
{remaining_projects}
        </section>

        <section class="section">
          <h2 class="section-title">开源贡献</h2>
          <div class="opensource-list">
            <ul>
{open_source}
            </ul>
          </div>
        </section>
      </section>
    </main>
  </body>
</html>
"""


def render_markdown(data: dict, photo: Path) -> str:
    projects = data["projects"] if data.get("preserve_projects") else normalize_projects(data["projects"])
    skills_md = "\n".join(f"- {label}：{value}" for label, value in data["skills"])
    works_md = "\n".join(f"- {label}：{value}" for label, value in COMMON["works"])

    def render_entries(entries: list[dict]) -> str:
        blocks = []
        for e in entries:
            head = f"**{e['title']}** | {e['sub']} | {e['meta']}" if e.get("sub") else f"**{e['title']}** | {e['meta']}"
            bullets = "\n".join(f"- {b}" for b in e["bullets"])
            blocks.append(f"{head}\n{bullets}")
        return "\n\n".join(blocks)

    open_source_md = "\n".join(f"- {item}" for item in data.get("opensource", COMMON["opensource"]))
    education_md = "\n\n".join(
        f"**{e['school']}** | {e['meta']}\n{e['note']}".strip()
        for e in COMMON["education"]
    )
    language_md = "\n".join(f"- {item}" for item in COMMON["language"])

    return f"""# {COMMON['name']}

![]({photo.resolve()}){{ width=1.0in }}

{COMMON['contact_line']} | 17362707076 | 1397951685@qq.com  
GitHub: {COMMON['github']} | Homepage: {COMMON['homepage']}  
求职方向：{data['role']}

## 个人简介
{data['summary']}

## 自我评价
{COMMON['self_evaluation']}

## 作品展示
{works_md}

## 核心技能
{skills_md}

## 实习经历
{render_entries(data['experience'])}

## 教育经历
{education_md}

## 语言能力
{language_md}

## 重点项目
{render_entries(projects)}

## 开源贡献
{open_source_md}
"""


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def resolve_photo() -> Path:
    for candidate in PHOTO_CANDIDATES:
        if candidate and candidate.exists():
            return candidate
    checked = ", ".join(str(p) for p in PHOTO_CANDIDATES if p)
    raise FileNotFoundError(f"resume photo not found; checked: {checked}")


def publish_public_resume_pdf(export_dir: Path, alias_pdf: Path) -> None:
    export_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(alias_pdf, export_dir / alias_pdf.name)


def main() -> None:
    photo = resolve_photo()
    if not PANDOC:
        raise RuntimeError("pandoc not found")
    if not CHROME:
        raise RuntimeError("google-chrome not found")

    for data in RESUMES:
        md_path = ROOT / f"{data['slug']}.md"
        html_path = ROOT / f"{data['slug']}-styled.html"
        docx_path = ROOT / f"{data['slug']}.docx"
        pdf_path = ROOT / f"{data['slug']}.pdf"
        alias_docx = ROOT / f"{data['alias']}.docx"
        alias_pdf = ROOT / f"{data['alias']}.pdf"

        md_path.write_text(render_markdown(data, photo))
        html_path.write_text(render_html(data, photo))

        run(["pandoc", str(md_path), "-o", str(docx_path)], ROOT)
        run(
            [
                CHROME,
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


if __name__ == "__main__":
    main()
