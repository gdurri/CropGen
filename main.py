import asyncio
import websockets
from lib.config import Config
from lib.logger import Logger
from lib.message_processor import MessageProcessor

message_processor = MessageProcessor()


async def message_handler(websocket, path):
    data = await websocket.recv()
    response = message_processor._process_message(data)
    await websocket.send(response)


# Main
if __name__ == "__main__":
    config = Config()
    logger = Logger()

    start_server = websockets.serve(message_handler, config.socket_server_ip,
                                    config.socket_server_port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()