# 🤖 AlphaWeaver AI: Hybrid Transformer & Reinforcement Learning Agent

AlphaWeaver AI is an advanced cryptocurrency trading system that integrates the power of **Deep Learning** and **Reinforcement Learning** for intelligent, autonomous trade execution in volatile markets.

## 🌟 Key Features
* **Transformer-Based Price Engine:** Utilizes the `PriceTransformer` architecture (PyTorch) to extract complex time-series price patterns.
* **PPO Reinforcement Learning:** An intelligent agent that learns to make autonomous decisions (Buy/Sell/Hold) using the *Proximal Policy Optimization* algorithm.
* **LLM Multi-Modal Analysis:** Integrated with Google Gemini AI to provide natural language-based trading validation and insights.
* **Advanced Risk Management:** Automatically calculates *Take Profit* (TP) and *Stop Loss* (SL) targets to ensure capital preservation.
* **Market Insight Tools:** Features a real-time market health dashboard and cross-coin correlation tracking (`ETH`, `SOL`, `BNB`).

## 🏗️ System Architecture
The project consists of several core modules working in sync:
1.  **`main_bot.py`**: The primary orchestrator running the asynchronous trading loop.
2.  **`transformer_engine.py`**: The Deep Learning engine for market pattern recognition.
3.  **`ai_analyst.py`**: Bridge to Gemini AI for sentiment analysis and smart validation.
4.  **`risk_manager.py`**: Logic for risk calculation and trade safety.
5.  **`market_correlator.py`**: Analyzes market health through major coin comparisons.
6.  **`whale_tracker.py`**: Monitors large volume spikes to detect "whale" activity.

## 🚀 Getting Started
1.  Clone this repository.
2.  Install dependencies: `pip install torch ccxt requests pandas yfinance colorama python-dotenv`.
3.  Add your `GEMINI_API_KEY` to a `.env` file.
4.  Run the bot: `python main_bot.py`.

## 📈 Vision
To eliminate human emotional bias by providing a trading agent that possesses deep technical analytical capabilities and disciplined decision-making logic.
