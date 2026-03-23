import argparse
import csv
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

CSV_COLUMNS = [
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
]

def join_values(values):
    if not values:
        return ""
    if isinstance(values, (list, tuple)):
        return " | ".join(str(value) for value in values if value not in (None, ""))
    return str(values)

def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in CSV_COLUMNS})

def write_json(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def post_json(url, payload, headers):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))

def normalize_meituan_job(job):
    job_union_id = job.get("jobUnionId")
    work_locations = " | ".join([city.get("name", "") for city in job.get("cityList", [])])
    departments = " | ".join([dept.get("name", "") for dept in job.get("department", [])])
    
    return {
        "source": "meituan",
        "company": "Meituan",
        "position_id": job_union_id,
        "position_name": job.get("name", ""),
        "position_url": f"https://zhaopin.meituan.com/web/position/detail?jobUnionId={job_union_id}",
        "category_name": job.get("jobFamily", ""),
        "work_locations": work_locations,
        "departments": departments,
        "requirement": job.get("jobRequirement") or job.get("highLight", ""),
        "description": job.get("jobDuty", ""),
        "publish_time": job.get("refreshTime", ""),
        "batch_name": "Meituan Campus Internship",
    }

def normalize_jd_job(job):
    publish_id = job.get("publishId")
    req_id = job.get("reqId")
    plan_id = job.get("planId")
    
    # Extract work locations from requirementVoList
    work_locations_list = []
    for req in job.get("requirementVoList", []):
        if req.get("workCity"):
            work_locations_list.append(req.get("workCity"))
    work_locations = " | ".join(work_locations_list)
    
    return {
        "source": "jd",
        "company": "JD",
        "position_id": publish_id,
        "parent_position_id": str(req_id),
        "batch_id": str(plan_id),
        "position_name": job.get("positionName", ""),
        "position_url": f"https://campus.jd.com/#/jobs/detail?publishId={publish_id}&reqId={req_id}&planId={plan_id}",
        "category_name": job.get("jobCategory", ""),
        "work_locations": work_locations,
        "requirement": job.get("qualification", ""),
        "description": job.get("workContent", ""),
        "publish_time": job.get("publishTime", ""),
        "batch_name": "JD Campus Recruitment",
    }

def fetch_meituan_all():
    url = "https://zhaopin.meituan.com/api/official/job/getJobList"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        "Origin": "https://zhaopin.meituan.com",
        "Referer": "https://zhaopin.meituan.com/web/position?hiringType=4_6&jfJgList=11001_1100109"
    }
    
    all_jobs = []
    page_no = 1
    page_size = 100
    
    while True:
        payload = {
            "page": {"pageNo": page_no, "pageSize": page_size},
            "jobShareType": "1",
            "keywords": "",
            "cityList": [],
            "department": [],
            "jfJgList": [{"code": "11001", "subCode": ["1100109"]}],
            "jobType": [{"code": "4", "subCode": ["6"]}],
            "typeCode": ["6"],
            "specialCode": [],
            "u_query_id": "117e130b344d60740dbf8a15e4f5b674",
            "r_query_id": str(int(time.time() * 1000))
        }
        
        try:
            print(f"Fetching Meituan page {page_no}...")
            response = post_json(url, payload, headers)
            jobs = response.get("data", {}).get("list", [])
            if not jobs:
                break
            all_jobs.extend([normalize_meituan_job(job) for job in jobs])
            
            total_count = response.get("data", {}).get("totalCount", 0)
            if len(all_jobs) >= total_count:
                break
            page_no += 1
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching Meituan: {e}")
            break
            
    return all_jobs

def fetch_jd_all():
    url = "https://campus.jd.com/api/wx/position/page?type=present"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        "Origin": "https://campus.jd.com",
        "Referer": "https://campus.jd.com/"
    }
    
    all_jobs = []
    page_index = 0
    page_size = 100
    
    while True:
        payload = {
            "pageSize": page_size,
            "pageIndex": page_index,
            "parameter": {
                "positionName": "",
                "planIdList": ["45"],
                "jobDirectionCodeList": [],
                "workCityCodeList": [],
                "positionDeptList": []
            }
        }
        
        try:
            print(f"Fetching JD page {page_index}...")
            response = post_json(url, payload, headers)
            body = response.get("body", {})
            jobs = body.get("items", [])
            if not jobs:
                break
            all_jobs.extend([normalize_jd_job(job) for job in jobs])
            
            total_number = body.get("totalNumber", 0)
            if len(all_jobs) >= total_number:
                break
            page_index += 1
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching JD: {e}")
            break
            
    return all_jobs

def main():
    output_dir = Path("data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    meituan_jobs = fetch_meituan_all()
    print(f"Total Meituan jobs: {len(meituan_jobs)}")
    write_json(output_dir / "meituan_positions.json", {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "meituan",
        "total_count": len(meituan_jobs),
        "jobs": meituan_jobs
    })
    write_csv(output_dir / "meituan_positions.csv", meituan_jobs)
    
    jd_jobs = fetch_jd_all()
    print(f"Total JD jobs: {len(jd_jobs)}")
    write_json(output_dir / "jd_positions.json", {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "jd",
        "total_count": len(jd_jobs),
        "jobs": jd_jobs
    })
    write_csv(output_dir / "jd_positions.csv", jd_jobs)

if __name__ == "__main__":
    main()
