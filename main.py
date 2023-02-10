#
# Main application entry point.
#

# Imports
import asyncio
from lib.logging.logger import Logger

from lib.server.socket_server import SocketServer
from lib.utils.config import Config

config = Config()

# Functions
def client_connected_cb(client_reader, client_writer):
    server = SocketServer(config)
    server.client_connected_callback(client_reader, client_writer)

# Main entry point
if __name__ == "__main__":
    logger = Logger()
    logger.raw_logger.debug("Started CropGen application")

    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(
        client_connected_cb,
        host=config.socket_server_host,
        port=config.socket_server_port,
        loop=loop,
    )

    server = loop.run_until_complete(server_coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
    logger.raw_logger.debug("Closing CropGen application")
