# MES Alumni Association 

[![Build Status](https://app.travis-ci.com/MESAlumniAssn/mes-aa-jobs.svg?branch=main)](https://app.travis-ci.com/MESAlumniAssn/mes-aa-jobs)

## Setting up the jobs
1. Clone the repository - `https://github.com/MESAlumniAssn/mes-aa-jobs`
2. Create a virtual environment - `python -m venv venv`
3. Activate the virtual environment - `venv\Scripts\activate` (windows) or `source venv/bin/activate` (Linux/MacOS)
4. Install the project dependencies - `pip install -r requirements.txt`
5. Create the environment variables in a `.env` file. Refer to the `.env.example` file for the list of variables
6. Run a specific job -<br />
   :star: Birthday notifications - `python birthday.py`<br />
   :star: Membership expiry notifications - `python expiry_notifications.py`<br />
   :star: Renewal notifications - `python renewal_notifications.py`

Refer to the [Documentation site](https://mesalumniassn.github.io/docs) for the full documentation.
