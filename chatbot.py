import os
import warnings
from dotenv import load_dotenv
import groq
import mem0

# Suppress deprecation warnings from third-party libraries
warnings.filterwarnings("ignore", category=DeprecationWarning, module="backoff")


def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()
    groq_api = os.getenv("groq_api")
    mem0_api = os.getenv("mem0_api")

    if not groq_api or not mem0_api:
        raise ValueError("Missing required API keys: groq_api or mem0_api")

    return groq_api, mem0_api


def initialize_clients(groq_api: str, mem0_api: str):
    """Initialize Groq and Mem0 clients."""
    groq_client = groq.Groq(api_key=groq_api)
    mem0_client = mem0.MemoryClient(api_key=mem0_api)
    return groq_client, mem0_client


def search_memories(mem0_client, user_input: str, user_id: str = "abdullah_01"):
    """Search for relevant memories based on user input."""
    try:
        # Use filters parameter as required by Mem0 API v2
        results = mem0_client.search(query=user_input, filters={"user_id": user_id})
        # Extract memory text from results
        memories = []
        if results and isinstance(results, list):
            for result in results:
                if isinstance(result, dict) and "memory" in result:
                    memories.append(result["memory"])
        return memories
    except Exception as e:
        print(f"⚠️  Memory search error: {e}")
        return []


def build_system_message(memories: list) -> str:
    """Build system message with memory context."""
    base_message = "You are a helpful and knowledgeable assistant. "

    if memories:
        memory_context = "\n".join(memories)
        return f"{base_message}\nRelevant context from previous interactions:\n{memory_context}"

    return base_message


def chat_with_groq(groq_client, messages: list) -> str:
    """Send message to Groq and get response."""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def store_memory(
    mem0_client, user_input: str, response: str, user_id: str = "abdullah_01"
):
    """Store user input and response in memory."""
    try:
        # Store user message and assistant response as proper message format
        messages = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response},
        ]
        mem0_client.add(messages=messages, user_id=user_id)
        print("💾 Memory stored successfully")
    except Exception as e:
        print(f"⚠️  Memory storage error: {e}")


def run_chatbot():
    """Main chatbot loop."""
    print("🤖 Initializing Chatbot with Memory...\n")

    # Load environment variables
    groq_api, mem0_api = load_environment()

    # Initialize clients
    groq_client, mem0_client = initialize_clients(groq_api, mem0_api)
    user_id = "abdullah_01"

    print(f"✅ Chatbot initialized successfully!")
    print(f"👤 User ID: {user_id}")
    print("📝 Type 'quit' or 'exit' to end the conversation\n")
    print("-" * 60)

    conversation_history = []

    while True:
        # Get user input
        user_input = input("\n👤 You: ").strip()

        # Check for exit commands
        if user_input.lower() in ["quit", "exit"]:
            print("\n👋 Goodbye! Your memories have been saved.")
            break

        if not user_input:
            print("⚠️  Please enter a message.")
            continue

        # Search for relevant memories
        print("\n🔍 Searching memories...")
        memories = search_memories(mem0_client, user_input, user_id)

        # Build system message with memory context
        system_message = build_system_message(memories)

        # Build messages for Groq
        messages = [
            {"role": "system", "content": system_message},
            *conversation_history,
            {"role": "user", "content": user_input},
        ]

        # Get response from Groq
        print("🤖 Generating response...")
        try:
            response = chat_with_groq(groq_client, messages)

            # Display response
            print(f"\n🤖 Assistant: {response}")

            # Ask user if they want to store this in memory
            print("\n💾 Store this exchange in memory for future reference?")
            while True:
                save_choice = input("   (yes/no): ").strip().lower()
                if save_choice in ["yes", "y"]:
                    store_memory(mem0_client, user_input, response, user_id)
                    break
                elif save_choice in ["no", "n"]:
                    print("⏭️  Skipped memory storage")
                    break
                else:
                    print("   ⚠️  Please enter 'yes' or 'no'")

            # Update conversation history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": response})

            # Keep conversation history manageable (last 10 exchanges)
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]

        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Entry point."""
    try:
        run_chatbot()
    except KeyboardInterrupt:
        print("\n\n👋 Chatbot interrupted by user.")
    except Exception as e:
        print(f"❌ Fatal error: {e}")


if __name__ == "__main__":
    main()
