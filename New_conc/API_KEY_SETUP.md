# ⚠️ API Key Required

## 🔴 Current Error
```
No API key found. Please set GOOGLE_API_KEY, OPENAI_API_KEY, 
or ANTHROPIC_API_KEY in your .env file
```

## ✅ How to Fix

### Step 1: Get a FREE API Key

**Option A: Google Gemini** (Recommended - Free tier available)
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

**Option B: OpenAI**
1. Go to: https://platform.openai.com/api-keys
2. Sign up/login
3. Create new API key
4. Copy the key

**Option C: Anthropic Claude**
1. Go to: https://console.anthropic.com/
2. Sign up/login
3. Go to API Keys
4. Create new key
5. Copy the key

### Step 2: Add Your API Key to .env

Open the `.env` file in your editor and replace `your_gemini_api_key_here` with your actual key:

**For Google Gemini:**
```env
GOOGLE_API_KEY=AIzaSyYOUR_ACTUAL_KEY_HERE
MODEL_NAME=gemini-pro
```

**For OpenAI:**
```env
OPENAI_API_KEY=sk-YOUR_ACTUAL_KEY_HERE
MODEL_NAME=gpt-4
```

**For Anthropic:**
```env
ANTHROPIC_API_KEY=sk-ant-YOUR_ACTUAL_KEY_HERE
MODEL_NAME=claude-3-sonnet-20240229
```

### Step 3: Restart the Server

1. Stop the current server (Ctrl+C in the terminal where it's running)
2. Start it again:
```bash
python main.py
```

3. Refresh your browser at http://localhost:8000

## ✨ Then Try Again!

Once you've added your API key and restarted, try these queries:
- "How is my portfolio performing?"
- "Analyze my spending this month"
- "Give me personalized financial insights"

---

**Note:** The `.env` file is gitignored (for security) so it won't be committed to version control.
