import ccxt.async_support as ccxt
import asyncio

class MarketCorrelator:
    def __init__(self, exchange):
        self.exchange = exchange
        self.other_symbols = ['ETH/IDR', 'SOL/IDR', 'BNB/IDR']

    async def get_market_overview(self):
        overview = []
        try:
            for symbol in self.other_symbols:
                ticker =  await self.exchange.fetch_ticker(symbol)
                last = ticker.get('last', 0)
                open_price = ticker.get('open', 0)

                if open_price and open_price != 0:
                    change = ((last - open_price) / open_price) * 100
                else:
                    change = 0.0

                coin_name = symbol.split('/')[0]
                overview.append(f"{coin_name}: {change:+.2f}%")
            return" | ".join(overview)
        except Exception as e:
            return f"Gagal mengambil data koin lain: {str(e)}"
