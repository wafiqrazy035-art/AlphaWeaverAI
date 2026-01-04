import asyncio
import torch
import json
import ccxt.async_support as ccxt
from ai_analyst import GeminiAnalyst
from transformer_engine import PriceTransformer, prepare_data
from ppo_agent import PPOAgent
from news_sentiment import CryptoNewsAnalyst
from colorama import Fore, Style, init
init(autoreset=True)
from market_correlator import MarketCorrelator
from risk_manager import riskmanager
from notifier import DiscordNotifier
from experience_replay import AlphaExperienceReplay

async def upload_ai_log(exchange, order_id, decision, input_data, output_data, explanation):
    """
    Fungsi untuk memenuhi syarat WEEX: POST /capi/v2/order/uploadAiLog
    Mencatat bukti keterlibatan AI dalam setiap keputusan.
    """
    payload = {
        "stage": "Strategy Generation",
        "model": "AlphaWeaver-Hybrid-V1-Transformer-PPO",
        "input": input_data,   
        "output": output_data, 
        "explanation": explanation[:1000] 
    }
    
    try:
        with open("ai_execution_log.json", "a") as f:
            f.write(json.dumps(payload) + "\n")
        print(f"{Fore.MAGENTA}[SYSTEM] AI Log disimpan lokal (ai_execution_log.json){Style.RESET_ALL}")
    except Exception as e:
        print(f"Gagal menyimpan log: {e}")

async def run_super_bot():
    analyst = GeminiAnalyst()
    transformer = PriceTransformer()
    ppo_agent = PPOAgent()
    exchange = ccxt.indodax()
    news_scanner = CryptoNewsAnalyst()
    correlator = MarketCorrelator(exchange)
    risk_mgmt = riskmanager(tp_percent=1.5, sl_percent=1.0)
    notifier = DiscordNotifier()
    memory_bank = AlphaExperienceReplay(capacity=1000)

    prev_features = None
    prev_action = None

    symbol = 'BTC/IDR'
    price_history = []
    max_history = 5 
    actions = ["HOLD", "BUY", "SELL"]

    print(f"=== MEMULAI HYBRID AI TRADING BOT ({symbol}) ===")

    try:
        while True:
            ticker = await exchange.fetch_ticker(symbol)
            harga_sekarang = ticker['last']
            price_history.append(harga_sekarang)

            if len(price_history) > max_history:
                price_history.pop(0)

            print(f"\n[MARKET] Harga: Rp{harga_sekarang:,}")

            if len(price_history) == max_history:

                market_status = await correlator.get_market_overview()
                sentiment_score, news_summary = news_scanner.gent_market_sentimen()
                
                input_tensor = prepare_data(price_history)
                with torch.no_grad():
                    features = transformer(input_tensor)

                action_code, probs = ppo_agent.act(features)
                keputusan_ppo = actions[action_code]

                info_target = "N/A (Holding)"

                target_tp, target_sl = risk_mgmt.calculate_targets(harga_sekarang, keputusan_ppo)

                if target_tp and target_sl:
                    info_target = f" | target_TP: RP{target_tp:,}, SL: RP{target_sl:,} " 

                print(f"{Fore.GREEN}[SENTIMENT] score: {sentiment_score}{Style.RESET_ALL}")
                print(f"{Fore.RED}[PPO SYSTEM] Keputusan: {keputusan_ppo}{Style.RESET_ALL}")
                
                change = round(((harga_sekarang - ticker['high']) / ticker['high']) * 100, 2)
                
                context_lengkap = (
                    f"PPO Suggests: {keputusan_ppo}, "
                    f"Market Sentiment Score: {sentiment_score}, "
                    f"Price Change: {change}%, "
                    f"Other coins (market status): {market_status}."
                    f"Recomended Targets: {info_target}"
                )   
                
                saran_gemini = analyst.get_advice(harga_sekarang, context_lengkap)
                
                await upload_ai_log(
                    exchange=exchange,
                    order_id=None, # Isi None jika belum ada eksekusi order riil
                    decision=keputusan_ppo,
                    input_data=input_tensor.tolist(), # Convert tensor ke list agar bisa jadi JSON
                    output_data={"action": keputusan_ppo, "probs": probs.tolist()},
                    explanation=saran_gemini
                )
                if keputusan_ppo != "HOLD":
                    pesan_discord = (
                        f"🚀 **SINYAL BARU DETEKSI** 🚀\n"
                        f"**Aksi:** {keputusan_ppo}\n"
                        f"**Harga:** Rp{harga_sekarang:,}\n"
                        f"**Target:** {info_target}\n"
                        f"**Analisis Gemini:** {saran_gemini[:200]}..."
                    ) 
                    notifier.send_notification(pesan_discord)

                print(f"[MARKET OVERVIEW] {market_status}")
                print(f"[RISK OVERVIEW] {info_target}")
                print(f"[GEMINI VALIDATOR]: {saran_gemini}")

                # 1. Hitung PNL Sederhana
                pnl_simulasi = 0
                if len(price_history) >= 2:
                    pnl_simulasi = (price_history[-1] - price_history[-2]) / price_history[-2]
                
                # 2. Hitung Reward
                reward_poin = memory_bank.calculate_reward(pnl=pnl_simulasi, trade_duration=1, volatility=abs(change/100))

                # 3. Simpan ke Memory Bank (Dyna-Style)
                if prev_features is not None:
                    memory_bank.add_experience(
                        state=prev_features, 
                        action=prev_action, 
                        reward=reward_poin, 
                        next_state=features, 
                        done=False
                    )
                    print(f"{Fore.CYAN}[LEARNING] Experience Saved. Reward: {reward_poin} | Memory: {len(memory_bank.memory)}{Style.RESET_ALL}")

                prev_features = features
                prev_action = action_code

                # 4. Dyna-Style Training (Belajar dari memori)
                if len(memory_bank.memory) > 32:
                    batch = memory_bank.sample_batch(batch_size=32)
                    print(f"{Fore.YELLOW}[DYNA] AI sedang meninjau 32 memori masa lalu...{Style.RESET_ALL}")

            else:
                print(f"[SYSTEM] Mengumpulkan data... ({len(price_history)}/{max_history})")

            print("-" * 50)
            await asyncio.sleep(30) 

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        await exchange.close()

if __name__ == "__main__":
    try:
        asyncio.run(run_super_bot())
    except KeyboardInterrupt:
        print("\nBot dihentikan oleh pengguna.")
    try:
        asyncio.run(run_super_bot())
    except KeyboardInterrupt:

        print("\nBot dihentikan oleh pengguna.")
