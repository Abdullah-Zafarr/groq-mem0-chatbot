# Stateful Chatbot with Groq & Mem0

A powerful chatbot that combines **Groq's LLM capabilities** with **Mem0's long-term memory** to create a stateful, learning AI assistant — available both as a **CLI tool** and a **Streamlit web app**.

<!-- Screenshot: Open the app at http://localhost:8501, take a screenshot, and save it as assets/chatbot-screenshot.png -->
<!-- Then uncomment the line below: -->
<!-- ![Chatbot Screenshot](assets/chatbot-screenshot.png) -->

## Features

✨ **Stateful Conversations** — Maintains conversation history within a session  
🧠 **Long-Term Memory** — Powered by Mem0, learns and remembers from past interactions  
⚡ **Fast LLM Responses** — Uses Groq's llama-3.3-70b-versatile model  
🎯 **Smart Memory** — AI-powered filter saves only meaningful exchanges, skipping trivial messages like greetings  
🌐 **Web UI** — Beautiful Streamlit interface with dark theme, gradient branding, and status badges  
💻 **CLI Mode** — Terminal-based chat with emoji indicators  
🔐 **Secure API Management** — Environment-based API key management with `python-dotenv`  
🎨 **Modern Design** — Inter font, glassmorphism sidebar, smooth animations  

## Quick Start

### 1. Install Dependencies

```bash
uv add groq mem0ai python-dotenv streamlit
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
groq_api=your_groq_api_key_here
mem0_api=your_mem0_api_key_here
```

Get your keys from:
- **Groq**: https://console.groq.com/keys
- **Mem0**: https://app.mem0.ai/

### 3. Run the Chatbot

**Web UI (recommended):**
```bash
uv run streamlit run app.py
```
Then open **http://localhost:8501** in your browser.

**CLI mode:**
```bash
python chatbot.py
```

## Architecture

### Core Components

| Component | Function | Description |
|-----------|----------|-------------|
| `load_environment()` | Configuration | Loads API keys from `.env` |
| `initialize_clients()` | Setup | Initializes Groq + Mem0 clients |
| `search_memories()` | Memory Retrieval | Searches Mem0 for relevant context |
| `build_system_message()` | Prompt Engineering | Injects memories into system prompt |
| `chat_with_groq()` | LLM Interaction | Sends messages to Groq |
| `store_memory()` | Memory Persistence | Stores exchanges in Mem0 |
| `is_worth_remembering()` | Smart Filter | Uses LLM to classify memory importance |

### How Memory Works

```
User Input → Search Mem0 for relevant memories
           → Inject memories into system prompt
           → Send to Groq LLM → Get response
           → Smart filter evaluates importance
           → If important → Store in Mem0
           → If trivial (hello, thanks) → Skip
```

### Web UI Features

- **Chat Interface** — Native Streamlit chat with `st.chat_message`
- **Smart Memory Toggle** — Sidebar toggle to enable/disable auto-saving
- **Memory Badges** — Visual indicators showing memory search results and save status
- **Clear Chat** — One-click conversation reset
- **Conversation History** — Maintains last 20 exchanges per session

## Project Structure

```
chatbot-with-memory/
├── app.py              # Streamlit web UI
├── chatbot.py          # Core chatbot logic + CLI mode
├── .env                # Environment variables (keep secret!)
├── pyproject.toml      # Project dependencies
├── assets/
│   └── chatbot-screenshot.png
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Tech Stack

- **LLM**: Groq — llama-3.3-70b-versatile
- **Memory**: Mem0 (long-term memory service)
- **Frontend**: Streamlit
- **Runtime**: Python 3.14+
- **Package Manager**: uv

## Error Handling

The chatbot includes robust error handling for:
- Missing API keys
- Memory search failures
- Groq API errors
- Memory storage errors
- Smart filter fallback (saves on classifier failure)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing API Keys | Ensure both `groq_api` and `mem0_api` are in `.env` |
| Memory not stored | Check Mem0 API key and account quota |
| Slow responses | Verify Groq API connectivity and internet |
| Wrong Python version | Requires Python 3.14+ |

## Future Enhancements

- [ ] Multi-user support with different user IDs
- [ ] Conversation export to JSON/text
- [ ] Memory analytics dashboard
- [ ] Custom system prompts per user
- [ ] Rate limiting and usage tracking
- [ ] Database integration for local persistence

## License

MIT License — Feel free to use and modify!

---

**Built with** ⚡ Groq + 🧠 Mem0 + 🎈 Streamlit + 🐍 Python
