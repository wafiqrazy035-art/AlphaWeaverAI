import requests
import os

class DiscordNotifier:
    def __init__(self):
        # GANTI URL DI BAWAH dengan Webhook URL dari Discord kamu
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def send_notification(self, pesan):
        data = {
            "username": "AI Trading Bot Monitor",
            "content": pesan
        }
        try:
            requests.post(self.webhook_url, json=data)
        except Exception as e:
            print(f"Gagal kirim notifikasi: {e}")
