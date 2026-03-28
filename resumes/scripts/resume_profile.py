from __future__ import annotations

from copy import deepcopy


COMMON_PROFILE = {
    "name": "刘新宇",
    "location": "武汉",
    "contact_line": "武汉 · 华中师范大学人工智能教育学部计算机技术硕士在读（2027届）",
    "phone_email": "17362707076 · 1397951685@qq.com",
    "github": "github.com/LouisLau-art",
    "homepage": "louislau-art.github.io",
    "works": [
        (
            "多 Agent Skills 目录站",
            "louislau-art.github.io/multi-agent-skills-catalog/ · 多 Agent skills、Context7 文档与安装方案",
        ),
        (
            "目录站 GitHub 仓库",
            "github.com/LouisLau-art/multi-agent-skills-catalog · 公开维护 skills catalog 与 profile 方案",
        ),
        (
            "个人主页 / 技术博客",
            "louislau-art.github.io · 项目复盘、技术博客与工程经验沉淀",
        ),
    ],
    "education": [
        {
            "school": "华中师范大学",
            "meta": "硕士 · 人工智能教育学部 · 计算机技术 · 2025.09 - 2027.06",
            "note": "领域方向：时空预测 · 导师：崔建群",
        },
        {
            "school": "北京印刷学院",
            "meta": "本科 · 信息工程学院 · 计算机科学与技术 · 2019.09 - 2023.06",
            "note": "导师：范士喜",
        },
    ],
    "language": [
        "英语 CET-4：610 分",
        "英语 CET-6：469 分",
    ],
    "opensource": [
        "VueUse：修复 useMagicKeys 中键盘事件 key 为 undefined 时的边界情况问题，PR #5225 已合并。",
        "Naive UI：为 DatePicker 组件添加 date slot 与 prefix slot 支持，PR #7382 / #7379。",
        "Una UI：修复 Checkbox 组件颜色解析正则漏洞，补充 destructive 颜色 CSS 变量并优化 SSR 兼容性，PR #553 / #554 / #557。",
        "Ikun-ui：主导适配 Svelte 5 新版运行时的重构，修复渲染问题并重写部分单元测试。",
    ],
    "self_evaluation": "具备较强的自驱力、工程落地意识和文档表达能力，能够把模糊需求快速拆解为可执行方案，并在 AI Agent、后端服务与多方协作之间完成闭环交付。对新工具和新领域学习速度快，既能独立推进，也能和业务、产品、前后端高效配合，为结果负责。",
}


STANDARD_PROJECTS = [
    {
        "title": "multi-agent-skills-catalog（目录站 + 开源仓库）",
        "meta": "持续维护",
        "sub": "AI Agent 工具链 / Skills Catalog / 文档工程",
        "bullets": [
            "维护 `louislau-art.github.io/multi-agent-skills-catalog/` 与 `github.com/LouisLau-art/multi-agent-skills-catalog`，系统整理多 Agent skills、Context7 文档、安装方案与按场景划分的 profile。",
            "围绕 skills catalog、MCP 接入、可安装性校验和多端兼容性持续迭代，沉淀出适合 Codex、Claude Code、Gemini 等 CLI Agent 的能力组织方式。",
            "将公开资料站与开源仓库联动维护，形成可展示、可复用、可持续更新的 AI 工具链作品集。",
        ],
    },
    {
        "title": "internship-jd-catalog（实习JD目录与简历自动化生成系统）",
        "meta": "持续维护",
        "sub": "岗位抓取 / 定向简历生成 / 投递追踪自动化",
        "bullets": [
            "维护 `github.com/LouisLau-art/internship-jd-catalog`，持续抓取和整理大厂技术类实习 JD，统一落库并支持按公司、匹配度和投递状态快速筛选岗位。",
            "构建定向简历生成、共享资料注入、覆盖审计与 PDF 导出链路，降低针对不同 JD 做定制化简历的重复劳动。",
            "打通岗位数据、投递进度与邮件回流同步，支持岗位到简历的映射、待投清单整理和投后跟踪自动化。",
        ],
    },
    {
        "title": "louislau-art.github.io（个人主页 / 技术博客）",
        "meta": "持续维护",
        "sub": "技术品牌建设 / 项目复盘 / 文档沉淀",
        "bullets": [
            "建设并持续维护个人主页，集中展示项目复盘、技术博客与工程实践总结，形成公开可验证的技术作品集。",
            "将 AI Agent、后端工程与复杂业务系统实践沉淀为结构化案例，提升技术表达、对外展示和知识复用效率。",
            "围绕招聘投递、开源协作和技术传播持续优化信息架构与内容组织，提升个人项目材料的可读性与说服力。",
        ],
    },
]


_PROJECT_TOKENS_TO_SKIP = (
    "scholarflow",
    "multi-cloud-email-sender",
    "multi-agent-skills-catalog",
    "louislau-art.github.io",
    "个人主页 / 技术博客",
)


def build_common_profile() -> dict:
    return deepcopy(COMMON_PROFILE)


def normalize_projects(projects: list[dict]) -> list[dict]:
    filtered: list[dict] = []
    for project in projects:
        title = str(project.get("title", "")).lower()
        if any(token in title for token in _PROJECT_TOKENS_TO_SKIP):
            continue
        filtered.append(deepcopy(project))
    return deepcopy(STANDARD_PROJECTS) + filtered
