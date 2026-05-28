"""Example: Simple ASX Portfolio Tracker using the analyzer.
"""

from src.asx_analyzer import ASXAnalyzer
import pandas as pd


def track_portfolio(holdings: dict):
    """holdings = {'BHP': 100, 'RIO': 50, 'CSL': 20}  # shares owned"""
    portfolio_data = []
    total_value = 0.0

    for ticker, shares in holdings.items():
        analyzer = ASXAnalyzer(ticker)
        analyzer.fetch_data(period="1mo")
        price = analyzer.get_latest_price()
        value = price * shares
        total_value += value
        portfolio_data.append({
            "Ticker": ticker + ".AX",
            "Shares": shares,
            "Latest Price (AUD)": round(price, 2),
            "Value (AUD)": round(value, 2),
            "Weight %": 0  # will calculate later
        })

    df = pd.DataFrame(portfolio_data)
    df["Weight %"] = round(df["Value (AUD)"] / total_value * 100, 1)
    print("\n=== ASX Portfolio Summary ===")
    print(df.to_string(index=False))
    print(f"\nTotal Portfolio Value: AUD ${total_value:,.2f}")
    return df


if __name__ == "__main__":
    my_holdings = {
        "BHP": 250,
        "RIO": 80,
        "WBC": 150,
        "CSL": 30
    }
    track_portfolio(my_holdings)
