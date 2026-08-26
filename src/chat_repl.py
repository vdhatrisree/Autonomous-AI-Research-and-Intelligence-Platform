from memory.db import init_db
from memory.recall import get_all_sessions
from chat.session_context import load_session_context
from chat.chat_engine import chat_respond

init_db()
sessions = get_all_sessions()

if not sessions:
    print("No past research sessions found. Run main_agentic.py first.")
    exit()

print("Past research sessions:")
for s in sessions[:10]:
    print(f"  [{s['id']}] {s['question']} ({s['created_at']})")

session_id = int(input("\nEnter a session ID to chat about: "))
context = load_session_context(session_id)

if context is None:
    print("Session not found.")
    exit()

print(f"\nChatting about: \"{context['question']}\"")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ("exit", "quit"):
        break
    response = chat_respond(user_input, context)
    print(f"Bot: {response}\n")

