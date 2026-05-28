"""ASX Analyzer - Core capabilities for ASX stock data analysis and visualization.
Built by Grok for the ASX Project.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime


class ASXAnalyzer:
    """Main class for fetching, analyzing, and visualizing ASX stocks."""

    def __init__(self, ticker: str):
        self.ticker = self._format_ticker(ticker)
        self.data: pd.DataFrame | None = None
        self.info: dict | None = None

    def _format_ticker(self, ticker: str) -> str:
        ticker = ticker.upper().strip()
        if not ticker.endswith(".AX"):
            ticker += ".AX"
        return ticker

    def fetch_data(self, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """Fetch historical price data from Yahoo Finance."""
        try:
            stock = yf.Ticker(self.ticker)
            self.data = stock.history(period=period, interval=interval)
            self.info = stock.info
            if self.data.empty:
                raise ValueError(f"No data found for {self.ticker}")
            print(f"Fetched {len(self.data)} rows for {self.ticker}")
            return self.data
        except Exception as e:
            print(f"Error fetching data: {e}")
            raise

    def add_indicators(self) -> pd.DataFrame:
        """Add common technical indicators to the dataframe."""
        if self.data is None or self.data.empty:
            raise ValueError("No data loaded. Call fetch_data() first.")

        df = self.data.copy()

        # Simple Moving Averages
        df["SMA_20"] = df["Close"].rolling(window=20).mean()
        df["SMA_50"] = df["Close"].rolling(window=50).mean()
        df["SMA_200"] = df["Close"].rolling(window=200).mean()

        # Exponential Moving Averages
        df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()
        df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()

        # MACD
        df["MACD"] = df["EMA_12"] - df["EMA_26"]
        df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
        df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]

        # RSI (14-period)
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))

        # Bollinger Bands (20, 2 std)
        sma20 = df["Close"].rolling(window=20).mean()
        std20 = df["Close"].rolling(window=20).std()
        df["BB_Upper"] = sma20 + (std20 * 2)
        df["BB_Lower"] = sma20 - (std20 * 2)
        df["BB_Middle"] = sma20

        # Average True Range (ATR 14)
        high_low = df["High"] - df["Low"]
        high_close = np.abs(df["High"] - df["Close"].shift())
        low_close = np.abs(df["Low"] - df["Close"].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df["ATR"] = true_range.rolling(14).mean()

        self.data = df
        return df

    def plot(self, show_volume: bool = True) -> go.Figure:
        """Create interactive Plotly candlestick chart with indicators."""
        if self.data is None or self.data.empty:
            raise ValueError("No data to plot.")

        df = self.data

        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.6, 0.2, 0.2],
            subplot_titles=(f"{self.ticker} Price & Indicators", "Volume", "RSI / MACD")
        )

        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Price"
            ),
            row=1, col=1
        )

        # Moving Averages
        if "SMA_20" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"], line=dict(color="blue", width=1), name="SMA 20"), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], line=dict(color="orange", width=1), name="SMA 50"), row=1, col=1)

        # Bollinger Bands
        if "BB_Upper" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["BB_Upper"], line=dict(color="gray", width=1, dash="dash"), name="BB Upper"), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df["BB_Lower"], line=dict(color="gray", width=1, dash="dash"), name="BB Lower"), row=1, col=1)

        # Volume
        if show_volume and "Volume" in df.columns:
            colors = ["green" if c >= o else "red" for c, o in zip(df["Close"], df["Open"])]
            fig.add_trace(
                go.Bar(x=df.index, y=df["Volume"], marker_color=colors, name="Volume", opacity=0.6),
                row=2, col=1
            )

        # RSI
        if "RSI" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], line=dict(color="purple", width=1.5), name="RSI (14)"), row=3, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

        # MACD
        if "MACD" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], line=dict(color="blue", width=1), name="MACD"), row=3, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df["MACD_Signal"], line=dict(color="orange", width=1), name="Signal"), row=3, col=1)

        fig.update_layout(
            title=f"{self.ticker} - ASX Technical Analysis ({datetime.now().strftime('%Y-%m-%d')})",
            xaxis_rangeslider_visible=False,
            height=900,
            showlegend=True,
            template="plotly_white"
        )
        fig.update_yaxes(title_text="Price (AUD)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_yaxes(title_text="RSI / MACD", row=3, col=1)

        return fig

    def get_latest_price(self) -> float:
        """Get the most recent closing price."""
        if self.data is None or self.data.empty:
            self.fetch_data(period="5d")
        return float(self.data["Close"].iloc[-1])

    def summary(self) -> dict:
        """Return key statistics and latest indicators."""
        if self.data is None or self.data.empty:
            self.fetch_data()
        latest = self.data.iloc[-1]
        return {
            "ticker": self.ticker,
            "latest_close": round(latest["Close"], 2),
            "change_pct": round(((latest["Close"] - self.data["Close"].iloc[-2]) / self.data["Close"].iloc[-2] * 100), 2) if len(self.data) > 1 else 0,
            "rsi": round(latest.get("RSI", 0), 1),
            "sma_20": round(latest.get("SMA_20", 0), 2),
            "volume": int(latest.get("Volume", 0)),
        }


if __name__ == "__main__":
    # Demo
    analyzer = ASXAnalyzer("BHP")
    analyzer.fetch_data("3mo")
    analyzer.add_indicators()
    print(analyzer.summary())
    fig = analyzer.plot()
    fig.write_html("bhp_chart.html")
    print("Chart saved to bhp_chart.html - open in browser!")
