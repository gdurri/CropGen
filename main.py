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
# Construct and parse the config. This gets passed around to minimise the
# amount of file reading we do.
config = Config()


# Web socket endpoints - All Comms expects JSON.

# Run endpoint
@app.websocket("/cropgen/run")
async def test(websocket: WebSocket):
    await websocket.accept()
    message_processor = MessageProcessor(config, websocket)

    while True:
        request = await websocket.receive_text()
        await message_processor.process_run_message(request)


# Main entry point
if __name__ == "__main__":
    # Run the web server.
    uvicorn.run(
        "main:app", 
        port=config.socket_server_port,
        reload=True,
        log_level=config.web_server_log_level
    )