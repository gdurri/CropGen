import uvicorn
from fastapi import FastAPI, WebSocket
from lib.MessageProcessing.message_processor import MessageProcessor
from lib.Logging.results_logger import ResultsLogger

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
    ResultsLogger._remove_and_create_results_folder()
    uvicorn.run("main:app")