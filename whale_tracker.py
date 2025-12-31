import yfinance as yf
import time

def monitor_whale():
    simbol = input("Enter the coin symbol to track (example: BTC-USD):").upper()
    volume_threshold = 500

    print(f"=== Getting Started with Whale Tracker for {simbol} ===")

    try:
        ticker_obj=yf.Ticker(simbol)

        while True:
            # Get the latest data from yfinance
            data= ticker_obj.fast_info
            current_volume = data['last_volume']
            price = data['last_price']


        # Simple logic: If the volume is very high, mark it as Whale activity
            if current_volume > volume_threshold:
                print(f"!!! WHALE WARNING: Large volume detected: {current_volume:.0f}")
                print(f"Current price: ${price:.2f}")
            else:
                print(f"Monitoring... Current volume: {current_volume:.0f} | Price: ${price:.2f}")
        
            time.sleep(10)

    except KeyboardInterrupt:
        print(f"\nmonitoring is stopped by the user.")
    except Exception as e:
      print(f"There is an error: {e}")

if __name__ == "__main__":
    monitor_whale()
