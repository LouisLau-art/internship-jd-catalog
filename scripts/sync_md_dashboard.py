import json
import os
import re
from datetime import datetime

def generate_fingerprint(company, role, date):
    """Generate a unique fingerprint for a job entry."""
    # Normalize strings: remove bold, strip whitespace, lowercase
    def normalize(s):
        if s is None: return ""
        s = s.replace("**", "")
        return s.strip().lower()
    
    # Use only the date part (YYYY-MM-DD) for fingerprinting
    norm_date = normalize(date)[:10]
    return f"{normalize(company)}|{normalize(role)}|{norm_date}"

def parse_md_table(md_content, section_title):
    """Extract fingerprints from a specific markdown table section."""
    lines = md_content.splitlines()
    table_started = False
    fingerprints = set()
    
    # Find the section
    section_index = -1
    for i, line in enumerate(lines):
        if line.startswith("##") and section_title in line:
            section_index = i
            break
    
    if section_index == -1:
        return fingerprints

    # Find the table after the section
    for i in range(section_index + 1, len(lines)):
        line = lines[i].strip()
        if not line: continue
        if line.startswith("|"):
            if "---" in line or "公司" in line:
                table_started = True
                continue
            if table_started:
                # Filter out the empty parts from split if they are just from leading/trailing pipes
                parts = [p.strip() for p in line.split("|")][1:-1]
                if len(parts) >= 4:
                    if section_title == "已投递岗位":
                        # | 公司 | 岗位 | 地点 | 状态 | 投递日期 | 备注 |
                        company = parts[0]
                        role = parts[1]
                        date = parts[4]
                        if company != "-" and role != "-":
                            fingerprints.add(generate_fingerprint(company, role, date))
                    elif section_title == "已收到面试邀请":
                        # | 公司 | 岗位 | 面试形式 | 日期 |
                        company = parts[0]
                        role = parts[1]
                        date = parts[3]
                        if company != "-" and role != "-":
                            fingerprints.add(generate_fingerprint(company, role, date))
        elif table_started and not line.startswith("|"):
            break
            
    return fingerprints

def sync_emails_to_md(json_data, md_content):
    """Sync email data into markdown content."""
    emails = json_data.get("emails", [])
    if not emails:
        return md_content

    applied_fingerprints = parse_md_table(md_content, "已投递岗位")
    interview_fingerprints = parse_md_table(md_content, "已收到面试邀请")
    
    new_applied_rows = []
    new_interview_rows = []
    
    for email in emails:
        etype = email.get("type", "other")
        company = email.get("sender_company", "Unknown")
        # Extract role from subject (heuristic)
        subject = email.get("subject", "")
        role = subject.split("-")[-1].strip() if "-" in subject else subject
        # Clean up subject like "【阿里巴巴】面试邀请 - 后端研发工程师"
        role = re.sub(r'【.*?】', '', role).strip()
        role = role.replace("面试邀请", "").strip()
        
        email_date = email.get("date", "")[:10] # YYYY-MM-DD
        
        if etype == "interview":
            int_date = email.get("interview_date", email_date)
            int_time = email.get("interview_time", "")
            full_date = f"{int_date} {int_time}".strip()
            fp = generate_fingerprint(company, role, int_date)
            if fp not in interview_fingerprints:
                location = email.get("location", "远程/待定")
                new_interview_rows.append(f"| **{company}** | {role} | {location} | {full_date} |")
                interview_fingerprints.add(fp)
        
        # All job-related emails can be added to "Applied" if not already there
        # but specifically 'application' and 'interview' types
        if etype in ["application", "interview", "notification"]:
            fp = generate_fingerprint(company, role, email_date)
            if fp not in applied_fingerprints:
                location = email.get("location", "-")
                status = "已收到邀请" if etype == "interview" else "已投递"
                new_applied_rows.append(f"| **{company}** | {role} | {location} | {status} | {email_date} | - |")
                applied_fingerprints.add(fp)

    if not new_applied_rows and not new_interview_rows:
        return md_content

    lines = md_content.splitlines()
    
    # Update Applied Table
    if new_applied_rows:
        target_idx = -1
        for i, line in enumerate(lines):
            if "## ✅ 已投递岗位" in line:
                # Find table header
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith("| 公司 |"):
                        target_idx = j + 2 # After separator line
                        break
                break
        
        if target_idx != -1:
            # Check if first row is a placeholder
            if target_idx < len(lines) and "| - | - |" in lines[target_idx]:
                lines[target_idx:target_idx+1] = new_applied_rows
            else:
                # Insert at the top of the table (after header)
                lines[target_idx:target_idx] = new_applied_rows

    # Update Interview Table
    if new_interview_rows:
        target_idx = -1
        for i, line in enumerate(lines):
            if "### 已收到面试邀请" in line:
                # Find table header
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith("| 公司 |"):
                        target_idx = j + 2 # After separator line
                        break
                break
        
        if target_idx != -1:
            # Check if first row is a placeholder
            if target_idx < len(lines) and "| - | - |" in lines[target_idx]:
                lines[target_idx:target_idx+1] = new_interview_rows
            else:
                lines[target_idx:target_idx] = new_interview_rows

    # Update "最后更新" date
    today = datetime.now().strftime("%Y-%m-%d")
    for i, line in enumerate(lines):
        if line.startswith("最后更新："):
            lines[i] = f"最后更新：{today}"
            break

    return "\n".join(lines)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Sync job emails to MD dashboard")
    parser.add_argument("--input", default="data/job_emails.json", help="Path to job_emails.json")
    parser.add_argument("--output", default="docs/job-search-progress.md", help="Path to job-search-progress.md")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Input file {args.input} not found. Skipping sync.")
        exit(0)

    with open(args.input, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    with open(args.output, "r", encoding="utf-8") as f:
        md_content = f.read()

    new_md_content = sync_emails_to_md(json_data, md_content)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(new_md_content)
    
    print(f"Successfully synced {len(json_data.get('emails', []))} emails to {args.output}")
