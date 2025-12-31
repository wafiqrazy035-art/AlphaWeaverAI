import yfinance as yf
import pandas as pd
import time
import os
from datetime import datetime

def start_logging():
    coins = ("BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "DOGE-USD")
    file_name = "crypto_market_data.csv"

    print(f"=== market logger started ===")
    print(f"Data will be saved to: {file_name}")

    try:
        while True:
            log_data = []
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            for symbol in coins:
                ticker = yf.Ticker(symbol)
                info = ticker.fast_info

                row = {
                    "timestamp": current_time,
                    "symbol": symbol,
                    "price": info ['last_price'],
                    "volume": info ['last_volume']
                }
                log_data.append(row)

            df = pd.DataFrame(log_data)

            if not os.path.isfile(file_name):
                df.to_csv(file_name, index=False)
            else:
                df.to_csv(file_name, mode='a', header=False, index=False)

            print(f"[{current_time}] Data successfully recorded to Excel/CSV.")

            time.sleep(60)
    except KeyboardInterrupt:
        print("\nLogging stopped by user.")
    except Exception as e:
        print(f"Eroor: {e}")

if __name__ == "__main__":
    start_logging()
                                                             
