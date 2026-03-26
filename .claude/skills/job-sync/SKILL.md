# Job Sync Skill

This skill automates the synchronization of job notifications from QQ emails to the project dashboard.

## /sync-jobs

Synchronizes job notifications from QQ emails and updates the job search progress dashboard.

### Logic
1.  **Check Environment**: Verifies that the `.env` file exists and contains the necessary `QQ_EMAIL` and `QQ_AUTH_CODE`.
2.  **Parse Emails**: Runs `python scripts/parse_qq_job_emails.py --output data/job_emails.json` to extract job information from emails.
3.  **Update Dashboard**: Runs `python scripts/sync_md_dashboard.py --input data/job_emails.json --output docs/job-search-progress.md` to update the markdown dashboard.

### Usage
```bash
/sync-jobs
```

### Requirements
- Python 3.x
- `.env` file with `QQ_EMAIL` and `QQ_AUTH_CODE`.
