# backend/alert.py
import requests

BOT_TOKEN = "7533379152:AAGu7a6yP6Q163WKmH73UUNexORXaH37Or8"
CHAT_ID = "1730471395"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        print(response.text)  # Optional: helps debug
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Telegram alert failed: {e}")
