from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel

app = FastAPI()

# This dictionary stores: { "user_id": websocket_connection }
active_pcs = {}

class CommandRequest(BaseModel):
    user_id: str
    command: str
    payload: dict = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_pcs[user_id] = websocket
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        del active_pcs[user_id]

@app.post("/send-command")
async def send_command(req: CommandRequest):
    if req.user_id not in active_pcs:
        raise HTTPException(status_code=404, detail="PC not online")
    
    # Push the command to the specific PC's websocket
    target_socket = active_pcs[req.user_id]
    await target_socket.send_json({
        "command": req.command,
        "payload": req.payload
    })
    return {"status": "success"}