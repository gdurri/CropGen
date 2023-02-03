#
# Main application entry point.
#

# Imports
import uvicorn
from fastapi import FastAPI, WebSocket
from lib.message_processing.message_processor import MessageProcessor
from lib.utils.config import Config

# Constructs the app using the Fast API
app = FastAPI()


# Web socket endpoints - All Comms expects JSON.

# Run endpoint
@app.websocket("/cropgen/run")
async def test(websocket: WebSocket):
    await websocket.accept()
    message_processor = MessageProcessor(websocket)

    while True:
        request = await websocket.receive_text()
        await message_processor._process_run_message(request)


# Main entry point
if __name__ == "__main__":
    # Construct the config as this is used to obtain the server port.
    config = Config()

    # Run the web server.
    uvicorn.run(
        "main:app", 
        port=config.socket_server_port,
        reload=True,
        log_level="info"
    )