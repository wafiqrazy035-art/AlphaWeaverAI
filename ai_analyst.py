import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class GeminiAnalyst:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        # PERBAIKAN: Menggunakan model yang terbukti ada di daftar 'cek_model.py' kamu
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.api_key}"

    def get_advice(self, price, change):
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Bitcoin price is Rp{price:,}, change {change}%. Berikan saran singkat BUY/SELL/HOLD dalam Bahasa Indonesia (max 15 kata)."
                }]
            }]
        }
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(self.url, headers=headers, data=json.dumps(payload))
            data = response.json()
            
            if 'error' in data:
                return f"Google Error: {data['error']['message']}"
                
            return data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"System Error: {e}"

if __name__ == "__main__":
    analyst = GeminiAnalyst()
    print("=== Menghubungkan ke Gemini Flash (Stable Version) ===")
    
    # Tes dengan harga simulasi
    hasil = analyst.get_advice(1470000000, 2.5)
    print(f"Saran Gemini: {hasil}")