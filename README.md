
# 🚄 Indian Railways Train Scraper Tool

This Python script scrapes **all available train numbers and names** from the official [Indian Railways Schedule page](https://www.indianrail.gov.in/enquiry/SCHEDULE/TrainSchedule.html) using Selenium.

It handles:
- Data collection
- Proxy fallback
- Resume capability
- Error screenshots
- JSON logging of active, new, and retired trains

---

## 🔧 Features

✅ Scrapes all train names and numbers using autocomplete suggestions  
✅ Covers all 676 alphabetic combinations from **AA to ZZ**  
✅ Skips duplicates intelligently  
✅ Detects and logs:
- Newly added trains → `newtrain.json`
- Retired trains → `retiredtrain.json`  
✅ Maintains active list → `trains.json`  
✅ Automatically creates:
- Timestamped backups in `backup/`
- Error screenshots if failures occur  
✅ Resume support — pick up where you left off

---

## 📁 Output Files

All output files are inside the `list_data/` folder:

| File | Description |
|------|-------------|
| `trains.json` | List of all active trains |
| `newtrain.json` | List of new trains since the last run |
| `retiredtrain.json` | List of trains no longer available |
| `backup/trains_backup_*.json` | Timestamped backups |
| `session.json` | Keeps track of completed inputs |
| `errorscreenshot/` | Screenshot folder for errors |

---

## 💻 Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the scraper:
   ```bash
   python scraper.py
   ```

3. On startup, it will prompt:
   ```
   🟡 Resume previous session? (y/n):
   ```

4. The scraper will simulate inputting combos like "AA", "AB", ..., "ZZ", and collect all train numbers shown in the dropdown.

---

## 🌐 Proxy Support

- Tries a **normal connection** first.
- If that fails, retries using an **authenticated rotating proxy**.

You can configure your proxy credentials in the script:
```python
PROXY_HOST = "HOST"
PROXY_PORT = PORT
PROXY_USER = "your-username"
PROXY_PASS = "your-password"
```

---

## ⚠️ Troubleshooting

- Make sure **Google Chrome** is installed.
- The script uses `undetected-chromedriver` to avoid detection.
- If scraping fails, check `errorscreenshot/` for screenshots of the failure.
- Confirm internet or proxy connectivity using the IP check log at the top of the script.

---

## 📦 Requirements

```text
selenium
tqdm
undetected-chromedriver
```

Install using:

```bash
pip install -r requirements.txt
```

---

## 📂 Folder Structure

```
indianrail/
├── scraper.py
├── requirements.txt
├── README.md
└── list_data/
    ├── trains.json
    ├── newtrain.json
    ├── retiredtrain.json
    ├── session.json
    ├── errorscreenshot/
    └── backup/
```

---

## 🧠 How It Works

- Each 2-letter combo (AA–ZZ) is entered in the search box.
- The dropdown of train suggestions is scraped.
- Unique train numbers are stored.
- Previous results are compared to detect any new/removed entries.
- The scraper resumes automatically if interrupted.

---

## 👨‍💻 Author

Made with ❤️ by **Ravi Gautam**
