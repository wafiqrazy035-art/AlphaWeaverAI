import asyncio
import ccxt.async_support as ccxt

async def market_pro():
    exchange = ccxt.indodax()
    symbol = 'BTC/IDR'

    print(f"=== Memulai Market Pro: {symbol} ===")
    
    try:
        while True:
            ticker = await exchange.fetch_ticker(symbol)
            harga = ticker['last']
            high = ticker['high']
            
            print(f"[{symbol}] Harga: Rp{harga:,} | High 24j: Rp{high:,}")
            
            await asyncio.sleep(0.5)

    except Exception as e:
        print(f"\nAda masalah koneksi: {e}")
    finally:
        await exchange.close()

if __name__ == "__main__":
    try:
        asyncio.run(market_pro())
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")