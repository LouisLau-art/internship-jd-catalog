import os
import sys
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts import parse_qq_job_emails as qq_job_emails


def test_env_example_uses_real_newlines():
    content = Path(".env.example").read_text(encoding="utf-8")

    assert "\\n" not in content
    assert content.splitlines() == [
        "QQ_EMAIL=您的QQ邮箱@qq.com",
        "QQ_AUTH_CODE=您的IMAP授权码",
    ]


def test_get_default_credentials_falls_back_to_process_env(tmp_path, monkeypatch):
    monkeypatch.setenv("QQ_EMAIL", "env-user@qq.com")
    monkeypatch.setenv("QQ_AUTH_CODE", "env-auth-code")

    email, auth_code = qq_job_emails.get_default_credentials(tmp_path / ".env")

    assert email == "env-user@qq.com"
    assert auth_code == "env-auth-code"


def test_get_default_credentials_prefers_dotenv_values(tmp_path, monkeypatch):
    env_path = tmp_path / ".env"
    env_path.write_text(
        "QQ_EMAIL=file-user@qq.com\nQQ_AUTH_CODE=file-auth-code\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("QQ_EMAIL", "env-user@qq.com")
    monkeypatch.setenv("QQ_AUTH_CODE", "env-auth-code")

    email, auth_code = qq_job_emails.get_default_credentials(env_path)

    assert email == "file-user@qq.com"
    assert auth_code == "file-auth-code"
