import os
from pathlib import Path

import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message, photo_path=None):
    try:
        if not TELEGRAM_TOKEN or not CHAT_ID:
            print("⚠️ Telegram não configurado. Defina TELEGRAM_TOKEN e TELEGRAM_CHAT_ID.")
            return

        if photo_path:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {'chat_id': CHAT_ID, 'caption': message, 'parse_mode': 'Markdown'}
                requests.post(url, files=files, data=data)
        else:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
            requests.post(url, data=data)
        print("📲 Notificação enviada ao Telegram!")
    except Exception as e:
        print(f"❌ Erro ao enviar Telegram: {e}")
