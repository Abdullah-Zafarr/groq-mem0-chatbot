# Stateful CLI Chatbot with Groq & Mem0

A powerful CLI chatbot that combines **Groq's LLM capabilities** with **Mem0's long-term memory** to create a stateful, learning AI assistant.

## Features

✨ **Stateful Conversations** - The chatbot maintains conversation history within a session  
🧠 **Long-Term Memory** - Powered by Mem0, the chatbot learns and remembers from previous interactions  
⚡ **Fast LLM Responses** - Uses Groq's llama-3.3-70b-versatile model for quick, high-quality responses  
🔐 **Secure API Management** - Environment-based API key management with `python-dotenv`  
📝 **Clean Output** - User-friendly interface with emoji indicators (🤖, 👤, 💾)  
🎯 **Modular Architecture** - Well-organized, reusable functions for easy maintenance

## Architecture

### Core Components

1. **Environment Management** (`load_environment()`)
   - Loads `groq_api` and `mem0_api` from `.env` file securely

2. **Client Initialization** (`initialize_clients()`)
   - Sets up Groq client for LLM calls
   - Sets up Mem0 client for memory management

3. **Memory Search** (`search_memories()`)
   - Searches for relevant memories based on current user input
   - Uses fixed `user_id="abdullah_01"` for consistency

4. **System Message Building** (`build_system_message()`)
   - Incorporates retrieved memories into the system prompt
   - Provides context for more informed responses

5. **LLM Integration** (`chat_with_groq()`)
   - Sends messages to Groq's llama-3.3-70b-versatile model
   - Manages temperature and token limits

6. **Memory Persistence** (`store_memory()`)
   - Stores user input and assistant responses in Mem0
   - Enables learning over time

## Setup

### 1. Install Dependencies

```bash
uv add groq mem0ai python-dotenv
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

```bash
python chatbot.py
```

## Usage

```
🤖 Initializing Chatbot with Memory...

✅ Chatbot initialized successfully!
👤 User ID: abdullah_01
📝 Type 'quit' or 'exit' to end the conversation

👤 You: What can you do?

🔍 Searching memories...
🤖 Generating response...

🤖 Assistant: I'm a stateful AI assistant powered by Groq and Mem0. I can help you with...
💾 Memory stored successfully

👤 You: quit

👋 Goodbye! Your memories have been saved.
```

## Key Features Explained

### 🧠 Memory System

- **Before Each Response**: The chatbot searches Mem0 for relevant memories based on your input
- **Context Injection**: Retrieved memories are included in the system prompt to provide context
- **After Each Response**: User input and assistant response are stored in Mem0 for future recall
- **User ID**: Fixed as `"abdullah_01"` to maintain consistent memory associations

### 💬 Conversation Loop

- Maintains conversation history within the session (limited to last 20 exchanges for efficiency)
- Ends gracefully when user types `'quit'` or `'exit'`
- Handles errors gracefully with informative messages

### ⚡ Performance

- Uses Groq's fast inference server
- Model: `llama-3.3-70b-versatile`
- Temperature: 0.7 (balanced creativity and stability)
- Max tokens: 1024 per response

## Project Structure

```
chatbot-with-memory/
├── chatbot.py          # Main chatbot implementation
├── .env                # Environment variables (keep secret!)
├── pyproject.toml      # Project dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## API Models & Services

- **LLM**: Groq's llama-3.3-70b-versatile
- **Memory**: Mem0 (Long-term memory service)
- **Runtime**: Python 3.14+

## Error Handling

The chatbot includes robust error handling for:
- Missing API keys
- Memory search failures
- Groq API errors
- Memory storage errors
- Invalid user input

## Development

### Modular Functions

Each function has a single responsibility:
- `load_environment()` - Configuration
- `initialize_clients()` - Setup
- `search_memories()` - Memory retrieval
- `build_system_message()` - Prompt engineering
- `chat_with_groq()` - LLM interaction
- `store_memory()` - Memory persistence
- `run_chatbot()` - Main loop

### Extending the Chatbot

You can easily extend the chatbot by:
1. Adding more sophisticated memory search queries
2. Implementing custom system prompts
3. Adding user profiles beyond the fixed user_id
4. Integrating additional tools/APIs
5. Implementing conversation analytics

## Troubleshooting

### Missing API Keys
Ensure both `groq_api` and `mem0_api` are in the `.env` file

### Memory Not Being Stored
Check Mem0 API key validity and your account is within quota limits

### Slow Responses
- Verify Groq API connectivity
- Check your internet connection
- Consider reducing max_tokens if needed

## Future Enhancements

- [ ] Multi-user support with different user IDs
- [ ] Conversation export to JSON/text
- [ ] Memory analytics dashboard
- [ ] Custom system prompts per user
- [ ] Rate limiting and usage tracking
- [ ] Web UI interface
- [ ] Database integration for local persistence

## License

MIT License - Feel free to use and modify!

---

**Built with** ⚡ Groq + 🧠 Mem0 + 🐍 Python
