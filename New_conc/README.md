# AI Financial Relationship Manager 💰

An intelligent AI-powered financial relationship manager that provides personalized, conversational guidance by analyzing portfolios, transaction history, and real-time market data.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)

## ✨ Features

- **🤖 Conversational AI Agent**: Natural language financial advice powered by LangChain and LLMs (Gemini/OpenAI/Anthropic)
- **📊 Portfolio Analysis**: Real-time tracking of stocks and mutual funds with gain/loss calculations
- **💳 Transaction Insights**: Smart spending pattern recognition and budget tracking
- **📈 Market Data Integration**: Live stock prices and news via yfinance (free, no API key required)
- **🎯 Goal Alignment**: Personalized recommendations based on your financial goals
- **💎 Premium UI**: Beautiful dark theme with glassmorphism effects and smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- An API key for one of:
  - Google Gemini (recommended - free tier available)
  - OpenAI
  - Anthropic Claude

### Installation

1. **Clone or navigate to the project directory**:
```bash
cd New_conc
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```env
# For Google Gemini (recommended)
GOOGLE_API_KEY=your_gemini_api_key_here
MODEL_NAME=gemini-pro

# OR for OpenAI
# OPENAI_API_KEY=your_openai_api_key_here
# MODEL_NAME=gpt-4

# OR for Anthropic
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# MODEL_NAME=claude-3-sonnet-20240229
```

### Getting an API Key

**Google Gemini (Free):**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API Key"
3. Copy your key and paste it in `.env`

**OpenAI:**
1. Sign up at [OpenAI](https://platform.openai.com/)
2. Navigate to API keys section
3. Create and copy your key

**Anthropic:**
1. Sign up at [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Copy and add to `.env`

### Run the Application

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --port 8000
```

Then open your browser to: **http://localhost:8000**

## 🎯 How to Use

### Chat with Your AI Advisor

Navigate to the **AI Advisor** section and try these example queries:

- "How is my portfolio performing?"
- "Analyze my spending patterns this month"
- "What are the current prices for my stock holdings?"
- "Should I invest more in tech stocks?"
- "Give me personalized financial insights"
- "Am I on track for my emergency fund goal?"

### Quick Actions

Use the **Quick Prompts** for instant insights:
- 📊 Portfolio Performance
- 💳 Spending Analysis  
- 📈 Market Update
- 💡 Get Insights

## 🧠 Agent Capabilities

The AI agent has access to 5 powerful tools:

1. **`analyze_portfolio`**: Calculates current portfolio value, gains/losses, and asset allocation
2. **`analyze_transactions`**: Identifies spending patterns and compares against budget
3. **`fetch_market_data`**: Gets real-time stock prices, news, and market metrics via yfinance
4. **`generate_insights`**: Creates personalized recommendations based on your profile
5. **`check_goal_alignment`**: Validates if proposed actions align with your financial goals

## 📁 Project Structure

```
New_conc/
├── main.py                 # FastAPI server
├── agent/
│   ├── config.py          # Multi-provider AI configuration
│   ├── financial_agent.py # LangChain agent orchestrator
│   ├── tools.py           # Financial analysis tools
│   └── prompts.py         # System prompts
├── data/
│   ├── mock_user.py       # User profile data
│   ├── mock_portfolio.py  # Stock & mutual fund holdings
│   └── mock_transactions.py # Transaction history
├── public/
│   ├── index.html         # Dashboard UI
│   ├── styles.css         # Premium dark theme
│   └── app.js             # Frontend logic
├── requirements.txt       # Python dependencies
└── .env                   # Configuration (create from .env.example)
```

## 🎨 Technology Stack

**Backend:**
- FastAPI - High-performance async web framework
- LangChain - Agent orchestration with ReAct pattern
- Google Gemini / OpenAI / Anthropic - LLM providers
- yfinance - Free market data (no API key required)
- Pandas & NumPy - Data analysis

**Frontend:**
- Vanilla HTML/CSS/JavaScript
- Modern dark UI with glassmorphism
- Responsive design
- Real-time chat interface

## 🔧 Customization

### Modify User Profile

Edit `data/mock_user.py` to customize:
- Financial goals
- Risk tolerance
- Income and expenses
- Investment preferences

### Add Portfolio Holdings

Edit `data/mock_portfolio.py` to add/modify:
- Stock positions
- Mutual fund investments
- Cash positions

### Adjust Agent Behavior

Edit `agent/prompts.py` to customize:
- Agent personality
- Response style
- Financial advice guidelines

## 🚦 Example Conversations

**User**: "How is my portfolio performing?"

**AI**: *Uses `analyze_portfolio` tool to fetch real-time prices, then provides:*
- Total portfolio value and gains/losses
- Individual stock performance
- Asset allocation breakdown
- Top performers and underperformers

**User**: "Should I invest more in AAPL?"

**AI**: *Uses `fetch_market_data` for AAPL and `check_goal_alignment` to:*
- Check current AAPL price and trends
- Assess your tech sector exposure
- Compare against your risk tolerance
- Provide personalized recommendation

## 📊 Data Sources

- **Market Data**: yfinance (Yahoo Finance) - free, real-time stock prices and company info
- **Portfolio**: Mock data in `data/mock_portfolio.py` (extendable to real brokerage APIs)
- **Transactions**: Generated mock data (can integrate with Plaid, Stripe, etc.)

## 🔐 Security Notes

- Never commit your `.env` file with real API keys
- API keys are loaded via environment variables
- For production: add authentication, use HTTPS, secure database

## 🛠️ Troubleshooting

**"No API key found" error:**
- Make sure you've created `.env` from `.env.example`
- Verify your API key is correctly set

**Module not found errors:**
- Run `pip install -r requirements.txt` again
- Ensure you're using Python 3.8+

**Market data not loading:**
- yfinance is free but rate-limited
- Wait a moment and try again
- Check your internet connection

## 📝 Future Enhancements

- [ ] Real brokerage API integration (Alpaca, Interactive Brokers)
- [ ] Database persistence (PostgreSQL/MongoDB)
- [ ] User authentication and multi-user support
- [ ] Advanced charting with Chart.js or D3.js
- [ ] Email/SMS alerts for goal milestones
- [ ] Tax optimization recommendations
- [ ] Retirement planning calculators

## 📄 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project, but feel free to fork and customize for your needs!

---

**Built with ❤️ using Python, FastAPI, and LangChain**
