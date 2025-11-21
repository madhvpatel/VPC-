"""
LangChain tools for the financial AI agent
"""

from langchain.tools import tool
from typing import Optional, Union
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Import mock data
import sys
sys.path.append('..')
from data.mock_user import USER_PROFILE
from data.mock_portfolio import STOCK_HOLDINGS, MUTUAL_FUND_HOLDINGS, CASH_POSITION
from data.mock_transactions import TRANSACTION_HISTORY, get_spending_summary, get_transactions_by_category


@tool
def analyze_portfolio(include_details: Union[bool, str] = True) -> str:
    """
    Analyzes the user's investment portfolio including stocks and mutual funds.
    Returns current values, gains/losses, and allocation percentages.
    
    Args:
        include_details: Whether to include detailed breakdown of each holding
    
    Returns:
        String with comprehensive portfolio analysis
    """
    # Handle case where agent passes JSON string instead of boolean
    if isinstance(include_details, str):
        try:
            import json
            # Try to parse as JSON object
            if '{' in include_details:
                data = json.loads(include_details)
                if isinstance(data, dict):
                    include_details = data.get('include_details', True)
            else:
                # Handle simple string "true"/"false"
                include_details = include_details.lower() == 'true'
        except:
            # Default to True if parsing fails
            include_details = True

    try:
        # Fetch current prices for stocks
        stock_data = []
        total_stock_value = 0
        total_stock_cost = 0
        
        for _, holding in STOCK_HOLDINGS.iterrows():
            ticker = holding['ticker']
            try:
                stock = yf.Ticker(ticker)
                current_price = stock.info.get('currentPrice', stock.info.get('regularMarketPrice', 0))
                
                if current_price == 0:
                    # Fallback: try to get from history
                    hist = stock.history(period='1d')
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                
                quantity = holding['quantity']
                purchase_price = holding['purchase_price']
                cost_basis = quantity * purchase_price
                current_value = quantity * current_price
                gain_loss = current_value - cost_basis
                gain_loss_pct = (gain_loss / cost_basis) * 100 if cost_basis > 0 else 0
                
                stock_data.append({
                    'ticker': ticker,
                    'company': holding['company'],
                    'quantity': quantity,
                    'purchase_price': purchase_price,
                    'current_price': current_price,
                    'cost_basis': cost_basis,
                    'current_value': current_value,
                    'gain_loss': gain_loss,
                    'gain_loss_pct': gain_loss_pct
                })
                
                total_stock_value += current_value
                total_stock_cost += cost_basis
            except Exception as e:
                # If we can't fetch price, use purchase price as estimate
                quantity = holding['quantity']
                purchase_price = holding['purchase_price']
                cost_basis = quantity * purchase_price
                
                stock_data.append({
                    'ticker': ticker,
                    'company': holding['company'],
                    'quantity': quantity,
                    'purchase_price': purchase_price,
                    'current_price': purchase_price,
                    'cost_basis': cost_basis,
                    'current_value': cost_basis,
                    'gain_loss': 0,
                    'gain_loss_pct': 0
                })
                
                total_stock_value += cost_basis
                total_stock_cost += cost_basis
        
        # Fetch current NAV for mutual funds (simplified - using yfinance)
        mf_data = []
        total_mf_value = 0
        total_mf_cost = 0
        
        for _, holding in MUTUAL_FUND_HOLDINGS.iterrows():
            ticker = holding['ticker']
            try:
                fund = yf.Ticker(ticker)
                current_nav = fund.info.get('navPrice', fund.info.get('regularMarketPrice', 0))
                
                if current_nav == 0:
                    hist = fund.history(period='1d')
                    if not hist.empty:
                        current_nav = hist['Close'].iloc[-1]
                
                units = holding['units']
                purchase_nav = holding['purchase_nav']
                cost_basis = units * purchase_nav
                current_value = units * current_nav
                gain_loss = current_value - cost_basis
                gain_loss_pct = (gain_loss / cost_basis) * 100 if cost_basis > 0 else 0
                
                mf_data.append({
                    'ticker': ticker,
                    'fund_name': holding['fund_name'],
                    'units': units,
                    'purchase_nav': purchase_nav,
                    'current_nav': current_nav,
                    'cost_basis': cost_basis,
                    'current_value': current_value,
                    'gain_loss': gain_loss,
                    'gain_loss_pct': gain_loss_pct
                })
                
                total_mf_value += current_value
                total_mf_cost += cost_basis
            except Exception as e:
                units = holding['units']
                purchase_nav = holding['purchase_nav']
                cost_basis = units * purchase_nav
                
                mf_data.append({
                    'ticker': ticker,
                    'fund_name': holding['fund_name'],
                    'units': units,
                    'purchase_nav': purchase_nav,
                    'current_nav': purchase_nav,
                    'cost_basis': cost_basis,
                    'current_value': cost_basis,
                    'gain_loss': 0,
                    'gain_loss_pct': 0
                })
                
                total_mf_value += cost_basis
                total_mf_cost += cost_basis
        
        # Calculate totals
        total_cash = sum(CASH_POSITION.values())
        total_portfolio_value = total_stock_value + total_mf_value + total_cash
        total_invested = total_stock_cost + total_mf_cost
        total_gain_loss = (total_stock_value + total_mf_value) - total_invested
        total_gain_loss_pct = (total_gain_loss / total_invested) * 100 if total_invested > 0 else 0
        
        # Build response
        response = f"""PORTFOLIO ANALYSIS (as of {datetime.now().strftime('%Y-%m-%d')}):

OVERALL SUMMARY:
- Total Portfolio Value: ${total_portfolio_value:,.2f}
- Total Invested: ${total_invested:,.2f}
- Total Cash: ${total_cash:,.2f}
- Unrealized Gain/Loss: ${total_gain_loss:,.2f} ({total_gain_loss_pct:+.2f}%)

ALLOCATION:
- Stocks: ${total_stock_value:,.2f} ({(total_stock_value/total_portfolio_value)*100:.1f}%)
- Mutual Funds: ${total_mf_value:,.2f} ({(total_mf_value/total_portfolio_value)*100:.1f}%)
- Cash: ${total_cash:,.2f} ({(total_cash/total_portfolio_value)*100:.1f}%)
"""
        
        if include_details:
            response += "\n--- STOCK HOLDINGS ---\n"
            for stock in stock_data:
                response += f"\n{stock['ticker']} - {stock['company']}\n"
                response += f"  Qty: {stock['quantity']} | Current: ${stock['current_price']:.2f} | Total Value: ${stock['current_value']:,.2f}\n"
                response += f"  Gain/Loss: ${stock['gain_loss']:,.2f} ({stock['gain_loss_pct']:+.2f}%)\n"
            
            response += "\n--- MUTUAL FUND HOLDINGS ---\n"
            for mf in mf_data:
                response += f"\n{mf['ticker']} - {mf['fund_name']}\n"
                response += f"  Units: {mf['units']} | Current NAV: ${mf['current_nav']:.2f} | Total Value: ${mf['current_value']:,.2f}\n"
                response += f"  Gain/Loss: ${mf['gain_loss']:,.2f} ({mf['gain_loss_pct']:+.2f}%)\n"
        
        return response
        
    except Exception as e:
        return f"Error analyzing portfolio: {str(e)}"


@tool
def analyze_transactions(days: Union[int, str] = 30, category: Optional[str] = None) -> str:
    """
    Analyzes transaction history to identify spending patterns and trends.
    
    Args:
        days: Number of days to analyze (default 30)
        category: Optional category to filter by (e.g., 'Groceries', 'Dining')
    
    Returns:
        String with spending analysis and insights
    """
    # Handle case where agent passes JSON string instead of int/str
    if isinstance(days, str):
        try:
            import json
            if '{' in days:
                data = json.loads(days)
                if isinstance(data, dict):
                    days = int(data.get('days', 30))
            else:
                days = int(days)
        except:
            days = 30
            
    if isinstance(category, str):
        try:
            import json
            if '{' in category:
                data = json.loads(category)
                if isinstance(data, dict):
                    category = data.get('category', None)
        except:
            pass

    try:
        # Get spending summary
        summary = get_spending_summary(days=days)
        
        # Calculate total spending
        total_spent = summary['total_spent'].sum()
        
        # Get transactions
        transactions = get_transactions_by_category(category=category, days=days)
        
        response = f"""TRANSACTION ANALYSIS (Last {days} days):

SPENDING SUMMARY:
- Total Spent: ${total_spent:,.2f}
- Number of Transactions: {summary['num_transactions'].sum():.0f}
- Average Transaction: ${summary['avg_transaction'].mean():.2f}

TOP SPENDING CATEGORIES:
"""
        
        for cat, row in summary.head(5).iterrows():
            response += f"- {cat}: ${row['total_spent']:,.2f} ({row['num_transactions']:.0f} transactions, avg ${row['avg_transaction']:.2f})\n"
        
        # Add insights
        response += "\nINSIGHTS:\n"
        
        # Check if any category is over budget
        user_budget_categories = USER_PROFILE['expenses']['categories']
        monthly_multiplier = 30 / days
        
        for cat, row in summary.iterrows():
            if cat.lower() in [k.lower() for k in user_budget_categories.keys()]:
                # Find matching budget category
                budget_cat = [k for k in user_budget_categories.keys() if k.lower() == cat.lower()][0]
                budget = user_budget_categories[budget_cat]
                projected_monthly = row['total_spent'] * monthly_multiplier
                
                if projected_monthly > budget * 1.1:  # 10% over budget
                    response += f"⚠️ {cat} spending is tracking {((projected_monthly/budget - 1) * 100):.0f}% over budget\n"
        
        # Identify unusual patterns
        if len(transactions) > 0:
            avg_daily_spending = total_spent / days
            response += f"\n📊 Average daily spending: ${avg_daily_spending:.2f}\n"
        
        return response
        
    except Exception as e:
        return f"Error analyzing transactions: {str(e)}"


@tool
def fetch_market_data(ticker: str, include_news: Union[bool, str] = False) -> str:
    """
    Fetches current market data for a stock or fund including price, trends, and optionally news.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        include_news: Whether to include recent news headlines
    
    Returns:
        String with market data and analysis
    """
    # Handle case where agent passes JSON string instead of boolean/str
    if isinstance(ticker, str):
        try:
            import json
            if '{' in ticker:
                data = json.loads(ticker)
                if isinstance(data, dict):
                    ticker = data.get('ticker', ticker)
        except:
            pass

    if isinstance(include_news, str):
        try:
            import json
            if '{' in include_news:
                data = json.loads(include_news)
                if isinstance(data, dict):
                    include_news = data.get('include_news', False)
            else:
                include_news = include_news.lower() == 'true'
        except:
            include_news = False

    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get current price and key metrics
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
        prev_close = info.get('previousClose', 'N/A')
        day_change = ((current_price - prev_close) / prev_close * 100) if current_price != 'N/A' and prev_close != 'N/A' else 'N/A'
        
        # Get historical performance
        hist = stock.history(period='6mo')
        if not hist.empty:
            six_month_change = ((current_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100) if current_price != 'N/A' else 'N/A'
        else:
            six_month_change = 'N/A'
        
        response = f"""MARKET DATA for {ticker}:

CURRENT METRICS:
- Current Price: ${current_price:.2f if current_price != 'N/A' else current_price}
- Previous Close: ${prev_close:.2f if prev_close != 'N/A' else prev_close}
- Day Change: {day_change:+.2f}% if day_change != 'N/A' else 'N/A'
- 6-Month Change: {six_month_change:+.2f}% if six_month_change != 'N/A' else 'N/A'

KEY INFO:
- Company: {info.get('longName', 'N/A')}
- Sector: {info.get('sector', 'N/A')}
- Industry: {info.get('industry', 'N/A')}
- Market Cap: ${info.get('marketCap', 0):,.0f}
- P/E Ratio: {info.get('trailingPE', 'N/A')}
- Dividend Yield: {info.get('dividendYield', 0)*100:.2f}% if info.get('dividendYield') else 'N/A'
"""
        
        if include_news:
            try:
                news = stock.news
                if news:
                    response += "\nRECENT NEWS:\n"
                    for article in news[:3]:
                        response += f"- {article.get('title', 'No title')}\n"
            except:
                response += "\nNews not available.\n"
        
        return response
        
    except Exception as e:
        return f"Error fetching market data for {ticker}: {str(e)}"


@tool
def generate_insights() -> str:
    """
    Generates personalized financial insights and recommendations based on the user's profile,
    portfolio, and current financial goals.
    
    Returns:
        String with personalized insights and recommendations
    """
    try:
        user = USER_PROFILE
        
        response = f"""PERSONALIZED FINANCIAL INSIGHTS:

USER PROFILE:
- Risk Tolerance: {user['risk_tolerance'].upper()}
- Investment Horizon: {user['investment_horizon']}
- Monthly Income: ${user['income']['monthly_salary']:,.2f}
- Monthly Budget: ${user['expenses']['monthly_budget']:,.2f}

FINANCIAL GOALS:
"""
        for i, goal in enumerate(user['financial_goals'], 1):
            response += f"{i}. {goal}\n"
        
        response += """
RECOMMENDATIONS:
1. 💼 Portfolio Diversification: Your portfolio is heavily weighted toward technology stocks. Consider diversifying into other sectors to reduce risk.

2. 💰 Emergency Fund: Target is $50,000. Review your current cash position and savings rate to stay on track.

3. 🏠 House Down Payment Goal: With a 3-year timeline for $150,000, you need to save ~$4,170/month. Consider high-yield savings or short-term bonds.

4. 📊 Retirement Planning: With a moderate risk tolerance, maintain a balanced mix of growth stocks and index funds.

5. 🎯 Next Steps:
   - Review your largest expense categories for optimization opportunities
   - Consider rebalancing if tech allocation exceeds 60% of equity portfolio
   - Set up automatic transfers to dedicated savings goals
"""
        
        return response
        
    except Exception as e:
        return f"Error generating insights: {str(e)}"


@tool
def check_goal_alignment(proposed_action: str) -> str:
    """
    Checks if a proposed financial action aligns with the user's stated financial goals
    and risk tolerance.
    
    Args:
        proposed_action: Description of the action being considered
    
    Returns:
        String with alignment analysis and recommendation
    """
    # Handle case where agent passes JSON string
    if isinstance(proposed_action, str):
        try:
            import json
            if '{' in proposed_action:
                data = json.loads(proposed_action)
                if isinstance(data, dict):
                    proposed_action = data.get('proposed_action', proposed_action)
        except:
            pass

    try:
        user = USER_PROFILE
        
        response = f"""GOAL ALIGNMENT ANALYSIS:

Proposed Action: {proposed_action}

USER CONTEXT:
- Risk Tolerance: {user['risk_tolerance']}
- Investment Horizon: {user['investment_horizon']}
- Key Goals: {', '.join(user['financial_goals'][:2])}

ANALYSIS:
"""
        
        # Simple keyword-based analysis (in production, would use more sophisticated NLP)
        action_lower = proposed_action.lower()
        
        # Check for risky behavior
        if any(word in action_lower for word in ['crypto', 'options', 'leverage', 'margin']):
            if user['risk_tolerance'] == 'conservative':
                response += "⚠️ This action may not align with your CONSERVATIVE risk tolerance.\n"
            elif user['risk_tolerance'] == 'moderate':
                response += "⚠️ Exercise caution - this is higher risk than your typical MODERATE risk profile.\n"
        
        # Check for short-term investing
        if 'short-term' in action_lower or 'quick' in action_lower:
            if user['investment_horizon'] == 'long-term':
                response += "⚠️ This seems like a short-term strategy, but your investment horizon is LONG-TERM.\n"
        
        # Check alignment with goals
        if any(word in action_lower for word in ['save', 'saving', 'emergency fund']):
            response += "✅ Aligns well with your emergency fund goal.\n"
        
        if any(word in action_lower for word in ['house', 'down payment', 'property']):
            response += "✅ Aligns with your house down payment goal.\n"
        
        if any(word in action_lower for word in ['retirement', '401k', 'ira', 'long-term']):
            response += "✅ Aligns with your retirement planning goal.\n"
        
        # General recommendation
        response += "\nRECOMMENDATION: Consider how this action helps you progress toward your stated goals while respecting your risk tolerance.\n"
        
        return response
        
    except Exception as e:
        return f"Error checking goal alignment: {str(e)}"
