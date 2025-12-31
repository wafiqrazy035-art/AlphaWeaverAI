import yfinance as yf
import time

def cek_harga():
    print("=== Crypto/Stock Price Tracker ===")
    simbol = input("Masukkan simbol (contoh: BTC-USD atau AAPL): ").upper()

    if not simbol:
        print("Simbol tidak boleh kosong!")
        return

    
    print(f"\nMemantau harga unutuk{simbol}..." )

    try:
        while True:
            # Retrieves the latest data
            ticker_data = yf.Ticker(simbol)
            info = ticker_data.fast_info
            harga_sekarang = info['last_price']
            # Displays prices with current time
            waktu= time.strftime("%H:%M:%S")
            print(f"[{waktu}]harga {simbol}: {harga_sekarang:.2f}")

            # Wait 5 seconds before checking again (and can be changed again as desired)
            time.sleep(5)

    except KeyboardInterrupt:
        print(f"\npemantauan di hentikan oleh user.")           
    except Exception as e:
        print(f"terjadi kesalahan:{e}")

if __name__=="__main__":
    cek_harga()       