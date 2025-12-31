import os
import requests
import json
from ai_analyst import GeminiAnalyst

class CryptoNewsAnalyst:
    def __init__(self):
        self.analist =  GeminiAnalyst()
        self.news_url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"

    def gent_market_sentimen(self):
        try:
            response = requests.get(self.news_url)
            news_data = response.json()['Data'][:3]

            combined_news = ""
            for article in news_data:
                combined_news += f"- {article['title']}: {article['body'][:100]}...\n"

            prompt = f"""
            Analisis sentimen pasar Crypto dari berita berikut:
            {combined_news}
            
            Berikan skor angka saja antara -1.0 (sangat negatif) sampai 1.0 (sangat positif).
            Contoh output: 0.5
            """
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }

            res = requests.post(self.analist.url, json=payload)
            score_text = res.json()['candidates'][0]['content']['parts'][0]['text']

            sentiment_score = float(''.join(c for c in score_text if c in '0123456789.-'))
            return sentiment_score, combined_news
        
        except Exception as e:
            print(f"Error news: {e}")
            return 0.0, "no news anvailable"
        
if __name__ == "__main__":
    scanner = CryptoNewsAnalyst()
    score, news = scanner.gent_market_sentimen
    print(f"=== sentimen berita: {score} ===")
    print(news)
