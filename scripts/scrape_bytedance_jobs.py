from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.scrape_campus_jobs import USER_AGENT, write_csv, write_json
except ModuleNotFoundError:  # pragma: no cover - direct script execution path
    from scrape_campus_jobs import USER_AGENT, write_csv, write_json

try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:  # pragma: no cover - environment dependent
    raise SystemExit(
        "Missing dependency: playwright for Python. Install it before running this script."
    ) from exc


DEFAULT_LIST_URL = (
    "https://jobs.bytedance.com/campus/position?keywords=&category=6704215862557018372"
    "&location=&project=7194661126919358757&type=&job_hot_flag=&current=1&limit=10"
    "&functionCategory=&tag="
)
DEFAULT_CHROME_PATH = "/usr/bin/google-chrome"
DEFAULT_PAGE_SIZE = 600


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape ByteDance campus job listings into JSON and CSV.")
    parser.add_argument("--output-dir", default="data")
    parser.add_argument("--list-url", default=DEFAULT_LIST_URL)
    parser.add_argument("--project-id", default="7194661126919358757")
    parser.add_argument("--project-slug", default="byteintern")
    parser.add_argument("--project-name", default="ByteIntern")
    parser.add_argument("--category-id", default="6704215862557018372")
    parser.add_argument("--category-slug", default="backend")
    parser.add_argument("--category-name", default="后端")
    parser.add_argument("--company", default="ByteDance")
    parser.add_argument("--source", default="bytedance")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument("--chrome-path", default=DEFAULT_CHROME_PATH)
    parser.add_argument("--no-headless", action="store_true")
    return parser.parse_args()


def build_position_url(position_id: str) -> str:
    return f"https://jobs.bytedance.com/campus/position/{position_id}/detail"


def join_values(values: list[str]) -> str:
    return " | ".join(value for value in values if value)


def to_publish_time(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat()
    return str(value)


def normalize_job(job: dict[str, object], args: argparse.Namespace) -> dict[str, str]:
    project_name = (
        ((job.get("job_subject") or {}).get("name") or {}).get("zh_cn")
        or ((job.get("job_subject") or {}).get("name") or {}).get("i18n")
        or ((job.get("job_subject") or {}).get("name") or {}).get("en_us")
        or args.project_name
    )
    category_name = ((job.get("job_category") or {}).get("name")) or args.category_name
    cities = job.get("city_list") or []
    work_locations = join_values(
        [
            city.get("name") or city.get("i18n_name") or city.get("en_name") or ""
            for city in cities
            if isinstance(city, dict)
        ]
    )
    feature_tags: list[str] = []
    if job.get("job_hot_flag"):
        feature_tags.append("hot")
    if job.get("process_type") is not None:
        feature_tags.append(f"process_type:{job['process_type']}")
    if job.get("storefront_mode") is not None:
        feature_tags.append(f"storefront_mode:{job['storefront_mode']}")

    return {
        "source": args.source,
        "company": args.company,
        "position_id": str(job.get("id") or ""),
        "parent_position_id": "",
        "job_requirement_id": "",
        "position_intention_id": "",
        "position_intention_name": "",
        "position_name": str(job.get("title") or ""),
        "position_url": build_position_url(str(job.get("id") or "")),
        "position_req_code": str(job.get("code") or ""),
        "batch_id": str(((job.get("job_subject") or {}).get("id")) or args.project_id),
        "batch_name": str(project_name),
        "category_name": str(category_name),
        "family_code": "",
        "family_name": "",
        "data_source": "",
        "work_locations": work_locations
        or str(((job.get("city_info") or {}).get("name")) or ((job.get("city_info") or {}).get("i18n_name")) or ""),
        "interview_locations": "",
        "departments": str(job.get("department_id") or ""),
        "circles": "",
        "circle_codes": "",
        "channels": "campus",
        "feature_tags": join_values(feature_tags),
        "publish_time": to_publish_time(job.get("publish_time")),
        "modify_time": "",
        "graduation_from": "",
        "graduation_to": "",
        "requirement": str(job.get("requirement") or ""),
        "description": str(job.get("description") or ""),
    }


def fetch_all_jobs(args: argparse.Namespace) -> dict[str, object]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=not args.no_headless,
            executable_path=args.chrome_path,
        )
        page = browser.new_page(user_agent=USER_AGENT)
        try:
            page.goto(args.list_url, wait_until="domcontentloaded", timeout=120000)
            page.wait_for_function(
                "() => document.cookie.includes('atsx-csrf-token=')",
                timeout=30000,
            )
            return page.evaluate(
                """
                async ({ categoryId, projectId, pageSize }) => {
                  const token = decodeURIComponent(
                    document.cookie
                      .split('; ')
                      .find((entry) => entry.startsWith('atsx-csrf-token='))
                      ?.split('=')[1] || ''
                  );

                  async function fetchPage(limit, offset) {
                    const payload = {
                      keyword: '',
                      limit,
                      offset,
                      job_category_id_list: [categoryId],
                      tag_id_list: [],
                      location_code_list: [],
                      subject_id_list: [projectId],
                      recruitment_id_list: [],
                      portal_type: 3,
                      job_function_id_list: [],
                      storefront_id_list: [],
                      portal_entrance: 1,
                    };

                    const response = await fetch('/api/v1/search/job/posts', {
                      method: 'POST',
                      credentials: 'include',
                      headers: {
                        accept: 'application/json, text/plain, */*',
                        'content-type': 'application/json',
                        'portal-channel': 'campus',
                        'portal-platform': 'pc',
                        'website-path': 'campus',
                        'x-csrf-token': token,
                        env: 'undefined',
                      },
                      body: JSON.stringify(payload),
                    });

                    if (!response.ok) {
                      const text = await response.text();
                      throw new Error(`ByteDance API failed: ${response.status} ${text.slice(0, 500)}`);
                    }

                    return response.json();
                  }

                  const first = await fetchPage(pageSize, 0);
                  const firstData = first.data || {};
                  const total = Number(firstData.count || 0);
                  const jobs = [...(firstData.job_post_list || [])];

                  for (let offset = jobs.length; offset < total; offset += pageSize) {
                    const next = await fetchPage(pageSize, offset);
                    jobs.push(...((next.data || {}).job_post_list || []));
                  }

                  return {
                    total,
                    token,
                    cookies: document.cookie,
                    jobs,
                  };
                }
                """,
                {
                    "categoryId": args.category_id,
                    "projectId": args.project_id,
                    "pageSize": args.page_size,
                },
            )
        finally:
            browser.close()


def main() -> None:
    args = parse_args()
    result = fetch_all_jobs(args)
    rows = [normalize_job(job, args) for job in result["jobs"]]
    generated_at = datetime.now(timezone.utc).isoformat()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_stem = f"{args.source}_positions_{args.project_slug}_{args.category_slug}"
    json_path = output_dir / f"{file_stem}.json"
    csv_path = output_dir / f"{file_stem}.csv"

    write_json(
        json_path,
        {
            "generated_at": generated_at,
            "source": args.source,
            "company": args.company,
            "project_id": args.project_id,
            "project_name": args.project_name,
            "category_id": args.category_id,
            "category_name": args.category_name,
            "total_count": result["total"],
            "jobs": rows,
        },
    )
    write_csv(csv_path, rows)

    print(f"ByteDance positions: {result['total']}")
    print(f"Wrote {json_path}")
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
