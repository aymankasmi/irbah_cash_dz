import requests

url = "https://api.telegram.org"
try:
    response = requests.get(url)
    print("✅ اتصال ناجح بـ Telegram API")
except Exception as e:
    print("❌ فشل الاتصال:", e)
