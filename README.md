# 🤖 Live AI Assistant

<div align="center">

![Live AI Assistant](https://img.shields.io/badge/Live%20AI-Assistant-6366f1?style=for-the-badge&logo=lightning&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61dafb?style=for-the-badge&logo=react&logoColor=black)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-white?style=for-the-badge&logo=ollama&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A fully local, production-ready AI assistant with real-time streaming, semantic memory, and built-in tools.**

[Features](#-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Project Structure](#-project-structure)

</div>

---

## 📸 Overview

Live AI Assistant is a full-stack AI chat application that runs **entirely on your local machine**. It combines a FastAPI backend with an Ollama-powered LLM, FAISS vector memory for semantic recall, and a premium React frontend with real-time streaming.

> **No cloud required.** Everything runs locally — your data stays private.

---

## ✨ Features

### 🧠 AI & Memory
- **Local LLM** via [Ollama](https://ollama.com/) (default: `qwen2.5:3b`)
- **Real-time streaming** — responses appear token by token
- **Conversation memory** — last 20 messages kept in context
- **Semantic vector memory** — FAISS + `all-MiniLM-L6-v2` embeddings for long-term recall

### 🔧 Built-in Tools
| Tool | Trigger | Description |
|------|---------|-------------|
| 🌐 **Web Search** | "search", "latest", "news", "today" | Live web search via [Tavily API](https://tavily.com/) |
| 🧮 **Calculator** | `+`, `-`, `*`, `/` operators | Safe arithmetic expression evaluator |
| 🕐 **Date & Time** | "what time", "today's date" | Returns current date and time |
| 📄 **File Reader** | "read file", "open file" | Reads local text files |

### 🎨 Frontend
- **Dark glassmorphism UI** with purple/indigo accent system
- **Markdown rendering** with GitHub Flavored Markdown (GFM)
- **Syntax-highlighted code blocks** with one-click copy
- **Tool result cards** — visual cards for search results, calculations
- **Connection status** — live health monitoring of backend
- **Responsive** — works on desktop and mobile

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                     Frontend (React)                │
│   Sidebar │ WelcomeScreen │ ChatMessages │ ChatInput │
│              Vite Dev Server :5173                  │
│           Proxy /api → localhost:8000               │
└─────────────────┬───────────────────────────────────┘
                  │ HTTP / SSE Streaming
┌─────────────────▼───────────────────────────────────┐
│                  Backend (FastAPI)                  │
│                                                     │
│  POST /api/v1/chat          ← Full response         │
│  POST /api/v1/chat/stream   ← Streaming response    │
│  GET  /api/v1/memory        ← Conversation history  │
│  POST /api/v1/memory/clear  ← Reset memory          │
│  GET  /api/v1/health        ← Health check          │
│                                                     │
│  ┌─────────────┐  ┌─────────┐  ┌──────────────┐   │
│  │ AssistantAgent│  │ Planner │  │ ToolManager  │   │
│  └──────┬──────┘  └────┬────┘  └──────┬───────┘   │
│         │              │               │            │
│  ┌──────▼──────┐  ┌────▼─────────────▼──────────┐ │
│  │MemoryManager│  │    Tools Registry             │ │
│  │             │  │  WebSearch │ Calculator       │ │
│  │ ConvMemory  │  │  DateTime  │ FileReader       │ │
│  │ VectorMemory│  └──────────────────────────────┘ │
│  └─────────────┘                                   │
│                                                     │
│  ┌──────────────┐   ┌────────────────────────────┐ │
│  │ LLM Provider │   │   Vector Store (FAISS)     │ │
│  │ Ollama/OpenAI│   │  all-MiniLM-L6-v2 Embeds  │ │
│  └──────────────┘   └────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Live-Ai-Assistent/
│
├── 📂 backend/                        # FastAPI Backend
│   ├── 📂 app/
│   │   ├── 📄 main.py                 # FastAPI app entry point, CORS config
│   │   │
│   │   ├── 📂 api/
│   │   │   └── 📂 v1/
│   │   │       ├── 📄 router.py       # API router — registers all endpoints
│   │   │       └── 📂 endpoints/
│   │   │           ├── 📄 chat.py     # POST /chat & POST /chat/stream
│   │   │           ├── 📄 health.py   # GET /health
│   │   │           └── 📄 memory.py   # GET /memory, POST /memory/clear
│   │   │
│   │   ├── 📂 agents/
│   │   │   ├── 📄 base.py             # Abstract BaseAgent
│   │   │   ├── 📄 assistant.py        # Main AssistantAgent (run + stream)
│   │   │   └── 📄 planner.py          # Keyword-based tool routing
│   │   │
│   │   ├── 📂 llm/
│   │   │   ├── 📂 providers/
│   │   │   │   ├── 📄 base.py         # Abstract BaseLLMProvider
│   │   │   │   ├── 📄 factory.py      # Provider factory (ollama/openai)
│   │   │   │   └── 📄 ollama.py       # OllamaProvider (chat + stream)
│   │   │   └── 📂 prompts/
│   │   │       └── 📄 system_prompt.py# System prompt definition
│   │   │
│   │   ├── 📂 memory/
│   │   │   ├── 📄 base.py             # Abstract BaseMemory
│   │   │   ├── 📄 manager.py          # MemoryManager (conv + vector)
│   │   │   ├── 📄 conversation.py     # In-memory chat history (last 20)
│   │   │   ├── 📄 vector.py           # VectorMemory (FAISS-backed)
│   │   │   ├── 📄 embeddings.py       # SentenceTransformer embeddings
│   │   │   └── 📄 retriever.py        # Semantic retrieval
│   │   │
│   │   ├── 📂 tools/
│   │   │   ├── 📄 base.py             # Abstract BaseTool
│   │   │   ├── 📄 registry.py         # Tool registry (register/get)
│   │   │   ├── 📄 manager.py          # ToolManager (wires all tools)
│   │   │   ├── 📄 web_search.py       # Tavily web search
│   │   │   ├── 📄 calculator.py       # Safe AST-based calculator
│   │   │   ├── 📄 datetime_tool.py    # Current date/time
│   │   │   └── 📄 file_reader.py      # Local file reader
│   │   │
│   │   ├── 📂 vectorstore/
│   │   │   └── 📄 faiss_store.py      # FAISS index (add/search/save/clear)
│   │   │
│   │   ├── 📂 core/
│   │   │   ├── 📄 settings.py         # Pydantic settings (reads .env)
│   │   │   └── 📄 logging.py          # Logging configuration
│   │   │
│   │   ├── 📂 db/
│   │   │   ├── 📄 database.py         # SQLAlchemy engine + Base
│   │   │   └── 📄 session.py          # DB session factory
│   │   │
│   │   └── 📂 schemas/
│   │       ├── 📄 chat.py             # ChatRequest schema
│   │       └── 📄 health.py           # HealthResponse schema
│   │
│   ├── 📂 alembic/                    # DB migrations
│   ├── 📄 alembic.ini
│   ├── 📄 requirements.txt            # Python dependencies
│   └── 📄 .env                        # Environment variables (see below)
│
├── 📂 frontend/                       # React Frontend (Vite)
│   ├── 📂 src/
│   │   ├── 📄 main.jsx                # React entry point
│   │   ├── 📄 App.jsx                 # Root component — chat orchestration
│   │   ├── 📄 index.css              # Full design system (CSS variables + layout)
│   │   │
│   │   ├── 📂 api/
│   │   │   └── 📄 client.js           # API client (chat, stream, memory, health)
│   │   │
│   │   └── 📂 components/
│   │       ├── 📄 Sidebar.jsx         # Brand, actions, tools, connection status
│   │       ├── 📄 ChatMessage.jsx     # Markdown, code blocks, tool result cards
│   │       └── 📄 ChatInput.jsx       # Auto-expand textarea, keyboard shortcuts
│   │
│   ├── 📂 public/
│   │   └── 📄 favicon.svg             # Custom gradient favicon
│   │
│   ├── 📄 index.html                  # HTML template with SEO meta tags
│   ├── 📄 vite.config.js              # Vite config + /api proxy to :8000
│   └── 📄 package.json
│
├── 📂 docker/                         # Docker configs (WIP)
├── 📂 docs/                           # Documentation (WIP)
├── 📄 .gitignore
└── 📄 LICENSE
```

---

## ⚡ Quick Start

### Prerequisites

Make sure you have the following installed:

| Requirement | Version | Check |
|-------------|---------|-------|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| [Ollama](https://ollama.com/download) | Latest | `ollama --version` |
| PostgreSQL | 14+ | `psql --version` |

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/Live-Ai-Assistent.git
cd Live-Ai-Assistent
```

---

### Step 2 — Pull the LLM Model

```bash
ollama pull qwen2.5:3b
```

> You can use any Ollama model. Update `OLLAMA_MODEL` in `.env` to switch models.

---

### Step 3 — Configure Environment Variables

```bash
cd backend
copy .env.example .env   # Windows
# or: cp .env.example .env  (Linux/macOS)
```

Edit `backend/.env`:

```env
# App
APP_NAME=Live AI Assistant
APP_VERSION=1.0.0
DEBUG=True
HOST=127.0.0.1
PORT=8000

# LLM — Ollama
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama
OLLAMA_MODEL=qwen2.5:3b

# Web Search (get a free key at https://tavily.com)
TAVILY_API_KEY=your_tavily_api_key_here

# PostgreSQL Database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=live_ai_assistent
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
```

---

### Step 4 — Set Up the Database

```bash
# Create the PostgreSQL database
psql -U postgres -c "CREATE DATABASE live_ai_assistent;"

# Run Alembic migrations
cd backend
alembic upgrade head
```

---

### Step 5 — Install Backend Dependencies

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 6 — Start the Backend Server

```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
Live AI Assistant Started
```

> 📖 Interactive API docs available at: **http://127.0.0.1:8000/docs**

---

### Step 7 — Install Frontend Dependencies

Open a **new terminal**:

```bash
cd frontend
npm install
```

---

### Step 8 — Start the Frontend

```bash
npm run dev
```

You should see:
```
  VITE v8.x.x  ready in xxxx ms

  ➜  Local:   http://localhost:5173/
```

---

### Step 9 — Open the App 🎉

Open your browser at:

```
http://localhost:5173
```

---

## 🔌 API Reference

Base URL: `http://127.0.0.1:8000/api/v1`

### `GET /health`
Check if the backend is running.

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### `POST /chat`
Send a message and get a full response.

**Request:**
```json
{
  "message": "What is the capital of France?"
}
```

**Response (LLM):**
```json
{
  "type": "llm",
  "response": "The capital of France is Paris."
}
```

**Response (Tool):**
```json
{
  "type": "tool",
  "tool": "web_search",
  "result": { "answer": "...", "results": [...] }
}
```

---

### `POST /chat/stream`
Send a message and receive a **streaming** plain-text response (SSE-style).

```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum computing"}' \
  --no-buffer
```

---

### `GET /memory`
Retrieve the full conversation history.

```json
[
  { "role": "user", "content": "Hello!" },
  { "role": "assistant", "content": "Hi! How can I help you?" }
]
```

---

### `POST /memory/clear`
Clear all conversation and vector memory.

```json
{ "message": "Conversation memory cleared" }
```

---

## 🛠️ Configuration

### Switching LLM Models

Edit `backend/.env`:

```env
# Use a different Ollama model
OLLAMA_MODEL=llama3.2:3b
# or
OLLAMA_MODEL=mistral:7b
# or
OLLAMA_MODEL=gemma2:2b
```

Then restart the backend.

---

### Changing the System Prompt

Edit [`backend/app/llm/prompts/system_prompt.py`](backend/app/llm/prompts/system_prompt.py):

```python
SYSTEM_PROMPT = """
You are Live AI Assistant.
Be accurate and concise.
Answer professionally.
Help the user learn.
Do not hallucinate.
"""
```

---

### Tool Routing Rules

The Planner in [`backend/app/agents/planner.py`](backend/app/agents/planner.py) routes messages to tools based on keywords:

| Keywords | Tool Triggered |
|----------|---------------|
| `latest`, `news`, `today`, `current`, `search`, `google` | `web_search` |
| `+`, `-`, `*`, `/` (operators in message) | `calculator` |
| *(none matched)* | LLM response |

---

## 📦 Tech Stack

### Backend
| Library | Purpose |
|---------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework + async API |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| [Ollama](https://ollama.com/) | Local LLM runtime |
| [OpenAI SDK](https://github.com/openai/openai-python) | Ollama-compatible client |
| [FAISS](https://github.com/facebookresearch/faiss) | Vector similarity search |
| [sentence-transformers](https://sbert.net/) | Text embeddings (`all-MiniLM-L6-v2`) |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM + database |
| [Alembic](https://alembic.sqlalchemy.org/) | DB migrations |
| [Pydantic](https://docs.pydantic.dev/) | Settings + data validation |
| [Tavily](https://tavily.com/) | Web search API |
| [HTTPX](https://www.python-httpx.org/) | Async HTTP client |

### Frontend
| Library | Purpose |
|---------|---------|
| [React 19](https://react.dev/) | UI framework |
| [Vite 8](https://vite.dev/) | Build tool + dev server |
| [react-markdown](https://github.com/remarkjs/react-markdown) | Markdown rendering |
| [remark-gfm](https://github.com/remarkjs/remark-gfm) | GitHub Flavored Markdown |
| [react-syntax-highlighter](https://github.com/react-syntax-highlighter/react-syntax-highlighter) | Code block highlighting |
| [lucide-react](https://lucide.dev/) | Icon library |
| Vanilla CSS | Design system (no framework) |

---

## 🐛 Troubleshooting

### ❌ `Ollama connection refused`
```bash
# Make sure Ollama is running
ollama serve

# Verify the model is downloaded
ollama list
```

### ❌ `Database connection failed`
```bash
# Make sure PostgreSQL is running
# Windows:
net start postgresql

# Check credentials in backend/.env match your PostgreSQL setup
```

### ❌ `Module not found` errors
```bash
# Make sure your virtual environment is activated
cd backend
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
```

### ❌ Frontend shows "Offline" status
- Make sure the backend is running on port `8000`
- Check the browser console for errors
- Verify `vite.config.js` has the proxy set to `http://127.0.0.1:8000`

### ❌ Web search returns errors
- Get a free API key at [tavily.com](https://tavily.com)
- Set `TAVILY_API_KEY` in `backend/.env`

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Ollama](https://ollama.com/) — for making local LLM inference accessible
- [Tavily](https://tavily.com/) — for the excellent web search API
- [FAISS](https://github.com/facebookresearch/faiss) by Meta — for vector similarity search
- [sentence-transformers](https://sbert.net/) — for the embedding models

---

<div align="center">

Made with ❤️ by **Supritto**

⭐ Star this repo if you found it useful!

</div>
