import os
from dotenv import load_dotenv

# 1. LOAD THIS FIRST
load_dotenv() 

import asyncio
import websockets
import json
import time

# 2. NOW IMPORT THE GRAPH (It will now see the API key)
from graph import compiled_graph

# Use a .env or config file to store your unique User ID
USER_ID = "ovVLHZWFm6cWaxNCZS1UqJn246Q2" 
# When deployed, this will be wss://your-app.render.com/ws/
BACKEND_WS_URL = f"wss://mobile-controller.onrender.com/ws/{USER_ID}"

async def run_agent():
    while True: # Infinite loop to keep it "Always On"
        try:
            print(f"Connecting to Cloud Middleman...")
            async with websockets.connect(BACKEND_WS_URL) as websocket:
                print("Connection established. Waiting for commands...")
                
                while True:
                    # Listen for commands from the Cloud
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    print(f"Received: {data['message']}")
                    
                    # Run through your LangGraph tools
                    inputs = {"messages": [("user", data['message'])]}
                    result = compiled_graph.invoke(inputs)
                    
                    # Optional: Send the result back to the phone
                    response = result["messages"][-1].content
                    await websocket.send(json.dumps({"reply": response}))
                    
        except Exception as e:
            print(f"Connection lost: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5) # Wait before trying to reconnect

if __name__ == "__main__":
    asyncio.run(run_agent())