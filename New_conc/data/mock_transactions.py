"""
Mock transaction history data
"""

import pandas as pd
from datetime import datetime, timedelta
import random

# Generate realistic transaction data for the past 90 days
def generate_transactions():
    """Generate mock transaction data"""
    
    transactions = []
    current_date = datetime.now()
    
    # Transaction templates
    transaction_templates = [
        # Groceries
        {"category": "Groceries", "merchants": ["Whole Foods", "Trader Joe's", "Safeway", "Kroger"], "amount_range": (45, 180)},
        # Dining
        {"category": "Dining", "merchants": ["Chipotle", "Starbucks", "Panera Bread", "Local Restaurant"], "amount_range": (12, 85)},
        # Entertainment
        {"category": "Entertainment", "merchants": ["Netflix", "Spotify", "AMC Theaters", "Concert Tickets"], "amount_range": (15, 120)},
        # Transportation
        {"category": "Transportation", "merchants": ["Shell Gas", "Uber", "Public Transit", "Parking"], "amount_range": (8, 65)},
        # Utilities
        {"category": "Utilities", "merchants": ["Electric Company", "Water Utility", "Internet Provider", "Gas Company"], "amount_range": (45, 150)},
        # Shopping
        {"category": "Shopping", "merchants": ["Amazon", "Target", "Best Buy", "Nike"], "amount_range": (25, 250)},
        # Healthcare
        {"category": "Healthcare", "merchants": ["CVS Pharmacy", "Doctor Visit", "Gym Membership"], "amount_range": (20, 200)},
    ]
    
    # Generate transactions for past 90 days
    for day_offset in range(90):
        transaction_date = current_date - timedelta(days=day_offset)
        
        # 2-5 transactions per day
        num_transactions = random.randint(2, 5)
        
        for _ in range(num_transactions):
            template = random.choice(transaction_templates)
            merchant = random.choice(template["merchants"])
            amount = round(random.uniform(*template["amount_range"]), 2)
            
            transactions.append({
                "date": transaction_date.strftime("%Y-%m-%d"),
                "category": template["category"],
                "merchant": merchant,
                "amount": -amount,  # Negative for expenses
                "type": "debit"
            })
    
    # Add monthly salary deposits
    for month_offset in range(3):
        salary_date = current_date - timedelta(days=30 * month_offset)
        transactions.append({
            "date": salary_date.strftime("%Y-%m-%d"),
            "category": "Income",
            "merchant": "Direct Deposit - Salary",
            "amount": 8500,
            "type": "credit"
        })
    
    # Add some investment purchases
    investment_transactions = [
        {"date": (current_date - timedelta(days=15)).strftime("%Y-%m-%d"), 
         "category": "Investment", "merchant": "Stock Purchase - AAPL", "amount": -1500, "type": "investment"},
        {"date": (current_date - timedelta(days=45)).strftime("%Y-%m-%d"), 
         "category": "Investment", "merchant": "Mutual Fund - VTSAX", "amount": -2000, "type": "investment"},
        {"date": (current_date - timedelta(days=60)).strftime("%Y-%m-%d"), 
         "category": "Investment", "merchant": "Stock Purchase - MSFT", "amount": -1000, "type": "investment"},
    ]
    
    transactions.extend(investment_transactions)
    
    # Convert to DataFrame and sort by date
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date', ascending=False)
    
    return df

# Generate the transactions
TRANSACTION_HISTORY = generate_transactions()

def get_transactions_by_category(category=None, days=30):
    """Get transactions filtered by category and date range"""
    df = TRANSACTION_HISTORY.copy()
    
    # Filter by date
    cutoff_date = datetime.now() - timedelta(days=days)
    df = df[df['date'] >= cutoff_date]
    
    # Filter by category if provided
    if category:
        df = df[df['category'] == category]
    
    return df

def get_spending_summary(days=30):
    """Get spending summary by category"""
    df = get_transactions_by_category(days=days)
    
    # Only expenses (negative amounts)
    expenses = df[df['amount'] < 0].copy()
    expenses['amount'] = expenses['amount'].abs()
    
    summary = expenses.groupby('category')['amount'].agg(['sum', 'count', 'mean']).round(2)
    summary.columns = ['total_spent', 'num_transactions', 'avg_transaction']
    
    return summary.sort_values('total_spent', ascending=False)
