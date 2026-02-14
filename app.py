import streamlit as st
from chatbot import (
    load_environment,
    initialize_clients,
    search_memories,
    build_system_message,
    chat_with_groq,
    store_memory,
)

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Memory Chatbot",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main container */
.stMainBlockContainer {
    max-width: 820px;
    padding-top: 2rem;
}

/* Header */
.chat-header {
    text-align: center;
    padding: 1.5rem 0 1rem;
}
.chat-header h1 {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}
.chat-header p {
    opacity: 0.55;
    font-size: 0.92rem;
}

/* Chat messages */
.stChatMessage {
    border-radius: 16px !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 0.5rem !important;
    border: 1px solid rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(12px);
}

/* Status badges */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
}
.badge-memory {
    background: rgba(102, 126, 234, 0.15);
    color: #667eea;
}
.badge-stored {
    background: rgba(72, 187, 120, 0.15);
    color: #48bb78;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(17, 17, 27, 0.6);
    backdrop-filter: blur(20px);
}
section[data-testid="stSidebar"] .stMarkdown h1 {
    font-size: 1.15rem;
    font-weight: 600;
}

/* Chat input */
.stChatInput > div {
    border-radius: 14px !important;
    border: 1px solid rgba(102, 126, 234, 0.3) !important;
    transition: border-color 0.2s;
}
.stChatInput > div:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.15) !important;
}

/* Spinner */
.stSpinner > div > div {
    border-top-color: #667eea !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ─── Init Session State ────────────────────────────────────────
def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "clients_ready" not in st.session_state:
        try:
            groq_api, mem0_api = load_environment()
            groq_client, mem0_client = initialize_clients(groq_api, mem0_api)
            st.session_state.groq_client = groq_client
            st.session_state.mem0_client = mem0_client
            st.session_state.clients_ready = True
        except Exception as e:
            st.error(f"❌ Failed to initialize: {e}")
            st.stop()


init_state()

USER_ID = "abdullah_01"


# ─── Smart Memory Filter ───────────────────────────────────────
def is_worth_remembering(groq_client, user_input: str, response: str) -> bool:
    """Use the LLM to decide if this exchange is worth storing in long-term memory."""
    try:
        judgement = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a memory-importance classifier. "
                        "Given a user message and an assistant reply, decide whether the exchange "
                        "contains information worth saving to long-term memory.\n\n"
                        "Save-worthy examples: personal facts, preferences, project details, "
                        "technical decisions, goals, feedback, or anything the user might want "
                        "the assistant to remember later.\n\n"
                        "NOT save-worthy: greetings (hi, hello, hey), small-talk (how are you), "
                        "thanks/goodbye, trivial one-word responses, or purely generic Q&A "
                        "with no personal context.\n\n"
                        "Reply with EXACTLY one word: SAVE or SKIP"
                    ),
                },
                {
                    "role": "user",
                    "content": f"User: {user_input}\nAssistant: {response}",
                },
            ],
            temperature=0,
            max_tokens=4,
        )
        verdict = judgement.choices[0].message.content.strip().upper()
        return "SAVE" in verdict
    except Exception:
        # If the classifier fails, save anyway to be safe
        return True

# ─── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🧠 Memory Chatbot")
    st.caption("Powered by Groq + Mem0")
    st.divider()

    auto_memory = st.toggle("💾 Smart memory", value=True)
    st.caption(
        "When enabled, important exchanges are automatically saved. Trivial messages like greetings are skipped."
    )

    st.divider()

    st.markdown(f"**👤 User:** `{USER_ID}`")
    st.markdown("**⚡ Model:** `llama-3.3-70b-versatile`")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.rerun()

    st.divider()
    st.caption("Built with ⚡ Groq + 🧠 Mem0 + 🎈 Streamlit")

# ─── Header ────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown(
        """
    <div class="chat-header">
        <h1>🧠 Memory Chatbot</h1>
        <p>Ask me anything — I remember our past conversations.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ─── Render Message History ───────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧠" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# ─── Chat Input ────────────────────────────────────────────────
if prompt := st.chat_input("Type your message…"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant", avatar="🧠"):
        # Search memories
        with st.spinner("🔍 Searching memories…"):
            memories = search_memories(
                st.session_state.mem0_client, prompt, USER_ID
            )

        if memories:
            st.markdown(
                f'<span class="status-badge badge-memory">🧠 {len(memories)} memor{"y" if len(memories) == 1 else "ies"} found</span>',
                unsafe_allow_html=True,
            )

        # Build messages
        system_message = build_system_message(memories)
        messages = [
            {"role": "system", "content": system_message},
            *st.session_state.conversation_history,
            {"role": "user", "content": prompt},
        ]

        # Get LLM response
        with st.spinner("✨ Thinking…"):
            response = chat_with_groq(st.session_state.groq_client, messages)

        st.markdown(response)

        # Smart memory storage
        if auto_memory:
            if is_worth_remembering(st.session_state.groq_client, prompt, response):
                store_memory(st.session_state.mem0_client, prompt, response, USER_ID)
                st.markdown(
                    '<span class="status-badge badge-stored">💾 Memory saved</span>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<span class="status-badge" style="background:rgba(160,160,160,0.12);color:#999;">⏭️ Trivial — not saved</span>',
                    unsafe_allow_html=True,
                )

    # Save to session
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_history.append(
        {"role": "user", "content": prompt}
    )
    st.session_state.conversation_history.append(
        {"role": "assistant", "content": response}
    )

    # Keep history manageable
    if len(st.session_state.conversation_history) > 20:
        st.session_state.conversation_history = (
            st.session_state.conversation_history[-20:]
        )
