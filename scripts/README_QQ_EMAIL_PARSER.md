# QQ 邮箱求职邮件解析脚本

## 概述

`parse_qq_job_emails.py` 用于连接 QQ 邮箱 IMAP 服务器，自动解析求职相关邮件，提取面试、投递、通知等信息。

## 功能特性

✅ **自动搜索求职邮件**
- 按主题关键词搜索：面试、笔试、测评、投递、通知、邀请
- 按发件人域名筛选：Alibaba、Ant Group、ByteDance、Meituan、JD、Tencent、Xiaohongshu、OceanBase、Huawei、Xiaomi、NetEase、Pinduoduo、Didi

✅ **智能解析邮件内容**
- 提取发件人邮箱和显示名
- 识别公司（从邮箱域名）
- 解析邮件主题
- 提取邮件正文（前 500 字符预览）
- 提取附件信息（文件名、大小、类型）

✅ **从正文中提取关键信息**
- 面试日期（支持多种格式：YYYY-MM-DD、YYYY年MM月DD日、MM月DD日等）
- 面试时间（HH:MM、HH点MM、上午/下午/晚上）
- 面试地点（北京、上海、广州、深圳、杭州、武汉等）

✅ **邮件分类**
- `interview` - 面试相关（面试、笔试、测评）
- `application` - 投递相关
- `notification` - 通知、提醒、安排

## 使用方法

### 1. 开启 QQ 邮箱 IMAP 服务

1. 登录 QQ 邮箱网页版：https://mail.qq.com
2. 进入"设置" → "账户" → "IMAP/SMTP 服务"
3. 开启"IMAP 服务"
4. 获取授权码（如果开启独立密码则不需要）
5. 记录服务器信息：
   - 服务器：`imap.qq.com`
   - SSL 端口：`993`
   - 非 SSL 端口：`143`

### 2. 运行脚本

```bash
# 基本用法
python scripts/parse_qq_job_emails.py --email your_qq@qq.com --password your_password

# 使用非 SSL 端口（如果 SSL 不可用）
python scripts/parse_qq_job_emails.py --email your_qq@qq.com --password your_password --no-ssl

# 指定输出文件
python scripts/parse_qq_job_emails.py --email your_qq@qq.com --password your_password --output my_emails.json

# 限制解析邮件数量（默认50封）
python scripts/parse_qq_job_emails.py --email your_qq@qq.com --password your_password --limit 100
```

### 3. 输出格式

脚本会生成 JSON 文件，格式如下：

```json
{
  "generated_at": "2026-03-26T10:00:00Z",
  "email": "your_qq@qq.com",
  "total_count": 15,
  "emails": [
    {
      "id": "12345",
      "type": "interview",
      "sender_email": "hr@alibaba.com",
      "sender_display": "阿里巴巴招聘 <hr@alibaba.com>",
      "sender_company": "Alibaba",
      "recipient_email": "your_qq@qq.com",
      "subject": "【阿里巴巴】面试邀请 - 后端研发工程师",
      "date": "2026-03-25T08:30:00Z",
      "body_preview": "亲爱的同学，恭喜你通过初筛...",
      "interview_date": "2026-03-28",
      "interview_time": "14:00",
      "location": "杭州",
      "attachments": [
        {
          "filename": "面试安排.pdf",
          "content_type": "application/pdf",
          "size": 123456
        }
      ],
      "attachment_count": 1
    }
  ]
}
```

## 邮件字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 邮件唯一标识 |
| `type` | string | 邮件类型：`interview`（面试）、`application`（投递）、`notification`（通知）、`other`（其他） |
| `sender_email` | string | 发件人邮箱地址 |
| `sender_display` | string | 发件人显示名称（含邮箱） |
| `sender_company` | string | 发件公司（从邮箱域名识别） |
| `recipient_email` | string | 收件人邮箱地址 |
| `subject` | string | 邮件主题 |
| `date` | string | 邮件日期（ISO 8601 格式） |
| `body_preview` | string | 邮件正文预览（前 500 字符） |
| `interview_date` | string | 从正文中提取的面试日期 |
| `interview_time` | string | 从正文中提取的面试时间 |
| `location` | string | 从正文中提取的面试地点 |
| `attachments` | array | 附件列表（最多 3 个） |
| `attachment_count` | int | 附件总数 |

## 注意事项

⚠️ **安全提示**
- 脚本不会保存密码，密码仅用于连接
- 建议在安全环境中运行，避免密码泄露到历史记录
- 可以考虑使用 QQ 邮箱的授权码而非独立密码

⚠️ **IMAP 服务限制**
- QQ 邮箱 IMAP 可能需要定期重新授权
- 如果连接失败，请检查 IMAP 服务是否正常开启
- SSL 端口（993）通常更稳定，非 SSL（143）可能需要特殊配置

⚠️ **搜索限制**
- 默认搜索最近 50 封邮件
- 可以通过 `--limit` 参数调整
- 搜索按日期倒序排列

## 下一步

解析后的 JSON 数据可以用于：

1. **更新求职进度文档** - 自动同步到 `docs/job-search-progress.md`
2. **生成面试日历** - 整合所有面试安排
3. **发送提醒** - 整合到日历或待办事项
4. **数据分析** - 统计各公司投递/面试情况

## 相关链接

- [catalog.csv](../catalog.csv) - 核心岗位索引
- [job-search-progress.md](../docs/job-search-progress.md) - 求职进度记事本
