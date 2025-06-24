import os
import sys
from datetime import datetime

# Add project root to import paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

from backend.db import load_contracts
from backend.scraper import check_content_live
from backend.alert import send_telegram_alert

def check_expired_contracts():
    contracts = load_contracts()
    print(f"[🕒] Loaded {len(contracts)} contract(s)")

    for c in contracts:
        expiry_date = datetime.strptime(c["expiry_date"], "%Y-%m-%d")
        if expiry_date < datetime.now():
            print(f"[⏰] Expired: {c['brand_name']} for {c['client_name']}")
            is_live = check_content_live(c["content_link"])

            if is_live:
                print("🚨 Still live. Sending alert...")
                try:
                    send_telegram_alert(f"⚠️ ALERT: {c['client_name']} - {c['brand_name']} content is still live after contract expiry!\nLink: {c['content_link']}")
                    print("✅ Telegram alert sent")
                except Exception as e:
                    print(f"❌ Failed to send alert: {e}")
            else:
                print("✅ Content is no longer live")

if __name__ == "__main__":
    check_expired_contracts()
