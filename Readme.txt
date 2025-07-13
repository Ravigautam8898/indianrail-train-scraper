========================================
🚄 INDIAN RAILWAYS TRAIN SCRAPER TOOL
========================================

📌 DESCRIPTION:
---------------
This script automates the scraping of **all operational train numbers and names** listed on the Indian Railways official site:
https://www.indianrail.gov.in/enquiry/SCHEDULE/TrainSchedule.html

It works by simulating keyboard inputs (AA to ZZ) into the train number search field and capturing every train shown in the dropdown results.

🎯 MAIN FEATURES:
-----------------
✔ Scrapes all publicly listed trains (based on autocomplete results)
✔ Tracks new trains added since the last run (saved to: `newtrain.json`)
✔ Detects and logs removed/retired trains (saved to: `retiredtrain.json`)
✔ Saves full active list to: `trains.json`
✔ Automatically backs up the previous train list to: `backup/trains_backup_<timestamp>.json`
✔ Resume scraping from where it left off if interrupted
✔ Captures error screenshots if any issues occur during scraping

📁 OUTPUT FILES:
---------------
- `list_data/trains.json` — Master list of all active trains
- `list_data/newtrain.json` — Trains newly added since last run
- `list_data/retiredtrain.json` — Trains no longer listed (retired/removed)
- `list_data/backup/` — Timestamped backups of previous train data
- `list_data/session.json` — Tracks completed combinations (for resume)
- `list_data/errorscreenshot/` — Screenshots of failed scraping attempts

🔧 DEPENDENCIES:
----------------
Install the required libraries with:

    pip install -r requirements.txt

🖥 USAGE:
---------
Run the script from the terminal:

    python scraper.py

You'll be prompted to resume or start a fresh session.

🌐 PROXY SUPPORT:
-----------------
- The script first tries to launch Chrome without a proxy.
- If it fails, it retries with a rotating authenticated proxy (PyProxy API).

🛠️ TROUBLESHOOTING:
-------------------
- Make sure `Chrome` is installed and matches your `chromedriver` version.
- On Windows Server, ensure you are running with internet access and no browser restrictions.
- If system-wide proxy is in use, and you're behind authentication, ensure the credentials are working.

📂 FOLDER STRUCTURE:
--------------------
indianrail/
│
├── scraper.py
├── requirements.txt
├── README.txt
└── list_data/
    ├── trains.json
    ├── newtrain.json
    ├── retiredtrain.json
    ├── session.json
    ├── errorscreenshot/
    └── backup/

✍️ AUTHOR:
----------
Created by Ravi Gautam

