import os

import dotenv

dotenv.load_dotenv()

import requests_async as requests

job_secret = os.getenv("JOB_SECRET")


async def update_job_run_date(job_id):
    try:
        await requests.put(
            os.getenv("API_URL") + "/jobs",
            json={"job_id": int(job_id)},
            headers={"job-secret": job_secret},
        )
    except Exception:
        raise Exception
