#!/usr/bin/env python3
"""
QQ 邮箱求职邮件解析脚本

功能：
1. 连接 QQ 邮箱 IMAP 服务器
2. 搜索求职相关邮件（面试、投递、通知、笔试、测评）
3. 解析发件人、公司、主题、正文
4. 提取面试时间、笔试安排等信息
5. 导出为 JSON 格式，方便后续处理

使用方法：
python scripts/parse_qq_job_emails.py
"""

from __future__ import annotations

import argparse
import email
import email.policy
import json
import re
import imaplib
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


# QQ 邮箱 IMAP 服务器配置
QQ_IMAP_SERVER = "imap.qq.com"
QQ_IMAP_PORT_SSL = 993
QQ_IMAP_PORT_NON_SSL = 143

# 公司域名列表
COMPANY_DOMAINS = [
    'bytedance.com', 'mi.com', 'meituan.com', 'jd.com',
    'alibaba-inc.com', 'alibaba.com', 'antgroup.com', 'tencent.com', 
    'xiaohongshu.com', 'huawei.com', 'netease.com', '163.com', '126.com',
    'pinduoduo.com', 'didiglobal.com', 'oceanbase.com'
]

# 动作词列表
ACTION_WORDS = [
    '面试', '笔试', '测评', '安排', '邀请', '录取', 'Offer', '投递', '通知'
]


def decode_str(value: str | bytes | None) -> str:
    """安全解码字符串"""
    if value is None:
        return ""
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8", errors="replace")
        except UnicodeDecodeError:
            try:
                return value.decode("gbk", errors="replace")
            except Exception:
                return str(value)
    return str(value)


def parse_email_address(header_value: str) -> tuple[str, str]:
    """解析邮箱地址，返回（邮箱，显示名）"""
    match = re.search(r"<([^>]+)>", header_value)
    if match:
        email = match.group(1)
        local_part = email.split("@")[0]
        return email, local_part
    return header_value, header_value


def extract_company_from_email(email_addr: str) -> str:
    """从邮箱地址提取公司名"""
    common_companies = {
        "alibaba.com": "Alibaba",
        "antgroup.com": "Ant Group",
        "bytedance.com": "ByteDance",
        "meituan.com": "Meituan",
        "jd.com": "JD",
        "tencent.com": "Tencent",
        "xiaohongshu.com": "Xiaohongshu",
        "oceanbase.com": "OceanBase",
        "huawei.com": "Huawei",
        "xiaomi.com": "Xiaomi",
        "netease.com": "NetEase",
        "pinduoduo.com": "Pinduoduo",
        "didiglobal.com": "Didi",
    }

    domain = email_addr.lower().split("@")[-1] if "@" in email_addr else ""
    return common_companies.get(domain, "Unknown")


def extract_date_from_text(text: str) -> str | None:
    """从文本中提取日期（增强版）"""
    today = datetime.now()
    
    # 相对日期解析
    if "今天" in text:
        return today.strftime("%Y-%m-%d")
    if "明天" in text:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    if "后天" in text:
        return (today + timedelta(days=2)).strftime("%Y-%m-%d")
    
    # 本周几解析
    weekdays = {"周一": 0, "周二": 1, "周三": 2, "周四": 3, "周五": 4, "周六": 5, "周日": 6,
                "星期一": 0, "星期二": 1, "星期三": 2, "星期四": 3, "星期五": 4, "星期六": 5, "星期日": 6}
    for day_str, day_idx in weekdays.items():
        if f"本{day_str}" in text or (day_str in text and "本" in text):
            days_ahead = (day_idx - today.weekday()) % 7
            return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    # 现有正则模式
    date_patterns = [
        r"(\d{4})-(\d{1,2})-(\d{1,2})",  # YYYY-MM-DD
        r"(\d{4})年(\d{1,2})月(\d{1,2})日",  # YYYY年MM月DD日
        r"(\d{1,2})月(\d{1,2})日",  # MM月DD日
        r"(\d{1,2})/(\d{1,2})",  # MM/DD
        r"(\d{1,2})月(\d{1,2})号",  # MM月DD号
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            if "年" in pattern or "-" in pattern:
                # 已经包含年份
                groups = match.groups()
                if len(groups) == 3:
                    return f"{groups[0]}-{int(groups[1]):02d}-{int(groups[2]):02d}"
            else:
                # 不含年份，补全当前年份
                groups = match.groups()
                if len(groups) == 2:
                    return f"{today.year}-{int(groups[0]):02d}-{int(groups[1]):02d}"
    return None


def extract_time_from_text(text: str) -> str | None:
    """从文本中提取时间"""
    time_patterns = [
        r"(\d{1,2}):(\d{2})",  # HH:MM
        r"(\d{1,2})点(\d{2})",  # HH点MM
        r"(\d{1,2})时(\d{2})分",  # HH时MM分
        r"(\d{1,2})点整?",  # HH点
        r"(上午|下午|晚上|中午|早晨|凌晨)(\d{1,2})[点:]?(\d{2})?",  # 上午9:00, 下午3点
    ]

    for pattern in time_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None


def extract_location_from_text(text: str) -> str | None:
    """从文本中提取地点"""
    location_keywords = ["北京", "上海", "广州", "深圳", "杭州", "武汉", "成都", "西安", "南京", "苏州"]
    for keyword in location_keywords:
        if keyword in text:
            return keyword
    return None


def extract_attachments(msg: email.message.EmailMessage) -> list[dict[str, Any]]:
    """提取邮件附件信息"""
    attachments = []

    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue

        content_disposition = part.get("Content-Disposition", "")
        if not content_disposition:
            continue

        filename = part.get_filename()
        if filename:
            payload = part.get_payload(decode=True)
            size = len(payload) if payload else 0
            attachment = {
                "filename": filename,
                "content_type": part.get_content_type(),
                "size": size,
            }
            attachments.append(attachment)

    return attachments


def parse_email_message(msg: email.message.EmailMessage, msg_id: str) -> dict[str, Any]:
    """解析单封邮件，提取关键信息"""
    # 解析头部
    from_header = msg.get("From", "")
    to_header = msg.get("To", "")
    subject_header = msg.get("Subject", "")
    date_header = msg.get("Date", "")

    # 提取发件人信息
    sender_email, sender_display = parse_email_address(from_header)
    sender_company = extract_company_from_email(sender_email)

    # 提取收件人信息
    recipient_email, _ = parse_email_address(to_header)

    # 解析日期
    date_str = ""
    try:
        email_date = email.utils.parsedate_to_datetime(date_header)
        date_str = email_date.astimezone(timezone.utc).isoformat() if email_date else ""
    except Exception:
        pass

    # 获取邮件正文
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if isinstance(payload, list):
                    body = "\n".join([decode_str(p) for p in payload])
                else:
                    body = decode_str(payload)
                break
    else:
        payload = msg.get_payload(decode=True)
        body = decode_str(payload) if payload else ""

    # 提取附件
    attachments = extract_attachments(msg)

    # 从正文中提取关键信息
    interview_date = extract_date_from_text(body)
    interview_time = extract_time_from_text(body)
    location = extract_location_from_text(body)

    # 判断邮件类型
    email_type = "other"
    subject_lower = subject_header.lower()

    if any(keyword in subject_lower for keyword in ["面试", "笔试", "测评", "面试邀请"]):
        email_type = "interview"
    elif any(keyword in subject_lower for keyword in ["投递", "投递成功", "简历投递", "已投递"]):
        email_type = "application"
    elif any(keyword in subject_lower for keyword in ["通知", "提醒", "安排", "结果"]):
        email_type = "notification"

    return {
        "id": msg_id,
        "type": email_type,
        "sender_email": sender_email,
        "sender_display": sender_display,
        "sender_company": sender_company,
        "recipient_email": recipient_email,
        "subject": subject_header,
        "date": date_str,
        "body_preview": body[:500] if len(body) > 500 else body,  # 前500字符预览
        "interview_date": interview_date,
        "interview_time": interview_time,
        "location": location,
        "attachments": [{"filename": a["filename"], "size": a["size"]} for a in attachments[:3]],  # 最多3个附件
        "attachment_count": len(attachments),
    }


def audit_header(subject: str, from_addr: str) -> bool:
    """
    本地审计邮件头部是否相关
    """
    # 检查域名
    domain_match = any(domain in from_addr.lower() for domain in COMPANY_DOMAINS)
    # 检查动作词
    action_match = any(word in subject for word in ACTION_WORDS)
    
    return domain_match or action_match


def search_job_emails(mail: imaplib.IMAP4_SSL, limit: int = 50) -> list[dict[str, Any]]:
    """搜索求职相关邮件（本地头部审计版）"""
    try:
        # 选择收件箱并获取邮件总数
        status, data = mail.select("INBOX")
        if status != "OK":
            print(f"选择收件箱失败: {status}")
            return []
        
        total_messages = int(data[0])
        print(f"收件箱共有 {total_messages} 封邮件")

        # 批量拉取最近 100 封邮件头部
        batch_size = 100
        start = max(1, total_messages - batch_size + 1)
        
        print(f"正在拉取最近 {batch_size} 封邮件头部进行本地审计...")
        # 使用 BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)] 批量拉取头部，不改变已读状态
        status, messages = mail.fetch(f"{start}:{total_messages}", "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
        
        if status != "OK":
            print(f"获取邮件头部失败: {status}")
            return []

        relevant_msg_ids = []
        # messages 是一个列表，每两项为一组 (header_data, ")")
        for i in range(0, len(messages), 2):
            msg_id_match = re.search(r'(\d+) \(BODY', str(messages[i][0]))
            if not msg_id_match:
                continue
            
            msg_id = msg_id_match.group(1)
            msg_data = messages[i][1]
            
            # 简单解析头部
            header_msg = email.message_from_bytes(msg_data, policy=email.policy.default)
            subject = str(header_msg.get("Subject", ""))
            from_addr = str(header_msg.get("From", ""))
            
            if audit_header(subject, from_addr):
                relevant_msg_ids.append(msg_id)

        print(f"审计完成，找到 {len(relevant_msg_ids)} 封相关邮件")

        # 限制返回数量
        relevant_msg_ids = relevant_msg_ids[-limit:] if len(relevant_msg_ids) > limit else relevant_msg_ids

        # 获取详细内容
        result = []
        for msg_id in reversed(relevant_msg_ids):  # 从新到旧
            status, msg_content = mail.fetch(msg_id, "(RFC822)")
            if status == "OK":
                email_message = email.message_from_bytes(msg_content[0][1], policy=email.policy.default)
                parsed = parse_email_message(email_message, str(msg_id))
                result.append(parsed)

        return result

    except Exception as e:
        print(f"审计邮件时出错: {e}")
        import traceback
        traceback.print_exc()
        return []


def load_env_manually(file_path: Path) -> dict[str, str]:
    """手动读取 .env 文件并解析环境变量"""
    env_vars = {}
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip().strip("'").strip('"')
                        env_vars[key] = value
    return env_vars


def get_default_credentials(file_path: Path) -> tuple[str | None, str | None]:
    """
    解析默认凭据。

    优先使用 .env 中的值；若 .env 缺失或字段为空，则回退到已导出的环境变量。
    """
    env_vars = load_env_manually(file_path)
    email_value = env_vars.get("QQ_EMAIL") or os.getenv("QQ_EMAIL")
    auth_code_value = env_vars.get("QQ_AUTH_CODE") or os.getenv("QQ_AUTH_CODE")
    return email_value, auth_code_value


def main() -> None:
    # 加载 .env 文件 (手动模式)
    env_path = Path(".env")
    env_vars = load_env_manually(env_path)
    default_email, default_password = get_default_credentials(env_path)

    if not env_vars and not (default_email and default_password):
        print("警告: 根目录未找到 .env 文件或文件为空，且当前环境变量中也没有 QQ_EMAIL / QQ_AUTH_CODE。")

    parser = argparse.ArgumentParser(
        description="解析 QQ 邮箱中的求职邮件，提取面试、投递、通知等信息"
    )
    parser.add_argument("--email", default=default_email, help="QQ 邮箱地址")
    parser.add_argument("--password", default=default_password, help="QQ 邮箱密码或授权码")
    parser.add_argument("--limit", type=int, default=50, help="最多解析多少封邮件（默认50）")
    parser.add_argument("--output", default="job_emails.json", help="输出文件名")
    parser.add_argument("--port", type=int, default=QQ_IMAP_PORT_SSL, help=f"IMAP 端口（默认 {QQ_IMAP_PORT_SSL}）")
    parser.add_argument("--no-ssl", action="store_true", help="使用非 SSL 连接（端口 143）")

    args = parser.parse_args()

    if not args.email or not args.password:
        print("错误: 未提供 QQ 邮箱地址或授权码。请在 .env 中配置或通过参数传入。")
        sys.exit(1)

    # 确定端口
    port = QQ_IMAP_PORT_NON_SSL if args.no_ssl else args.port

    print(f"连接到 QQ 邮箱: {args.email}")
    print(f"服务器: {QQ_IMAP_SERVER}:{port}")
    print(f"SSL: {'否' if args.no_ssl else '是'}")

    try:
        # 连接到 QQ 邮箱 IMAP 服务器
        if args.no_ssl:
            mail = imaplib.IMAP4(QQ_IMAP_SERVER, port)
        else:
            mail = imaplib.IMAP4_SSL(QQ_IMAP_SERVER, port)
        mail.login(args.email, args.password)

        print("登录成功！")

        # 选择收件箱
        mail.select("INBOX")

        # 搜索求职相关邮件
        emails = search_job_emails(mail, limit=args.limit)

        if not emails:
            print("未找到相关邮件")
            return

        # 按日期排序（如果有日期的话）
        def get_email_date(email_data: dict[str, Any]) -> str:
            date_str = email_data.get("date", "")
            return date_str if date_str else ""

        emails.sort(key=get_email_date, reverse=True)

        # 输出结果
        output_path = Path(args.output)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "email": args.email,
                    "total_count": len(emails),
                    "emails": emails,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(f"\n结果已保存到: {output_path}")

        # 打印摘要
        print("\n=== 邮件摘要 ===")
        type_counts = {}
        for email_data in emails:
            etype = email_data["type"]
            type_counts[etype] = type_counts.get(etype, 0) + 1

        print(f"总计: {len(emails)} 封")
        for etype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {etype}: {count} 封")

        print("\n=== 最近邮件 ===")
        for email_data in emails[:10]:  # 显示最近10封
            print(f"\nID: {email_data['id']}")
            print(f"类型: {email_data['type']}")
            print(f"发件人: {email_data['sender_display'] or email_data['sender_email']}")
            print(f"公司: {email_data['sender_company']}")
            print(f"主题: {email_data['subject']}")
            if email_data.get("interview_date"):
                print(f"面试日期: {email_data['interview_date']}")
            if email_data.get("interview_time"):
                print(f"面试时间: {email_data['interview_time']}")
            if email_data.get("location"):
                print(f"地点: {email_data['location']}")
            if email_data["attachment_count"] > 0:
                print(f"附件: {email_data['attachment_count']} 个")
            print("-" * 50)

        mail.close()

    except imaplib.IMAP4.error as e:
        print(f"IMAP 错误: {e}")
        print("\n可能的原因：")
        print("1. QQ 邮箱未开启 IMAP 服务")
        print("2. 用户名或密码错误")
        print("3. 网络连接问题")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
