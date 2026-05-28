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
pip install -e .
```

This installs the package in editable mode so you get the clean `from asx_analyzer import ASXAnalyzer` import. Requirements are pulled automatically from `pyproject.toml`.

You can still use `pip install -r requirements.txt` if you prefer the old way (then use `PYTHONPATH=src`).

## Quick Start

```bash
# Install in editable mode (recommended)
pip install -e .
```

Then use the clean import:

```python
from asx_analyzer import ASXAnalyzer

analyzer = ASXAnalyzer("BHP")  # BHP Billiton
analyzer.fetch_data(period="6mo")
analyzer.add_indicators()
fig = analyzer.plot()
fig.show()
```

If you prefer to run without installing, you can also do:

```bash
PYTHONPATH=src python your_script.py
```

See `examples/` for more scripts.

## Project Structure

```
asx-project/
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/
│   ├── __init__.py
│   └── asx_analyzer.py
├── examples/
│   └── portfolio_example.py
└── data/
    └── sample_asx_stocks.csv
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
