#!/usr/bin/env bun

const fs = require("fs");
const path = require("path");

let chromium;
try {
  ({ chromium } = require("playwright"));
} catch (error) {
  console.error(
    "Missing dependency: playwright. Install it locally or run Bun with NODE_PATH pointing at a node_modules directory that contains Playwright."
  );
  console.error(String(error));
  process.exit(1);
}

const USER_AGENT =
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36";
const DEFAULT_LIST_URL =
  "https://jobs.bytedance.com/campus/position?keywords=&category=6704215862557018372&location=&project=7194661126919358757&type=&job_hot_flag=&current=1&limit=10&functionCategory=&tag=";
const DEFAULT_CHROME_PATH = "/usr/bin/google-chrome";
const DEFAULT_PAGE_SIZE = 600;

const CSV_COLUMNS = [
  "source",
  "company",
  "position_id",
  "parent_position_id",
  "job_requirement_id",
  "position_intention_id",
  "position_intention_name",
  "position_name",
  "position_url",
  "position_req_code",
  "batch_id",
  "batch_name",
  "category_name",
  "family_code",
  "family_name",
  "data_source",
  "work_locations",
  "interview_locations",
  "departments",
  "circles",
  "circle_codes",
  "channels",
  "feature_tags",
  "publish_time",
  "modify_time",
  "graduation_from",
  "graduation_to",
  "requirement",
  "description",
];

function parseArgs(argv) {
  const args = {
    outputDir: "data",
    listUrl: DEFAULT_LIST_URL,
    projectId: "7194661126919358757",
    projectSlug: "byteintern",
    projectName: "ByteIntern",
    categoryId: "6704215862557018372",
    categorySlug: "backend",
    categoryName: "后端",
    company: "ByteDance",
    source: "bytedance",
    pageSize: DEFAULT_PAGE_SIZE,
    chromePath: process.env.BYTEDANCE_CHROME_PATH || DEFAULT_CHROME_PATH,
    headless: true,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    if (key === "no-headless") {
      args.headless = false;
      continue;
    }
    const value = argv[index + 1];
    if (value === undefined) {
      throw new Error(`Missing value for argument ${token}`);
    }
    index += 1;
    switch (key) {
      case "output-dir":
        args.outputDir = value;
        break;
      case "list-url":
        args.listUrl = value;
        break;
      case "project-id":
        args.projectId = value;
        break;
      case "project-slug":
        args.projectSlug = value;
        break;
      case "project-name":
        args.projectName = value;
        break;
      case "category-id":
        args.categoryId = value;
        break;
      case "category-slug":
        args.categorySlug = value;
        break;
      case "category-name":
        args.categoryName = value;
        break;
      case "page-size":
        args.pageSize = Number.parseInt(value, 10);
        break;
      case "chrome-path":
        args.chromePath = value;
        break;
      default:
        throw new Error(`Unknown argument: ${token}`);
    }
  }

  if (!Number.isFinite(args.pageSize) || args.pageSize <= 0) {
    throw new Error(`Invalid page size: ${args.pageSize}`);
  }

  return args;
}

function buildPositionUrl(positionId) {
  return `https://jobs.bytedance.com/campus/position/${positionId}/detail`;
}

function joinValues(values) {
  if (!values) return "";
  if (Array.isArray(values)) {
    return values
      .map((value) => String(value ?? "").trim())
      .filter(Boolean)
      .join(" | ");
  }
  return String(values);
}

function toPublishTime(value) {
  if (!value) return "";
  if (typeof value === "number") {
    return new Date(value).toISOString();
  }
  return String(value);
}

function normalizeJob(job, args) {
  const projectName =
    job?.job_subject?.name?.zh_cn ||
    job?.job_subject?.name?.i18n ||
    job?.job_subject?.name?.en_us ||
    args.projectName;
  const categoryName = job?.job_category?.name || args.categoryName;
  const workLocations = joinValues(
    (job?.city_list || []).map((city) => city?.name || city?.i18n_name || city?.en_name).filter(Boolean)
  );
  const departmentId = job?.department_id ? String(job.department_id) : "";
  const featureTags = [];
  if (job?.job_hot_flag) featureTags.push("hot");
  if (job?.process_type != null) featureTags.push(`process_type:${job.process_type}`);
  if (job?.storefront_mode != null) featureTags.push(`storefront_mode:${job.storefront_mode}`);

  return {
    source: args.source,
    company: args.company,
    position_id: String(job?.id || ""),
    parent_position_id: "",
    job_requirement_id: "",
    position_intention_id: "",
    position_intention_name: "",
    position_name: job?.title || "",
    position_url: buildPositionUrl(job?.id || ""),
    position_req_code: job?.code || "",
    batch_id: job?.job_subject?.id || args.projectId,
    batch_name: projectName,
    category_name: categoryName,
    family_code: "",
    family_name: "",
    data_source: "",
    work_locations:
      workLocations ||
      job?.city_info?.name ||
      job?.city_info?.i18n_name ||
      job?.city_info?.en_name ||
      "",
    interview_locations: "",
    departments: departmentId,
    circles: "",
    circle_codes: "",
    channels: "campus",
    feature_tags: joinValues(featureTags),
    publish_time: toPublishTime(job?.publish_time),
    modify_time: "",
    graduation_from: "",
    graduation_to: "",
    requirement: job?.requirement || "",
    description: job?.description || "",
  };
}

function writeJson(filePath, payload) {
  fs.writeFileSync(filePath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function escapeCsvCell(value) {
  const text = String(value ?? "");
  if (text.includes('"') || text.includes(",") || text.includes("\n") || text.includes("\r")) {
    return `"${text.replaceAll('"', '""')}"`;
  }
  return text;
}

function writeCsv(filePath, rows) {
  const lines = [CSV_COLUMNS.join(",")];
  for (const row of rows) {
    lines.push(CSV_COLUMNS.map((column) => escapeCsvCell(row[column] || "")).join(","));
  }
  fs.writeFileSync(filePath, `${lines.join("\n")}\n`, "utf8");
}

async function bootstrapAndFetchAll(args) {
  const browser = await chromium.launch({
    headless: args.headless,
    executablePath: args.chromePath,
  });
  const page = await browser.newPage({ userAgent: USER_AGENT });

  try {
    await page.goto(args.listUrl, { waitUntil: "domcontentloaded", timeout: 120000 });
    await page.waitForFunction(
      () => document.cookie.includes("atsx-csrf-token="),
      {},
      { timeout: 30000 }
    );

    return await page.evaluate(async ({ categoryId, projectId, pageSize }) => {
      const token = decodeURIComponent(
        document.cookie
          .split("; ")
          .find((entry) => entry.startsWith("atsx-csrf-token="))
          ?.split("=")[1] || ""
      );

      async function fetchPage(limit, offset) {
        const payload = {
          keyword: "",
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

        const response = await fetch("/api/v1/search/job/posts", {
          method: "POST",
          credentials: "include",
          headers: {
            accept: "application/json, text/plain, */*",
            "content-type": "application/json",
            "portal-channel": "campus",
            "portal-platform": "pc",
            "website-path": "campus",
            "x-csrf-token": token,
            env: "undefined",
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const text = await response.text();
          throw new Error(`ByteDance API failed: ${response.status} ${text.slice(0, 500)}`);
        }

        const body = await response.json();
        return body.data;
      }

      const firstPage = await fetchPage(pageSize, 0);
      const total = Number(firstPage.count || 0);
      const jobs = [...(firstPage.job_post_list || [])];

      for (let offset = jobs.length; offset < total; offset += pageSize) {
        const nextPage = await fetchPage(pageSize, offset);
        jobs.push(...(nextPage.job_post_list || []));
      }

      return {
        total,
        cookies: document.cookie,
        jobs,
      };
    }, { categoryId: args.categoryId, projectId: args.projectId, pageSize: args.pageSize });
  } finally {
    await browser.close();
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const result = await bootstrapAndFetchAll(args);
  const rows = result.jobs.map((job) => normalizeJob(job, args));
  const generatedAt = new Date().toISOString();

  const outputDir = path.resolve(process.cwd(), args.outputDir);
  fs.mkdirSync(outputDir, { recursive: true });

  const fileStem = `${args.source}_positions_${args.projectSlug}_${args.categorySlug}`;
  const jsonPath = path.join(outputDir, `${fileStem}.json`);
  const csvPath = path.join(outputDir, `${fileStem}.csv`);

  writeJson(jsonPath, {
    generated_at: generatedAt,
    source: args.source,
    company: args.company,
    project_id: args.projectId,
    project_name: args.projectName,
    category_id: args.categoryId,
    category_name: args.categoryName,
    total_count: result.total,
    jobs: rows,
  });
  writeCsv(csvPath, rows);

  console.log(`ByteDance positions: ${result.total}`);
  console.log(`Wrote ${jsonPath}`);
  console.log(`Wrote ${csvPath}`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : String(error));
  process.exit(1);
});
