import yfinance as yf
import time
import os

def check_market():
    # List of coins you want to monitor at once
    Coins = ("BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "DOGE-USD")
    
    print("=== crypto market healt dasbord ===")

    try:
        while True:
            # Clean up the terminal screen to look like a fixed dashboard
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"update time: {time.strftime('%H:%M:%S')}")
            print("-"* 50)
            print(f"{'SYMBOL':<10} | {'PRICE':<12} | {'24h VOL'}")
            print("-"*50)

            for symbol in Coins:
                ticker = yf.Ticker(symbol)
                info = ticker.fast_info
                price = info['last_price']
                vol = info['last_volume']

                print(f"{symbol:<10} | ${price:<11.2f} | {vol:.0f}")
            
            print("-"*50)
            print("press Ctrl+C to exit")
            time.sleep(15)

    except KeyboardInterrupt:
        print("\nDashnord cloded.")
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    check_market()        