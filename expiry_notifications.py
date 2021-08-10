import asyncio
import os

import dotenv
import requests_async as requests

dotenv.load_dotenv()

job_secret = os.getenv("JOB_SECRET")


async def send_expiry_notifications():
    try:
        expired_memberships = await requests.get(
            os.getenv("API_URL") + "/recently_expired_memberships",
            headers={"job-secret": job_secret},
        )

        # Did not send the header
        if expired_memberships == 400:
            return

        if not expired_memberships:
            return

        for membership in expired_memberships.json():
            await requests.put(
                os.getenv("API_URL") + "/expire_active_memberships",
                json={"email": membership["email"]},
                headers={"job-secret": job_secret},
            )

            alt_id = membership["alt_user_id"]
            renewal_hash = membership["renewal_hash"]

            renewal_url = os.getenv("SITE_URL") + f"/renewal/{alt_id}-{renewal_hash}"

            await requests.post(
                os.getenv("API_URL") + "/email/expired_membership",
                json={
                    "name": membership["name"],
                    "to_email": membership["email"],
                    "renewal_url": renewal_url,
                },
            )

        else:
            await requests.put(
                os.getenv("API_URL") + "/jobs",
                json={"job_id": int(os.getenv("EXPIRY_NOTIFICATION_JOB_ID"))},
                headers={"job-secret": job_secret},
            )

    except Exception:
        raise (Exception)


if __name__ == "__main__":
    asyncio.run(send_expiry_notifications())
