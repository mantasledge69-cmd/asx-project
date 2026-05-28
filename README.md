# ASX Project

**Grok-built Python toolkit for Australian Securities Exchange (ASX) stock analysis, data fetching, technical indicators, portfolio tracking, and interactive visualizations.**

## Features / Capabilities

- **Data Fetching**: Download historical and real-time (delayed) stock data for any ASX-listed company using Yahoo Finance (`.AX` tickers).
- **Technical Analysis**: Calculate popular indicators including SMA, EMA, RSI, MACD, Bollinger Bands, ATR.
- **Interactive Charts**: Plot candlestick charts with volume, overlays, and subplots using Plotly.
- **Portfolio Tracker**: Simple portfolio performance calculation, returns, and allocation.
- **Screening**: Basic stock screener example (e.g., RSI < 30 for oversold).
- **News & Events**: Fetch recent company news (via yfinance).
- **Export**: Save data to CSV/Excel for further analysis.

Built with ❤️ by Grok for the Australian market. Perfect for retail investors, analysts, or anyone working with ASX data.

## Installation

```bash
git clone https://github.com/mantasledge69-cmd/asx-project.git
cd asx-project
pip install -r requirements.txt
```

## Quick Start

```python
from src.asx_analyzer import ASXAnalyzer

analyzer = ASXAnalyzer("BHP")  # BHP Billiton
analyzer.fetch_data(period="6mo")
analyzer.add_indicators()
fig = analyzer.plot()
fig.show()
```

See `examples/` for more scripts.

## Project Structure

```
asx-project/
├── README.md
├── requirements.txt
├── src/
│   └── asx_analyzer.py
├── examples/
│   └── portfolio_example.py
└── data/
    └── sample_data.csv (optional)
```

## Disclaimer
This is for educational and personal use only. Not financial advice. Always do your own research. ASX data is delayed; for live trading use official sources.

## Future Capabilities (Roadmap)
- Integration with ASX official API / CHESS-related data simulation
- Machine learning price prediction models
- Real-time WebSocket alerts
- Dashboard with Streamlit or Dash
- Options chain analysis for ASX derivatives

Contributions welcome! Open an issue or PR.
