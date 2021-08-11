import asyncio
import os

import dotenv
import requests_async as requests

dotenv.load_dotenv()

job_secret = os.getenv("JOB_SECRET")


async def send_renewal_notifications(days):
    try:
        upcoming_renewals = await requests.get(
            os.getenv("API_URL") + f"/expiring_memberships/{days}",
            headers={"job-secret": job_secret},
        )

        # Did not send the header
        if upcoming_renewals == 400:
            return

        if not upcoming_renewals.json():
            return

        for renewal in upcoming_renewals.json():
            # Create the renewal hash
            renewal_hash = await requests.put(
                os.getenv("API_URL") + "/renewal_hash",
                json={"email": renewal["email"]},
                headers={"job-secret": job_secret},
            )

            alt_id = renewal["alt_user_id"]

            renewal_url = (
                os.getenv("SITE_URL")
                + "/renewal/"
                + alt_id
                + "-"
                + str(renewal_hash.json())
            )

            await requests.post(
                os.getenv("API_URL") + "/email/renewal",
                json={
                    "name": renewal["name"],
                    "to_email": renewal["email"],
                    "days": days,
                    "renewal_url": renewal_url,
                },
                headers={"job-secret": job_secret},
            )

        else:
            await requests.put(
                os.getenv("API_URL") + "/jobs",
                json={"job_id": int(os.getenv("RENEWAL_NOTIFICATION_JOB_ID"))},
                headers={"job-secret": job_secret},
            )

    except Exception:
        raise (Exception)


if __name__ == "__main__":
    asyncio.run(send_renewal_notifications(30))
    asyncio.run(send_renewal_notifications(1))
