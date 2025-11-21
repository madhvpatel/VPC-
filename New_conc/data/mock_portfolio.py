"""
Mock portfolio data with stock and mutual fund holdings
"""

import pandas as pd
from datetime import datetime, timedelta

# Stock holdings
STOCK_HOLDINGS = pd.DataFrame([
    {
        "ticker": "AAPL",
        "company": "Apple Inc.",
        "quantity": 50,
        "purchase_price": 150.25,
        "purchase_date": "2023-08-15",
        "sector": "Technology"
    },
    {
        "ticker": "MSFT",
        "company": "Microsoft Corporation",
        "quantity": 30,
        "purchase_price": 320.50,
        "purchase_date": "2023-09-22",
        "sector": "Technology"
    },
    {
        "ticker": "GOOGL",
        "company": "Alphabet Inc.",
        "quantity": 25,
        "purchase_price": 125.75,
        "purchase_date": "2024-01-10",
        "sector": "Technology"
    },
    {
        "ticker": "JNJ",
        "company": "Johnson & Johnson",
        "quantity": 40,
        "purchase_price": 155.00,
        "purchase_date": "2023-11-05",
        "sector": "Healthcare"
    },
    {
        "ticker": "V",
        "company": "Visa Inc.",
        "quantity": 20,
        "purchase_price": 245.30,
        "purchase_date": "2024-03-18",
        "sector": "Financial Services"
    },
    {
        "ticker": "TSLA",
        "company": "Tesla Inc.",
        "quantity": 15,
        "purchase_price": 245.60,
        "purchase_date": "2023-10-12",
        "sector": "Automotive"
    },
])

# Mutual fund holdings
MUTUAL_FUND_HOLDINGS = pd.DataFrame([
    {
        "fund_name": "Vanguard Total Stock Market Index",
        "ticker": "VTSAX",
        "units": 180,
        "purchase_nav": 110.50,
        "purchase_date": "2023-07-01",
        "category": "Large Cap Blend"
    },
    {
        "fund_name": "Fidelity 500 Index Fund",
        "ticker": "FXAIX",
        "units": 120,
        "purchase_nav": 165.25,
        "purchase_date": "2023-08-15",
        "category": "Large Cap Blend"
    },
    {
        "fund_name": "Vanguard Emerging Markets Stock Index",
        "ticker": "VEIEX",
        "units": 95,
        "purchase_nav": 32.80,
        "purchase_date": "2024-02-20",
        "category": "Diversified Emerging Markets"
    },
])

# Cash position
CASH_POSITION = {
    "savings_account": 25000,
    "checking_account": 5500,
    "emergency_fund": 30000
}

def get_portfolio_summary():
    """Returns a summary of the entire portfolio"""
    return {
        "stocks": STOCK_HOLDINGS,
        "mutual_funds": MUTUAL_FUND_HOLDINGS,
        "cash": CASH_POSITION
    }
