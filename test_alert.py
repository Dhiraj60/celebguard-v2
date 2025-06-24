from backend.alert import send_telegram_alert

try:
    print("[🔧] Sending test alert...")
    send_telegram_alert("🔔 Test Alert: This is a manual alert test.")
    print("✅ Alert sent successfully.")
except Exception as e:
    print(f"❌ Failed to send alert: {e}")
