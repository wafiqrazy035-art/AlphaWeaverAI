import requests

class DiscordNotifier:
    def __init__(self):
        # GANTI URL DI BAWAH dengan Webhook URL dari Discord kamu
        self.webhook_url = "https://discord.com/api/webhooks/1455436201644527657/jYnpBlepwwcOhTGrmDWeaKNf9yZI7Q7FQPQPsMsz1nhqVDCKC7O5SVReZiEBa-5ACKfn"

    def send_notification(self, pesan):
        data = {
            "username": "AI Trading Bot Monitor",
            "content": pesan
        }
        try:
            requests.post(self.webhook_url, json=data)
        except Exception as e:
            print(f"Gagal kirim notifikasi: {e}")