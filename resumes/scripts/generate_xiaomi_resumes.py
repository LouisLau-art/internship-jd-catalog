#!/usr/bin/env python3
from __future__ import annotations

import html
import os
import shutil
import subprocess
from pathlib import Path

from resume_profile import build_common_profile, normalize_projects


ROOT = Path(os.environ["RESUME_ROOT"]).expanduser() if os.environ.get("RESUME_ROOT") else Path(__file__).resolve().parent
PHOTO = Path(os.environ["RESUME_PHOTO"]).expanduser() if os.environ.get("RESUME_PHOTO") else ROOT / "louis-profile-photo.png"
CHROME = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
PANDOC = shutil.which("pandoc")


CSS = """
      @page {
        size: Letter;
        margin: 12mm 13mm 12mm 13mm;
      }

      :root {
        --ink: #162233;
        --muted: #556273;
        --line: #d9e0e8;
        --panel: #f5f8fb;
        --accent: #0f4c81;
        --accent-soft: #dbe9f6;
        --chip: #eef4fa;
      }

      * { box-sizing: border-box; }

      body {
        margin: 0;
        color: var(--ink);
        background: #ffffff;
        font-family: "Source Han Sans SC", "Noto Sans CJK SC", "IBM Plex Sans", "PingFang SC", "Microsoft YaHei", sans-serif;
        font-size: 9.6pt;
        line-height: 1.34;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }

      .resume { width: 100%; }
      .hero {
        border: 1px solid var(--line);
        border-top: 5px solid var(--accent);
        background: linear-gradient(135deg, rgba(15, 76, 129, 0.06), rgba(15, 76, 129, 0.015)), #ffffff;
        padding: 10px 12px 8px;
        border-radius: 10px;
      }
      .hero-top {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 14px;
      }
      .hero-aside {
        display: flex;
        align-items: flex-start;
        gap: 10px;
      }
      .name {
        margin: 0;
        font-size: 22.5pt;
        line-height: 1;
        font-weight: 800;
        letter-spacing: 0.5px;
      }
      .role {
        display: inline-block;
        margin-top: 6px;
        padding: 3px 9px;
        border-radius: 999px;
        background: var(--accent-soft);
        color: var(--accent);
        font-size: 9pt;
        font-weight: 700;
      }
      .contact {
        min-width: 240px;
        text-align: right;
        font-size: 8.9pt;
        color: var(--muted);
      }
      .contact div + div { margin-top: 2px; }
      .photo-frame {
        width: 84px;
        height: 98px;
        padding: 3px;
        border-radius: 12px;
        background: #ffffff;
        border: 1px solid var(--line);
        box-shadow: 0 8px 20px rgba(22, 34, 51, 0.08);
        flex: 0 0 auto;
      }
      .photo-frame img {
        width: 100%;
        height: 100%;
        display: block;
        object-fit: cover;
        border-radius: 8px;
      }
      .hero-summary {
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid var(--line);
        color: #27384b;
      }
      .signal-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 8px;
      }
      .signal {
        padding: 4px 8px;
        border-radius: 999px;
        background: var(--chip);
        color: var(--accent);
        font-size: 8.4pt;
        font-weight: 700;
      }
      .section { margin-top: 10px; }
      .section-title {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 0 0 6px;
        font-size: 10pt;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: var(--accent);
      }
      .section-title::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, var(--accent), transparent);
      }
      .skills-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px 12px;
      }
      .skill-card,
      .entry,
      .edu-card,
      .opensource-list {
        padding: 7px 9px;
        border: 1px solid var(--line);
        border-radius: 10px;
        background: #fff;
        break-inside: avoid;
      }
      .skill-label {
        display: block;
        margin-bottom: 3px;
        color: var(--accent);
        font-size: 8.9pt;
        font-weight: 800;
      }
      .entry + .entry { margin-top: 8px; }
      .entry-head {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: baseline;
        margin-bottom: 4px;
      }
      .entry-title {
        margin: 0;
        font-size: 10.2pt;
        font-weight: 800;
      }
      .entry-meta {
        color: var(--muted);
        font-size: 8.7pt;
        white-space: nowrap;
      }
      .entry-sub {
        margin: -1px 0 4px;
        color: var(--muted);
        font-size: 8.8pt;
      }
      ul {
        margin: 4px 0 0 15px;
        padding: 0;
      }
      li + li { margin-top: 2px; }
      .edu-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
      }
      .edu-school {
        font-size: 10pt;
        font-weight: 800;
      }
      .edu-meta {
        margin-top: 2px;
        color: var(--muted);
        font-size: 8.8pt;
      }
      .footer-note {
        margin-top: 6px;
        color: var(--muted);
        font-size: 8.3pt;
      }
      @media print {
        .section, .entry, .edu-card, .skills-grid, .opensource-list { break-inside: avoid; }
      }
"""


COMMON = build_common_profile()


RESUMES = [
    {
        "slug": "mi-server-side-rd-intern-resume",
        "alias": "刘新宇-小米-服务端研发实习生-武汉",
        "title": "刘新宇 - 小米服务端研发实习生（武汉）",
        "role": "服务端研发实习生—武汉",
        "summary": "华中师范大学计算机技术硕士在读，长期在武汉，可长期实习。具备 Java / Spring Boot / MyBatis、Python / FastAPI / Asyncio、MySQL、Redis、Docker、Linux 基础，能够完成从需求理解、功能开发到部署交付的完整闭环。实习期间独立完成 ScholarFlow 学术出版工作流系统并上线，也持续推进 multi-cloud-email-sender 的多云发送、追踪链路和外部服务稳定性建设。能够与产品、算法、前端协作推进需求落地，并结合 Sentry、平台日志与浏览器 Console 快速定位线上问题。",
        "signals": [
            "Java / Python / MySQL / Redis",
            "ScholarFlow + multi-cloud 双项目主线",
            "并发 / 异步 / 日志排障",
            "AI 辅助编码与工程交付",
        ],
        "skills": [
            ("后端核心", "Java、Python、Spring Boot、MyBatis、FastAPI、REST API、面向对象"),
            ("数据与缓存", "MySQL、Redis、索引、事务、缓存治理、批量导入、分批调度"),
            ("并发与异步", "Asyncio、SSE、异步任务、限流治理、外部服务调用链路"),
            ("稳定性与排障", "Sentry、Hugging Face Spaces 日志、Vercel 日志、浏览器 Console、Cloudflare"),
            ("交付与环境", "Docker、Linux、Git、Vercel、Hugging Face Spaces、Resend、Webhook 验签"),
            ("加分项", "AI 辅助编码工具、GitHub 开源、个人技术博客、跨角色协作"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立完成 ScholarFlow 学术出版工作流系统开发与上线，面向学术投稿、审稿与出版流程，支撑 9 类角色、5 条主工作流及财务门禁等核心链路。",
                    "基于 Next.js 16 + FastAPI + Supabase 构建前后端系统，采用 Vercel + Hugging Face Spaces + Docker 的混合部署方案，完成从开发到上线交付的完整闭环。",
                    "围绕实际业务流程与需求提出方持续沟通，抽象投稿、审稿、通知、财务门禁等核心链路，推动系统能力从需求讨论落地到线上发布。",
                    "实现投稿 PDF / DOCX / DOC 解析、审稿流程状态机、认证与 RBAC、财务关口与分析看板，并结合前后端 Sentry、平台日志和浏览器 Console 定位问题。",
                ],
            }
        ],
        "projects": [
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "后端 / 全栈开发 / 独立交付",
                "bullets": [
                    "面向学术投稿、审稿、修回和出版场景，独立完成从需求澄清、系统设计到开发上线的完整交付，支撑复杂的角色权限和流程流转。",
                    "实现 PDF / DOCX / DOC 解析与元数据抽取、审稿流程状态机、认证与 RBAC、journal scope、财务关口与分析看板等关键能力。",
                    "集成本地 AI reviewer recommendation，使用 sentence-transformers 与 TF-IDF 支撑智能匹配，并通过 Sentry、后端异常日志和浏览器 Console 提高问题定位效率。",
                ],
            },
            {
                "title": "multi-cloud-email-sender（内部邮件运营系统）",
                "meta": "2026.02 - 2026.03",
                "sub": "后端服务 / 工程交付",
                "bullets": [
                    "基于 FastAPI + React 打通联系人导入、模板变量替换、分批调度、发送看板与追踪链路，统一接入阿里云 DirectMail 与腾讯云 SES 双通道发信。",
                    "处理脏 CSV、多编码、多分隔符等真实运营数据问题，支持最大 30 万行联系人导入、任务草稿恢复与发送进度跟踪。",
                    "围绕固定追踪域名、Cloudflare 接管、`track_domain` 配置、启动校验与 tracking diagnostics 完善外部服务调用链路和公网追踪链路稳定性。",
                ],
            },
        ],
        "opensource": [
            "VueUse：修复 useMagicKeys 中键盘事件 key 为 undefined 时的边界情况问题，PR #5225 已合并。",
            "Naive UI：为 DatePicker 组件添加 date slot 与 prefix slot 支持，PR #7382 / #7379。",
        ],
    },
    {
        "slug": "mi-intl-site-backend-ai-translation-intern-resume",
        "alias": "刘新宇-小米-后端研发工程师实习生-国际站AI翻译",
        "title": "刘新宇 - 小米后端研发工程师实习生（AI 翻译与校对）",
        "role": "后端研发工程师实习生（AI 翻译与校对）",
        "summary": "华中师范大学计算机技术硕士在读，长期在武汉，可长期实习。具备 Java / Spring Boot / MyBatis、Python / FastAPI / Asyncio、MySQL、Redis 基础，做过兼容 OpenAI 标准协议的翻译中间件，也完成过 ScholarFlow 学术出版工作流系统和 multi-cloud-email-sender 的后端与全栈交付。适合 AI 翻译、AI 校对、AI 应用接口层和后端服务结合的岗位，能够把模型接口、异步调度、链路排障和工程落地结合起来。",
        "signals": [
            "AI 翻译 / OpenAI-Compatible API",
            "Doubao Translator + ScholarFlow",
            "Asyncio / 限流 / 异步调度",
            "Sentry + Cloudflare + 线上排障",
        ],
        "skills": [
            ("后端与接口", "Java、Python、Spring Boot、MyBatis、FastAPI、REST API、OpenAI-Compatible API"),
            ("异步与调度", "Asyncio、SSE、限流治理、任务分发、模型接口适配"),
            ("数据与缓存", "MySQL、Redis、索引、事务、缓存治理、读写分离"),
            ("稳定性与排障", "Sentry、Hugging Face Spaces 日志、Vercel 日志、Cloudflare、Resend、Webhook 验签"),
            ("工程交付", "Docker、Linux、Git、Vercel、Hugging Face Spaces、部署上线"),
            ("加分项", "GitHub 开源、个人技术博客、AI 辅助编码工具"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立完成 ScholarFlow 学术出版工作流系统开发与上线，面向学术投稿、审稿与出版流程，支撑 9 类角色、5 条主工作流及财务门禁等关键链路。",
                    "基于 Next.js 16 + FastAPI + Supabase 构建前后端系统，采用 Vercel + Hugging Face Spaces + Docker 的混合部署方案，完成从开发到上线交付的完整闭环。",
                    "实现投稿 PDF / DOCX / DOC 解析、审稿流程状态机、认证与 RBAC、财务关口与分析看板，并结合前后端 Sentry 与平台日志定位问题。",
                    "持续推进多云发送、追踪链路和外部服务稳定性建设，处理真实线上集成问题。",
                ],
            }
        ],
        "projects": [
            {
                "title": "Doubao Batch Translator（高并发异步翻译中间件）",
                "meta": "2025.12 - 2026.01",
                "sub": "AI 翻译 / 后端接口层",
                "bullets": [
                    "基于 Python 3.13 + Asyncio 构建兼容 OpenAI 标准协议的高并发翻译中间件，对接浏览器插件并承接真实翻译请求链路。",
                    "设计“一核多壳”插件化架构和“快慢双车道”动态路由策略，免费模型严格限制 80 RPM，高性能模型自动解锁 500+ 并发，CPU 利用率提升 300%。",
                    "围绕模型调用、限流调度、文件递归处理和断点续传构建稳定的 AI 翻译后端能力。",
                ],
            },
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "后端 / 全栈开发 / 独立交付",
                "bullets": [
                    "独立完成学术投稿、审稿、修回和出版流程系统的需求澄清、系统设计、开发联调与上线交付，支撑复杂业务状态与角色权限控制。",
                    "实现 PDF / DOCX / DOC 解析与元数据抽取、审稿流程状态机、Supabase 认证与 RBAC、journal scope、财务关口与分析看板等关键模块。",
                    "集成本地 AI reviewer recommendation，使用 sentence-transformers 与 TF-IDF 支撑智能匹配，并通过 Sentry、后端异常日志和浏览器 Console 提高问题定位效率。",
                ],
            },
            {
                "title": "multi-cloud-email-sender（内部邮件运营系统）",
                "meta": "2026.02 - 2026.03",
                "sub": "后端服务 / 工程交付",
                "bullets": [
                    "基于 FastAPI + React 打通联系人导入、模板变量替换、分批调度、发送看板与追踪链路，统一接入阿里云 DirectMail 与腾讯云 SES 双通道发信。",
                    "围绕固定追踪域名、Cloudflare 接管、`track_domain` 配置、启动校验与 Resend 域名配置完善外部服务调用链路和公网追踪链路稳定性。",
                    "处理脏 CSV、多编码、多分隔符等真实运营数据问题，支持最大 30 万行联系人导入与发送进度跟踪。",
                ],
            },
        ],
    },
    {
        "slug": "mi-cloud-platform-software-rd-intern-resume",
        "alias": "刘新宇-小米-软件研发工程师实习生-云平台基础服务",
        "title": "刘新宇 - 小米软件研发工程师实习生（云平台基础服务）",
        "role": "软件研发工程师实习生（云平台基础服务）",
        "summary": "华中师范大学计算机技术硕士在读，长期在武汉，可长期实习。具备 Java / Python、Linux、Docker、Git 基础，能够完成从需求分析、后端开发到部署上线和问题排查的完整闭环。实习期间独立完成 ScholarFlow 学术出版工作流系统开发与上线，也持续推进 multi-cloud-email-sender 的多云发送、追踪链路和交付稳定性建设。对基础服务、性能优化、持续交付效率和工具化能力有持续实践，适合偏云平台与基础服务的软件研发岗位。",
        "signals": [
            "云平台基础服务 / 持续交付",
            "ScholarFlow 上线与排障",
            "Cloudflare / Docker / Linux",
            "工具链与工程效率实践",
        ],
        "skills": [
            ("开发与环境", "Java、Python、Linux、Docker、Git、REST API"),
            ("交付与部署", "Vercel、Hugging Face Spaces、Cloudflare、Resend、Webhook 验签"),
            ("性能与稳定性", "Sentry、日志排障、Asyncio、SSE、链路可用性、启动预检"),
            ("数据与缓存", "MySQL、Redis、索引、事务、缓存治理、分批调度"),
            ("工具化与效率", "GitHub、Context7、MCP、Skills、文档沉淀、交接材料"),
            ("加分项", "开源贡献、个人技术博客、AI 辅助编码工具"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立完成 ScholarFlow 学术出版工作流系统开发与上线，基于 Next.js 16 + FastAPI + Supabase 构建前后端系统，采用 Vercel + Hugging Face Spaces + Docker 的混合部署方案。",
                    "实现投稿解析、审稿流程状态机、认证与 RBAC、财务关口与分析看板等关键模块，支撑复杂业务链路上线。",
                    "在开发过程中使用前后端 Sentry，并结合 Hugging Face Spaces 日志、Vercel 日志与浏览器 Console 进行问题定位和修复。",
                    "持续推进多云发送、追踪链路和外部服务稳定性建设，沉淀交接文档与工具化经验。",
                ],
            }
        ],
        "projects": [
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "全栈开发 / 独立交付",
                "bullets": [
                    "独立完成从需求澄清、系统设计到开发上线的完整交付，支撑 9 类角色、5 条主工作流及财务门禁。",
                    "采用 Vercel + Hugging Face Spaces + Docker 的混合部署方案，并通过 Cloudflare 反向代理改善中国大陆访问链路。",
                    "通过前后端 Sentry、平台日志和浏览器 Console 联合定位报错，保障上线后的可观测性与稳定性。",
                ],
            },
            {
                "title": "multi-cloud-email-sender（内部邮件运营系统）",
                "meta": "2026.02 - 2026.03",
                "sub": "后端服务 / 工程交付",
                "bullets": [
                    "基于 FastAPI + React 打通联系人导入、模板变量替换、分批调度、发送看板与追踪链路，统一接入阿里云 DirectMail 与腾讯云 SES 双通道发信。",
                    "围绕固定追踪域名、Cloudflare 接管、`track_domain` 配置、启动校验与 tracking diagnostics 完善链路稳定性与交付可靠性。",
                    "沉淀面向普通同事、技术同事和后续接手方的文档与交接材料，推动系统从“可用工具”演进为“可维护、可交接”的内部基础设施。",
                ],
            },
            {
                "title": "Skills 仓库治理与 Agent 工作流优化",
                "meta": "持续维护",
                "sub": "工具链 / 工程效率实践",
                "bullets": [
                    "维护收录 123 个公共 skills 的 GitHub 仓库，并为 Codex、Claude Code、Gemini 等 CLI Agent 配置 Context7 MCP。",
                    "参考 SkillsBench 思路治理本地与公共技能集，清理高重叠和高噪音 skill，优化任务匹配与上下文负担，并修复 session-handoff validator 的标题层级兼容问题。",
                ],
            },
        ],
    },
    {
        "slug": "mi-productivity-tools-rd-intern-resume",
        "alias": "刘新宇-小米-效能工具研发工程师实习生",
        "title": "刘新宇 - 小米效能工具研发工程师实习生",
        "role": "效能工具研发工程师实习生",
        "summary": "华中师范大学计算机技术硕士在读，长期在武汉，可长期实习。具备 React / Next.js、Java / Python、Linux、Git 基础，能够围绕工程工具、文档体系和开发工作流完成从需求理解、功能实现到交付落地的闭环。持续维护多 Agent skills 公开 catalog，为 Codex、Claude Code、Gemini 等 CLI Agent 配置 Context7 MCP，并沉淀安装 profile、接入文档与校验工具修复经验；同时在 ScholarFlow 和 multi-cloud-email-sender 中完成前后端联调、日志排障和交接材料整理，适合偏工具平台与研发效能方向的岗位。",
        "signals": [
            "效能工具 / Agent 工作流",
            "React + Python + Git + Linux",
            "Context7 MCP / Skills Catalog",
            "文档沉淀 / 交接 / 校验修复",
        ],
        "skills": [
            ("前端与交互", "React、Next.js、TypeScript、HTML、CSS、基础组件开发、页面联调"),
            ("后端与脚本", "Python、Java、FastAPI、Spring Boot、CLI 工具、自动化脚本"),
            ("流程与工具链", "Git、GitHub、Context7、MCP、Skills、Agent 工作流、文档沉淀"),
            ("调试与稳定性", "Sentry、浏览器 Console、Hugging Face Spaces 日志、Vercel 日志、校验器修复"),
            ("协作与交付", "需求澄清、技术文档、交接 handoff、问题复盘、跨角色协作"),
            ("加分项", "个人技术博客、GitHub 开源、AI 辅助编码工具"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立完成 ScholarFlow 学术出版工作流系统开发与上线，覆盖前后端功能实现、需求澄清、问题定位和交付发布，支撑复杂业务流程落地。",
                    "与需求提出方持续沟通并抽象业务流程，配合产品思路澄清、流程图整理和功能拆分，把模糊需求逐步转成可执行任务。",
                    "在开发过程中使用前后端 Sentry，并结合 Hugging Face Spaces 日志、Vercel 日志和浏览器 Console 快速定位问题，保障迭代效率。",
                    "持续补充项目文档、交接 handoff 和操作说明，提升后续接手、排障和协作效率。",
                ],
            }
        ],
        "projects": [
            {
                "title": "multi-agent-skills-catalog（多 Agent Skills 公开目录）",
                "meta": "持续维护",
                "sub": "工具平台 / 工程效率实践",
                "bullets": [
                    "维护收录 123 个公共 skills 的 GitHub 仓库，设计 `core + optional profiles` 的公开安装方案，并整理 Xiaomi / 小红书 JD 目录与简历源文件工作流。",
                    "为 Codex、Claude Code、Gemini 等 CLI Agent 配置 Context7 MCP，沉淀接入文档、公开 profile 和多客户端统一使用路径。",
                    "修复 `session-handoff` 校验器的标题层级兼容问题，补充回归测试并同步到多端技能副本，减少 handoff 文档误报和跨 session 切换成本。",
                ],
            },
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "全栈开发 / 工具化交付",
                "bullets": [
                    "独立完成从需求澄清、系统设计到开发上线的完整交付，支撑 9 类角色、5 条主工作流及财务门禁。",
                    "基于 Next.js 16 + FastAPI + Supabase 完成前后端联调和复杂流程界面实现，并用 Mermaid 图、结构化文档和 AI 辅助方式梳理需求。",
                    "通过前后端 Sentry、平台日志和浏览器 Console 联合定位报错，提高迭代与排障效率。",
                ],
            },
            {
                "title": "multi-cloud-email-sender（内部邮件运营系统）",
                "meta": "2026.02 - 2026.03",
                "sub": "工具系统 / 文档与交接",
                "bullets": [
                    "基于 FastAPI + React 打通联系人导入、模板变量替换、分批调度、发送看板与追踪链路，面向非技术同事提供可直接使用的内部工具。",
                    "围绕 `track_domain`、Cloudflare 接管、启动预检和 tracking diagnostics 完善操作说明、交接文档和问题排查路径，使系统更易维护和接手。",
                ],
            },
        ],
    },
    {
        "slug": "mi-data-understanding-rd-intern-resume",
        "alias": "刘新宇-小米-数据理解研发工程师实习生",
        "title": "刘新宇 - 小米数据理解研发工程师实习生",
        "role": "数据理解研发工程师实习生",
        "summary": "华中师范大学计算机技术硕士在读，长期在武汉，可长期实习。具备 Python / Java、Linux、MySQL 基础，做过真实业务场景下的数据清洗、文件解析、结构化提取和问题定位工作。实习期间在 ScholarFlow 中实现 PDF / DOCX / DOC 解析与元数据抽取，在 multi-cloud-email-sender 中处理脏 CSV、多编码、多分隔符等数据问题并支撑大规模联系人导入。对数据质量、问题定位、流程优化和用大模型辅助处理复杂信息有持续实践，适合偏数据理解与数据处理流程建设的岗位。",
        "signals": [
            "Python / Java / Linux",
            "数据清洗 / 文件解析 / 结构化提取",
            "30 万行联系人导入链路",
            "问题定位 / 流程优化 / LLM 辅助",
        ],
        "skills": [
            ("数据处理", "Python、Java、CSV 清洗、编码识别、分隔符兼容、结构化抽取、批处理"),
            ("文件与内容理解", "PDF / DOCX / DOC 解析、元数据抽取、文档结构整理、规则校验"),
            ("数据与环境", "MySQL、基础 SQL、Linux、日志定位、脚本化处理"),
            ("问题分析", "异常数据排查、字段标准化、流程校验、错误复现与定位"),
            ("AI 辅助处理", "大模型辅助信息整理、需求结构化、文档摘要与流程梳理"),
            ("加分项", "GitHub 开源、个人技术博客、AI 辅助编码工具"),
        ],
        "experience": [
            {
                "title": "遇见科技（武汉）有限公司 · 全栈开发",
                "meta": "2026.01 - 2026.03",
                "sub": "",
                "bullets": [
                    "独立完成 ScholarFlow 学术出版工作流系统开发与上线，实现 PDF / DOCX / DOC 解析、元数据抽取与投稿信息结构化处理。",
                    "将录音转写、文档整理、流程图绘制等需求理解过程结构化，并借助 AI 把模糊业务信息转化为可执行的系统流程和数据字段。",
                    "在 multi-cloud-email-sender 中处理脏 CSV、多编码、多分隔符等真实数据问题，完善联系人导入、字段兼容和发送链路稳定性。",
                    "结合平台日志、浏览器 Console 与业务现象进行问题分析，持续优化数据处理流程与错误定位效率。",
                ],
            }
        ],
        "projects": [
            {
                "title": "multi-cloud-email-sender（内部邮件运营系统）",
                "meta": "2026.02 - 2026.03",
                "sub": "数据清洗 / 结构化处理",
                "bullets": [
                    "处理脏 CSV、多编码、多分隔符等真实运营数据问题，支持最大 30 万行联系人导入、任务草稿恢复与发送进度跟踪。",
                    "围绕联系人字段、模板变量、发送状态和追踪事件设计数据处理链路，提升联系人导入和后续发送的稳定性与可解释性。",
                    "通过固定追踪域名、Cloudflare 接管和 tracking diagnostics 提升打开/点击事件的可追踪性，为后续数据分析提供稳定输入。",
                ],
            },
            {
                "title": "ScholarFlow（学术出版工作流系统）",
                "meta": "2026.01 - 2026.03",
                "sub": "内容解析 / 数据结构化",
                "bullets": [
                    "实现 PDF / DOCX / DOC 解析与元数据抽取，将学术投稿文件中的标题、作者和附属信息转化为结构化数据供后续流程使用。",
                    "围绕投稿、审稿、修回、通知和财务门禁梳理状态流转与字段约束，推动复杂业务流程数据化和可校验化。",
                    "结合 sentence-transformers 与 TF-IDF 支撑 AI reviewer recommendation，把文本相似度计算应用到真实业务场景。",
                ],
            },
            {
                "title": "ScholarFlow 需求整理与 AI 辅助结构化流程",
                "meta": "2026.01",
                "sub": "复杂信息整理 / 流程优化",
                "bullets": [
                    "将长时业务沟通录音转写为文本，并用 AI 整理需求、生成 Mermaid 流程图和状态图，帮助识别需求遗漏与流程冲突。",
                    "后续进一步把需求澄清前移为独立环节，使用 CLI Agent + Brainstorm 方式辅助需求方补全细节，减少因表述不清导致的返工。",
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


def render_html(data: dict) -> str:
    normalized_projects = normalize_projects(data["projects"])
    skills = "\n".join(
        f"""          <div class="skill-card">
            <span class="skill-label">{html.escape(label)}</span>
            {html.escape(value)}
          </div>"""
        for label, value in data["skills"]
    )
    experience = "\n".join(render_entry(e) for e in data["experience"])
    projects = "\n".join(render_entry(e) for e in normalized_projects)
    education = "\n".join(
        f"""          <div class="edu-card">
            <div class="edu-school">{html.escape(e['school'])}</div>
            <div class="edu-meta">{html.escape(e['meta'])}</div>
            {f'<div class="footer-note">{html.escape(e["note"])}</div>' if e.get('note') else ''}
          </div>"""
        for e in COMMON["education"]
    )
    works = "；".join(f"{label}：{value}" for label, value in COMMON["works"])
    language = "\n".join(
        f"""          <div class="edu-card">
            <div class="edu-school">{html.escape(item)}</div>
          </div>"""
        for item in COMMON["language"]
    )
    open_source = render_list(data.get("opensource", COMMON["opensource"]))
    signals = "\n".join(f'          <div class="signal">{html.escape(s)}</div>' for s in data["signals"])

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
      <section class="hero">
        <div class="hero-top">
          <div>
            <h1 class="name">{COMMON['name']}</h1>
            <div class="role">{html.escape(data['role'])}</div>
          </div>
          <div class="hero-aside">
            <div class="contact">
              <div>{COMMON['contact_line']}</div>
              <div>{COMMON['phone_email']}</div>
              <div>GitHub: {COMMON['github']}</div>
              <div>Homepage: {COMMON['homepage']}</div>
            </div>
            <div class="photo-frame">
              <img src="{PHOTO.resolve().as_uri()}" alt="刘新宇证件照" />
            </div>
          </div>
        </div>
        <div class="hero-summary">{html.escape(data['summary'])}</div>
        <div class="signal-row">
{signals}
        </div>
      </section>

      <section class="section">
        <h2 class="section-title">自我评价</h2>
        <div class="skill-card">{html.escape(COMMON['self_evaluation'])}</div>
      </section>

      <section class="section">
        <h2 class="section-title">作品展示</h2>
        <div class="skill-card">{html.escape(works)}</div>
      </section>

      <section class="section">
        <h2 class="section-title">核心技能</h2>
        <div class="skills-grid">
{skills}
        </div>
      </section>

      <section class="section">
        <h2 class="section-title">实习经历</h2>
{experience}
      </section>

      <section class="section">
        <h2 class="section-title">重点项目</h2>
{projects}
      </section>

      <section class="section">
        <h2 class="section-title">教育经历</h2>
        <div class="edu-grid">
{education}
        </div>
      </section>

      <section class="section">
        <h2 class="section-title">语言能力</h2>
        <div class="edu-grid">
{language}
        </div>
      </section>

      <section class="section">
        <h2 class="section-title">开源贡献</h2>
        <div class="opensource-list">
          <ul>
{open_source}
          </ul>
        </div>
      </section>
    </main>
  </body>
</html>
"""


def render_markdown(data: dict) -> str:
    normalized_projects = normalize_projects(data["projects"])
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

![]({PHOTO.resolve()}){{ width=1.0in }}

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

## 重点项目
{render_entries(normalized_projects)}

## 教育经历
{education_md}

## 语言能力
{language_md}

## 开源贡献
{open_source_md}
"""


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    if not PHOTO.exists():
        raise FileNotFoundError(PHOTO)
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

        md_path.write_text(render_markdown(data))
        html_path.write_text(render_html(data))

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
