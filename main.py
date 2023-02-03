import uvicorn
from fastapi import FastAPI, WebSocket
from lib.message_processing.message_processor import MessageProcessor
from lib.utils.config import Config


app = FastAPI()


# Endpoints
@app.websocket("/cropgen/run")
async def test(websocket: WebSocket):
    await websocket.accept()
    message_processor = MessageProcessor(websocket)

    while True:
        request = await websocket.receive_text()
        await message_processor._process_run_message(request)


if __name__ == "__main__":
    config = Config()
    uvicorn.run(
        "main:app", 
        port=config.socket_server_port,
        reload=True,
        log_level="info"
    )