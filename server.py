from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

clients:list[WebSocket] = []

@app.get('/')
async def hello_endpoint():
    return {'response': 'hi there!!!'}

@app.websocket("/broadcast")
async def hello_endpoint(websocket:WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print('client connected')

    try:
        while True:
            message:str = await websocket.receive_text()
            target_clients = [client for client in clients if client is not websocket]
            for client in target_clients:
                await client.send_text(message)
    except WebSocketDisconnect:
        clients.remove(websocket)
        print('client disconnected.')