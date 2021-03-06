import asyncio
import os

import dotenv
import requests_async as requests

from helpers.update_job_status import update_job_run_date

dotenv.load_dotenv()

job_secret = os.getenv("JOB_SECRET")


async def send_birthday_wishes():
    try:
        birthdays = await requests.get(
            os.getenv("API_URL") + "/alumni/birthdays",
            headers={"job-secret": job_secret},
        )

        # Did not send the header
        if birthdays.status_code == 400:
            return

        if not birthdays.json():
            await update_job_run_date(os.getenv("BIRTHDAY_JOB_ID"))
            return

        for birthday in birthdays.json():
            await requests.post(
                os.getenv("API_URL") + "/email/birthday",
                json={"name": birthday["name"], "to_email": birthday["email"]},
                headers={"job-secret": job_secret},
            )

        else:
            await update_job_run_date(os.getenv("BIRTHDAY_JOB_ID"))
    except Exception:
        raise (Exception)


if __name__ == "__main__":
    asyncio.run(send_birthday_wishes())
