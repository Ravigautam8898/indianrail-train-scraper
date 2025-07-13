import os
import json
import time
import string
import datetime
import shutil
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import undetected_chromedriver as uc

# === Proxy Auth ===
PROXY_HOST = "host"
PROXY_PORT = port
PROXY_USER = "username"
PROXY_PASS = "password"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "list_data")
SESSION_FILE = os.path.join(OUTPUT_DIR, "session.json")
ERROR_SCREENSHOT_DIR = os.path.join(OUTPUT_DIR, "errorscreenshot")
TRAINS_JSON = os.path.join(OUTPUT_DIR, "trains.json")
NEW_JSON = os.path.join(OUTPUT_DIR, "newtrain.json")
REMOVED_JSON = os.path.join(OUTPUT_DIR, "retiredtrain.json")
BACKUP_DIR = os.path.join(OUTPUT_DIR, "backup")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ERROR_SCREENSHOT_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

ALL_COMBOS = [a + b for a in string.ascii_uppercase for b in string.ascii_uppercase]

def load_session():
    if os.path.exists(SESSION_FILE):
        choice = input("🟡 Resume previous session? (y/n): ").strip().lower()
        if choice == 'y':
            with open(SESSION_FILE, "r") as f:
                return json.load(f).get("done_combos", [])
    return []

def save_session(done_combos):
    with open(SESSION_FILE, "w") as f:
        json.dump({"done_combos": done_combos}, f)

def get_driver(use_proxy=False):
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")

    if use_proxy:
        proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
        options.add_argument(f"--proxy-server={proxy_url}")

    driver = uc.Chrome(options=options, headless=False)
    driver.__del__ = lambda self=None: None  # 🩹 Suppress WinError 6 on cleanup

    try:
        driver.get("https://api.ipify.org?format=json")
        ip = driver.find_element(By.TAG_NAME, "pre").text
        print(f"🌐 Connected! IP: {ip}")
    except Exception as e:
        print(f"❌ Could not check IP: {e}")
        try:
            driver.quit()
        except:
            pass
        raise

    return driver

def scrape_all_data():
    driver = None
    try:
        print("🚀 Launching Chrome...")
        driver = get_driver()
        print("🌐 Opening Train Schedule page...")
        driver.get("https://www.indianrail.gov.in/enquiry/SCHEDULE/TrainSchedule.html")
    except Exception as e:
        print(f"🔁 Retrying with proxy due to: {e}")
        try:
            driver = get_driver(use_proxy=True)
            driver.get("https://www.indianrail.gov.in/enquiry/SCHEDULE/TrainSchedule.html")
        except Exception as e2:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            err_ss = os.path.join(ERROR_SCREENSHOT_DIR, f"launch_error_{ts}.png")
            if driver:
                try:
                    driver.save_screenshot(err_ss)
                    driver.quit()
                except:
                    pass
            print(f"❌ Proxy also failed: {e2}")
            print(f"🖼️ Screenshot saved to: {err_ss}")
            return

    wait = WebDriverWait(driver, 10)
    time.sleep(2)

    try:
        train_input = wait.until(EC.presence_of_element_located((By.ID, "trainNo")))
    except:
        print("❌ Input field not found. Exiting.")
        try:
            driver.quit()
        except:
            pass
        return

    all_results = {}  # train_number: train_name
    new_entries = {}  # to log newly added train data
    done_combos = load_session()

    old_train_data = {}
    if os.path.exists(TRAINS_JSON):
        try:
            with open(TRAINS_JSON, "r", encoding="utf-8") as f:
                existing = json.load(f)
                for item in existing:
                    old_train_data[item["train_number"]] = item["train_name"]
        except:
            pass

    progress_bar = tqdm(ALL_COMBOS, desc="🚂 Progress", unit="combo", dynamic_ncols=True)

    for combo in progress_bar:
        if combo in done_combos:
            continue
        try:
            train_input.clear()
            train_input.send_keys(combo)
            time.sleep(2)

            dropdown = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ui-autocomplete")))
            li_elements = dropdown.find_elements(By.TAG_NAME, "li")

            for li in li_elements:
                txt = li.text.strip()
                if " - " in txt:
                    num, name = txt.split(" - ", 1)
                    if num.strip() not in all_results:
                        new_entries[num.strip()] = name.strip()
                    all_results[num.strip()] = name.strip()

            done_combos.append(combo)
            save_session(done_combos)
            progress_bar.set_postfix(current=combo, total_found=len(all_results))

        except Exception:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            err_ss = os.path.join(ERROR_SCREENSHOT_DIR, f"error_{combo}_{ts}.png")
            try:
                driver.save_screenshot(err_ss)
            except:
                pass
            print(f"⚠️ Error on {combo}, screenshot saved: {err_ss}")
            continue

    try:
        driver.quit()
    except:
        pass

    # Prepare result list
    result_list = [{"train_number": n, "train_name": name} for n, name in sorted(all_results.items())]

    # Backup old file
    if os.path.exists(TRAINS_JSON):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(TRAINS_JSON, os.path.join(BACKUP_DIR, f"trains_backup_{ts}.json"))

    # Save updated trains list
    with open(TRAINS_JSON, "w", encoding="utf-8") as f:
        json.dump(result_list, f, indent=2, ensure_ascii=False)

    # Save new trains
    if new_entries:
        with open(NEW_JSON, "w", encoding="utf-8") as f:
            json.dump([{"train_number": k, "train_name": v} for k, v in new_entries.items()], f, indent=2, ensure_ascii=False)

    # Save removed trains
    removed_entries = {k: v for k, v in old_train_data.items() if k not in all_results}
    if removed_entries:
        with open(REMOVED_JSON, "w", encoding="utf-8") as f:
            json.dump([{"train_number": k, "train_name": v} for k, v in removed_entries.items()], f, indent=2, ensure_ascii=False)

    # Console summary
    print("\n✅ Scraping Summary:")
    print(f"🟢 Total active trains: {len(result_list)}")
    if new_entries:
        print(f"🆕 New trains detected: {len(new_entries)} saved to {NEW_JSON}")
    if removed_entries:
        print(f"🗑️ Retired trains detected: {len(removed_entries)} saved to {REMOVED_JSON}")
    print(f"📄 Updated train list saved to {TRAINS_JSON}")

if __name__ == "__main__":
    scrape_all_data()