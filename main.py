#
# Main application entry point.
#

# Imports
import asyncio
import logging
from lib.logging import set_logger_config

from lib.server.socket_server import SocketServer
from lib.server.server_state import ServerState
from lib.config.config import Config

config = Config()
server_state = ServerState()

# Functions
def client_connected_cb(client_reader, client_writer):
    server = SocketServer(config, server_state)
    server.client_connected_callback(client_reader, client_writer)

# Main entry point
if __name__ == "__main__":

    try:
        logging.debug("Started CropGen application")
        logging.info("Service Config: %s", config.to_json())

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
        logging.debug("Closing CropGen application")
    except:
        logging.exception("Exception - CropGen Main Application catch handler")
