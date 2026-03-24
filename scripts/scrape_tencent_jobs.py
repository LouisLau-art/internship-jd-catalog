import json
import urllib.request
import time
from datetime import datetime, timezone

def fetch_tencent_jobs():
    url = 'https://join.qq.com/api/v1/position/searchPosition'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Referer': 'https://join.qq.com/post.html'
    }
    
    all_jobs = []
    # Project mappings for technical internships
    # 2: 应届实习, 104: 日常实习
    # positionFidList: technical categories found in the capture
    payload = {
        'bgList': [],
        'keyword': '',
        'pageIndex': 1,
        'pageSize': 100,
        'positionFidList': [75, 76, 77, 84, 93, 231, 250],
        'projectMappingIdList': [2, 104],
        'recruitCityList': [],
        'workCityList': [],
        'workCountryType': 0
    }
    
    print(f"Fetching Tencent jobs from {url}...")
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data['status'] == 0:
                jobs = data['data']['positionList']
                print(f"Found {len(jobs)} technical jobs.")
                for job in jobs:
                    normalized = {
                        "source": "tencent",
                        "company": "Tencent",
                        "position_id": str(job.get('postId')),
                        "parent_position_id": "",
                        "job_requirement_id": "",
                        "position_intention_id": "",
                        "position_intention_name": "",
                        "position_name": job.get('positionTitle'),
                        "position_url": f"https://join.qq.com/post.html?postid={job.get('postId')}",
                        "position_req_code": "",
                        "batch_id": str(job.get('projectId')),
                        "batch_name": job.get('projectName'),
                        "category_name": "技术",
                        "family_code": "",
                        "family_name": "",
                        "data_source": "oa",
                        "work_locations": job.get('workCities', '').strip(),
                        "interview_locations": "",
                        "departments": job.get('bgs', '').strip(),
                        "circles": "",
                        "circle_codes": "",
                        "channels": "campus",
                        "feature_tags": job.get('recruitLabelName', ''),
                        "publish_time": "",
                        "modify_time": "",
                        "graduation_from": "",
                        "graduation_to": "",
                        "requirement": "请访问职位详情页查看完整要求。",
                        "description": f"事业群: {job.get('bgs')}",
                    }
                    all_jobs.append(normalized)
            else:
                print(f"Error from API: {data.get('message')}")
    except Exception as e:
        print(f"Request failed: {e}")
        
    return all_jobs

if __name__ == "__main__":
    jobs = fetch_tencent_jobs()
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "tencent",
        "total_count": len(jobs),
        "jobs": jobs
    }
    with open('data/tencent_positions.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(jobs)} jobs to data/tencent_positions.json")
