import uvicorn
from fastapi import FastAPI, WebSocket
from lib.message_processor import MessageProcessor
from lib.results_logger import ResultsLogger

app = FastAPI()
message_processor = MessageProcessor()
ResultsLogger._remove_and_create_results_folder()


# Endpoints
@app.websocket("/cropgen/run")
async def test(websocket: WebSocket):
    await websocket.accept()
    while True:
        request = await websocket.receive_text()
        await message_processor._process_run_message(request, websocket)


if __name__ == "__main__":
    uvicorn.run("main:app")