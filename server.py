from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

clients:list[WebSocket] = []

def global_path(local_path:str):
    return f'store/{local_path}'

@app.get('/')
async def hello_endpoint():
    return {'response': 'hi there!!!'}

@app.post('/upload')
async def upload_endpoint(file:UploadFile):
    with open(global_path(file.filename), 'wb') as output_file:
        output_file.write(file.file.read())
    return { 'response': file.filename }

@app.get('/store')
async def store_endpoint(path:str):
    return FileResponse(global_path(path))

@app.websocket("/broadcast")
async def hello_endpoint(websocket:WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            message:str = await websocket.receive_text()
            target_clients = [client for client in clients if client is not websocket]
            for client in target_clients:
                await client.send_text(message)
    except WebSocketDisconnect:
        clients.remove(websocket)