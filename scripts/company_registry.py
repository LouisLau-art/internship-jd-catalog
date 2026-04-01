from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
TEMP_DOCS_DIR = REPO_ROOT / "docs" / "temp"


def default_status_doc(group_key: str, on_date: date | None = None) -> Path:
    current = on_date or date.today()
    return TEMP_DOCS_DIR / f"{current.isoformat()}-{group_key.replace('_', '-')}-crawl-status.md"


@dataclass(frozen=True)
class CompanyConfig:
    key: str
    display_name: str
    doc_heading: str
    scrape_group: str
    data_json: Path
    data_csv: Path
    source_label: str
    status_doc: Path
    default_top_n: int
    fit_profile_key: str
    resume_strategy_key: str
    source_filters: tuple[str, ...] = ()


COMPANIES: dict[str, CompanyConfig] = {
    "netease": CompanyConfig(
        key="netease",
        display_name="NetEase",
        doc_heading="NetEase（网易）",
        scrape_group="extra_bigtech",
        data_json=DATA_DIR / "netease_positions_intern_tech.json",
        data_csv=DATA_DIR / "netease_positions_intern_tech.csv",
        source_label="技术 / 游戏程序 / 人工智能实习",
        status_doc=default_status_doc("extra_bigtech"),
        default_top_n=3,
        fit_profile_key="netease",
        resume_strategy_key="unapplied_bigtech",
    ),
    "pinduoduo": CompanyConfig(
        key="pinduoduo",
        display_name="Pinduoduo",
        doc_heading="Pinduoduo（拼多多）",
        scrape_group="extra_bigtech",
        data_json=DATA_DIR / "pinduoduo_positions_intern_tech.json",
        data_csv=DATA_DIR / "pinduoduo_positions_intern_tech.csv",
        source_label="技术专场实习",
        status_doc=default_status_doc("extra_bigtech"),
        default_top_n=3,
        fit_profile_key="pinduoduo",
        resume_strategy_key="unapplied_bigtech",
    ),
    "didi": CompanyConfig(
        key="didi",
        display_name="Didi",
        doc_heading="Didi（滴滴）",
        scrape_group="extra_bigtech",
        data_json=DATA_DIR / "didi_positions_intern_tech.json",
        data_csv=DATA_DIR / "didi_positions_intern_tech.csv",
        source_label="技术类实习岗位",
        status_doc=default_status_doc("extra_bigtech"),
        default_top_n=3,
        fit_profile_key="didi",
        resume_strategy_key="unapplied_bigtech",
    ),
    "xiaomi": CompanyConfig(
        key="xiaomi",
        display_name="Xiaomi",
        doc_heading="Xiaomi（小米）",
        scrape_group="extra_bigtech",
        data_json=DATA_DIR / "xiaomi_positions_intern_tech.json",
        data_csv=DATA_DIR / "xiaomi_positions_intern_tech.csv",
        source_label="技术实习岗位",
        status_doc=default_status_doc("extra_bigtech"),
        default_top_n=3,
        fit_profile_key="xiaomi",
        resume_strategy_key="xiaomi",
    ),
    "kuaishou": CompanyConfig(
        key="kuaishou",
        display_name="Kuaishou",
        doc_heading="Kuaishou（快手）",
        scrape_group="more_bigtech",
        data_json=DATA_DIR / "kuaishou_positions_intern_tech.json",
        data_csv=DATA_DIR / "kuaishou_positions_intern_tech.csv",
        source_label="工程类 + 算法类实习",
        status_doc=default_status_doc("more_bigtech"),
        default_top_n=3,
        fit_profile_key="kuaishou",
        resume_strategy_key="unapplied_bigtech",
    ),
    "honor": CompanyConfig(
        key="honor",
        display_name="Honor",
        doc_heading="Honor（荣耀）",
        scrape_group="more_bigtech",
        data_json=DATA_DIR / "honor_positions_intern_tech.json",
        data_csv=DATA_DIR / "honor_positions_intern_tech.csv",
        source_label="研发类实习岗位",
        status_doc=default_status_doc("more_bigtech"),
        default_top_n=3,
        fit_profile_key="honor",
        resume_strategy_key="unapplied_bigtech",
    ),
    "oppo": CompanyConfig(
        key="oppo",
        display_name="OPPO",
        doc_heading="OPPO",
        scrape_group="more_bigtech",
        data_json=DATA_DIR / "oppo_positions_intern_tech.json",
        data_csv=DATA_DIR / "oppo_positions_intern_tech.csv",
        source_label="软件类 + AI/算法类 + 工程技术类实习",
        status_doc=default_status_doc("more_bigtech"),
        default_top_n=3,
        fit_profile_key="oppo",
        resume_strategy_key="unapplied_bigtech",
    ),
    "bilibili": CompanyConfig(
        key="bilibili",
        display_name="Bilibili",
        doc_heading="Bilibili（哔哩哔哩）",
        scrape_group="more_bigtech",
        data_json=DATA_DIR / "bilibili_positions_intern_tech.json",
        data_csv=DATA_DIR / "bilibili_positions_intern_tech.csv",
        source_label="官方实习页",
        status_doc=default_status_doc("more_bigtech"),
        default_top_n=3,
        fit_profile_key="bilibili",
        resume_strategy_key="none",
    ),
    "alibaba": CompanyConfig(
        key="alibaba",
        display_name="Alibaba",
        doc_heading="Alibaba（阿里巴巴）",
        scrape_group="campus_core",
        data_json=DATA_DIR / "campus_positions_combined.json",
        data_csv=DATA_DIR / "campus_positions_combined.csv",
        source_label="阿里校招技术岗 + 合并导出",
        source_filters=("alibaba",),
        status_doc=default_status_doc("campus_core"),
        default_top_n=3,
        fit_profile_key="alibaba",
        resume_strategy_key="alibaba",
    ),
    "antgroup": CompanyConfig(
        key="antgroup",
        display_name="Ant Group",
        doc_heading="Ant Group（蚂蚁）",
        scrape_group="campus_core",
        data_json=DATA_DIR / "campus_positions_combined.json",
        data_csv=DATA_DIR / "campus_positions_combined.csv",
        source_label="蚂蚁校招导出 + 合并导出",
        source_filters=("antgroup",),
        status_doc=default_status_doc("campus_core"),
        default_top_n=3,
        fit_profile_key="antgroup",
        resume_strategy_key="antgroup",
    ),
    "bytedance": CompanyConfig(
        key="bytedance",
        display_name="ByteDance",
        doc_heading="ByteDance（字节跳动）",
        scrape_group="campus_core",
        data_json=DATA_DIR / "campus_positions_combined.json",
        data_csv=DATA_DIR / "campus_positions_combined.csv",
        source_label="ByteIntern + DailyIntern 维护导出",
        source_filters=("bytedance",),
        status_doc=default_status_doc("campus_core"),
        default_top_n=3,
        fit_profile_key="bytedance",
        resume_strategy_key="bytedance",
    ),
    "meituan": CompanyConfig(
        key="meituan",
        display_name="Meituan",
        doc_heading="Meituan（美团）",
        scrape_group="campus_core",
        data_json=DATA_DIR / "campus_positions_combined.json",
        data_csv=DATA_DIR / "campus_positions_combined.csv",
        source_label="美团维护导出",
        source_filters=("meituan",),
        status_doc=default_status_doc("campus_core"),
        default_top_n=3,
        fit_profile_key="meituan",
        resume_strategy_key="meituan",
    ),
    "jd": CompanyConfig(
        key="jd",
        display_name="JD",
        doc_heading="JD（京东）",
        scrape_group="campus_core",
        data_json=DATA_DIR / "campus_positions_combined.json",
        data_csv=DATA_DIR / "campus_positions_combined.csv",
        source_label="京东维护导出",
        source_filters=("jd",),
        status_doc=default_status_doc("campus_core"),
        default_top_n=3,
        fit_profile_key="jd",
        resume_strategy_key="jd",
    ),
    "tencent": CompanyConfig(
        key="tencent",
        display_name="Tencent",
        doc_heading="Tencent（腾讯）",
        scrape_group="campus_core",
        data_json=DATA_DIR / "campus_positions_combined.json",
        data_csv=DATA_DIR / "campus_positions_combined.csv",
        source_label="腾讯维护导出",
        source_filters=("tencent",),
        status_doc=default_status_doc("campus_core"),
        default_top_n=3,
        fit_profile_key="tencent",
        resume_strategy_key="tencent",
    ),
    "xiaohongshu": CompanyConfig(
        key="xiaohongshu",
        display_name="Xiaohongshu",
        doc_heading="Xiaohongshu（小红书）",
        scrape_group="campus_core",
        data_json=DATA_DIR / "campus_positions_combined.json",
        data_csv=DATA_DIR / "campus_positions_combined.csv",
        source_label="小红书维护导出",
        source_filters=("xiaohongshu",),
        status_doc=default_status_doc("campus_core"),
        default_top_n=3,
        fit_profile_key="xiaohongshu",
        resume_strategy_key="xiaohongshu",
    ),
    "huawei": CompanyConfig(
        key="huawei",
        display_name="Huawei",
        doc_heading="Huawei（华为）",
        scrape_group="campus_core",
        data_json=DATA_DIR / "campus_positions_combined.json",
        data_csv=DATA_DIR / "campus_positions_combined.csv",
        source_label="华为校招官网 + 合并导出",
        source_filters=("huawei",),
        status_doc=default_status_doc("campus_core"),
        default_top_n=3,
        fit_profile_key="huawei",
        resume_strategy_key="huawei",
    ),
}


def filter_company_jobs(payload: dict[str, object], company: CompanyConfig) -> list[dict[str, object]]:
    jobs = list(payload.get("jobs") or [])
    if not company.source_filters:
        return jobs
    allowed = {source.lower() for source in company.source_filters}
    return [job for job in jobs if str(job.get("source", "")).strip().lower() in allowed]


def count_company_jobs(payload: dict[str, object], company: CompanyConfig) -> int:
    filtered_jobs = filter_company_jobs(payload, company)
    if company.source_filters:
        return len(filtered_jobs)
    total_count = payload.get("total_count")
    return int(total_count) if total_count not in (None, "") else len(filtered_jobs)


def parse_company_keys(value: str | Iterable[str]) -> list[str]:
    if isinstance(value, str):
        raw_items = value.split(",")
    else:
        raw_items = list(value)

    ordered: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        key = str(item).strip().lower()
        if not key or key in seen:
            continue
        ordered.append(key)
        seen.add(key)
    return ordered


def get_company_config(key: str) -> CompanyConfig:
    normalized = key.strip().lower()
    try:
        return COMPANIES[normalized]
    except KeyError as exc:
        raise KeyError(f"unknown company key: {normalized}") from exc


def group_companies_by_scrape_group(company_keys: Iterable[str]) -> "OrderedDict[str, list[CompanyConfig]]":
    grouped: "OrderedDict[str, list[CompanyConfig]]" = OrderedDict()
    for key in parse_company_keys(company_keys):
        company = get_company_config(key)
        grouped.setdefault(company.scrape_group, []).append(company)
    return grouped
