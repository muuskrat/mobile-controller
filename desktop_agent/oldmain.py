from dotenv import load_dotenv
load_dotenv()

from graph import compiled_graph

## MAKE SURE TO ADD MESSAGE PRUNING SO TOKENS DONT GET OUT OF CONTROL ON LONG CONVERSATIONS
def run_chat():
    print("--- App Suite Loaded ---")
    session_messages = []
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]: break
        
        inputs = {"messages": session_messages + [("user", user_input)]}
        final_state = None
        for s in compiled_graph.stream(inputs, stream_mode="values"):
            final_state = s
        
        if final_state:
            session_messages = final_state["messages"]
            print(f"\nAI: {session_messages[-1].content}")

if __name__ == "__main__":
    run_chat()