from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Header, HTTPException
import firebase_admin
from firebase_admin import auth, credentials
import json

# Initialize Firebase (You'll need your serviceAccountKey.json)
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

app = FastAPI()

# Map of { user_id: WebSocket }
active_connections = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket
    print(f"PC Connected: {user_id}")
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        del active_connections[user_id]
        print(f"PC Disconnected: {user_id}")

@app.post("/send_msg")
async def handle_mobile_command(request_data: dict, authorization: str = Header(None)):
    # 1. Verify Firebase Token from Phone
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Token")
    
    token = authorization.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")

    # 2. Check if the PC for THIS user is online
    if uid not in active_connections:
        return {"reply": "Your PC is currently offline."}

    # 3. Push command to PC
    pc_socket = active_connections[uid]
    await pc_socket.send_json({"message": request_data["message"]})
    
    # In a real app, you'd wait for the PC to send a response back here
    return {"reply": "Command sent to your PC!"}