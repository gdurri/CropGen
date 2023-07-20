#
# Main application entry point.
#

# Imports
import asyncio
import logging

from lib.logging.logger_config import LoggerConfig
from lib.server.socket_server import SocketServer
from lib.server.server_state import ServerState
from lib.config.config import Config
from lib.docker.docker_helper import DockerHelper

config = Config()
server_state = ServerState()
docker_helper = DockerHelper()

# Functions
def client_connected_cb(client_reader, client_writer):
    server = SocketServer(config, server_state)
    server.client_connected_callback(client_reader, client_writer)

def log_app_startup():
    logging.info("Started CropGen application")
    if config.is_running_in_docker:
        image_info = docker_helper.get_image_info()
        if image_info:
            logging.info("Docker Info: %s", image_info)

    logging.info("Service Config: %s", config.to_json(config.pretty_print_json_in_logs))
    

# Main entry point
if __name__ == "__main__":

    try:
        logger_config = LoggerConfig(config)
        logger_config.setup_logger()

        log_app_startup()

        loop = asyncio.get_event_loop()
        server_coro = asyncio.start_server(
            client_connected_cb,
            host=config.socket_server_host,
            port=config.socket_server_port
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
        logging.info("Closing CropGen application")
    except:
        logging.exception("Exception - CropGen Main Application catch handler")
