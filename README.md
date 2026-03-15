# AI Career Sentinel 🤖

An autonomous multi-agent system that scrapes fresh GenAI & ML 
engineering jobs every morning, scores them against your resume 
using RAG, and delivers a personalised brief to your Telegram.

## Architecture
```
⏰ 8am IST Trigger (APScheduler)
        ↓
🔍 Scraper Agent (JSearch API + SQLite dedup)
        ↓
🌐 MCP Server → fetch_job_description tool
        ↓
🧠 RAG Engine (Sentence Transformers + Cosine Similarity)
        ↓
🤖 Groq/Llama Scorer (GREEN / YELLOW / RED per job)
        ↓
✍️  Brief Writer Agent (Llama 3.3 70B)
        ↓
📱 Telegram Bot (morning brief on your phone)
```

## Tech Stack

- Python
- MCP Protocol (real client/server via stdio)
- Sentence Transformers (all-MiniLM-L6-v2)
- Groq API + Llama 3.3 70B (free)
- JSearch API (job scraping)
- Telegram Bot API
- SQLite (deduplication)
- APScheduler
- httpx + BeautifulSoup

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/amit-ranjan-9/ai-career-sentinel.git
cd ai-career-sentinel
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file:
```
JSEARCH_API_KEY=your_jsearch_key
GROQ_API_KEY=your_groq_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 5. Add your resume
Paste your resume as plain text in `data/resume.txt`

### 6. Run once manually
```bash
python main.py
```

### 7. Run scheduler (daily 8am IST)
```bash
python scheduler/runner.py
```

## How to get API keys (all free)

- **JSearch** → rapidapi.com → search JSearch → free tier
- **Groq** → console.groq.com → free (14k requests/day)
- **Telegram Bot** → message @BotFather → /newbot

## Project Structure
```
ai-career-sentinel/
├── agents/
│   ├── scraper.py        # Job scraping + deduplication
│   ├── rag_matcher.py    # Resume vs JD matching
│   ├── scorer.py         # Groq/Llama scoring agent
│   └── brief_writer.py   # Morning brief generation
├── mcp_tools/
│   ├── mcp_server.py     # Real MCP server (2 tools)
│   ├── mcp_client.py     # MCP client (stdio protocol)
│   ├── jsearch.py        # JSearch API wrapper
│   └── fetch_mcp.py      # Fetch tool fallback
├── telegram_bot/
│   └── notifier.py       # Telegram delivery
├── scheduler/
│   └── runner.py         # APScheduler 8am IST
├── utils/
│   └── embedder.py       # Sentence Transformers wrapper
├── data/
│   └── resume.txt        # Your resume (plain text)
├── main.py               # Main orchestrator
├── requirements.txt
└── .env                  # API keys (never commit!)
```

## License
MIT