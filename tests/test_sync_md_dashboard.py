import sys
import os
import json

# Add scripts directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.sync_md_dashboard import sync_emails_to_md, generate_fingerprint

def test_sync_logic():
    sample_json = {
        "emails": [
            {
                "id": "1",
                "type": "interview",
                "sender_company": "Alibaba",
                "subject": "【阿里巴巴】面试邀请 - AI应用研发工程师",
                "date": "2026-03-27T10:00:00Z",
                "interview_date": "2026-03-30",
                "interview_time": "14:00",
                "location": "远程"
            },
            {
                "id": "2",
                "type": "application",
                "sender_company": "Tencent",
                "subject": "投递成功 - 后端开发实习生",
                "date": "2026-03-27T11:00:00Z"
            }
        ]
    }

    sample_md = """# 求职进度记事本

最后更新：2026-03-26

## ✅ 已投递岗位（track=targeted）

| 公司 | 岗位 | 地点 | 状态 | 投递日期 | 备注 |
| ----------------- | ------------------------------ | -------- | ----- | ---------- | --------------------- |
| **Meituan** | 基础技术-AI Coding项目实习生 | 北京 | 技术面完成 | 2026-03-26 | 上午已完成面试 |

## 📋 面试记录

### 已收到面试邀请

| 公司 | 岗位 | 面试形式 | 日期 |
| --- | --- | ---- | --- |
| - | - | - | - |
"""

    new_md = sync_emails_to_md(sample_json, sample_md)
    
    # Check if Alibaba interview is added to "已收到面试邀请"
    assert "Alibaba" in new_md
    assert "AI应用研发工程师" in new_md
    assert "2026-03-30 14:00" in new_md
    
    # Check if Tencent application is added to "已投递岗位"
    assert "Tencent" in new_md
    assert "后端开发实习生" in new_md
    assert "2026-03-27" in new_md
    
    # Check for deduplication
    new_md_v2 = sync_emails_to_md(sample_json, new_md)
    if new_md_v2 != new_md:
        import difflib
        diff = difflib.ndiff(new_md.splitlines(), new_md_v2.splitlines())
        print("Diff between new_md and new_md_v2:")
        print("\n".join(diff))
    assert new_md_v2 == new_md
    
    print("All tests passed!")

if __name__ == "__main__":
    test_sync_logic()
