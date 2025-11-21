# 🚀 Quick Start Guide

## ✅ Fixed Import Errors!

The import errors have been resolved. The application now uses `langchain_classic` which is compatible with LangChain 1.0.8+.

## 📝 Next Steps to Run the Application

### 1. Add Your API Key

Create a `.env` file from the example:
```bash
cp .env.example .env
```

Then edit `.env` and add your API key. **Get a FREE Google Gemini API key** (recommended):
1. Go to https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Copy the key

Edit `.env` and replace `your_gemini_api_key_here` with your actual key:
```plaintext
GOOGLE_API_KEY=your_actual_key_here
MODEL_NAME=gemini-pro
```

### 2. Start the Server

```bash
python main.py
```

### 3. Open in Browser

Navigate to: **http://localhost:8000**

## 🛠️ What Was Fixed

1. ✅ Installed `langchain-classic` for agent components
2. ✅ Installed `langchain-google-genai` for Gemini support  
3. ✅ Installed `langchain-openai` for OpenAI support
4. ✅ Updated imports in `financial_agent.py`:
   - `from langchain_classic.agents import AgentExecutor, create_react_agent`
   - `from langchain_classic.memory import ConversationBufferMemory`
5. ✅ Fixed `tiktoken` installation (prebuilt wheel now available)

## 🎯 The 5 Tools Available

Once running, the AI agent can use these tools:

1. **`analyze_portfolio`** - Real-time portfolio analysis with yfinance
2. **`analyze_transactions`** - Spending pattern recognition
3. **`fetch_market_data`** - Live stock prices and news
4. **`generate_insights`** - Personalized recommendations
5. **`check_goal_alignment`** - Goal validation

## ❓ Troubleshooting

**Server won't start?**
- Make sure you added a valid API key to `.env`
- Check that you're in the virtual environment: `source venv/bin/activate`

**Port 8000 already in use?**
- Change the PORT in `.env` to 8001 or another available port

**API key errors?**
- Verify your API key is correct
- Make sure there are no extra spaces in the `.env` file

## 💡 Try These Queries Once Running

- "How is my portfolio performing?"
- "Analyze my spending this month"
- "What's the current price of AAPL?"
- "Give me personalized financial insights"
- "Should I invest more in tech stocks?"

---

**All dependencies installed!** Just add your API key and run `python main.py` 🎉
