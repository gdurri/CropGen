import asyncio

from lib.server.socket_message_handler import SocketMessageHandler
from lib.logging.logger import Logger

#
# A socket server that handles incoming requests from clients.
#
class SocketServer():

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
        self.logger = Logger()

    #
    # Callback which is invoked when a client is connecting to this server.
    #
    def client_connected_callback(self, client_reader, client_writer):
        task = asyncio.ensure_future(
            self.client_listener(client_reader, client_writer)
        )
    
    #
    # Handles listening to the connected client and processing any messages.
    #
    async def client_listener(self, reader, writer):
        client_addr = writer.get_extra_info('peername')
        self.logger.log_debug(f'Connected to client {client_addr}. Waiting for commands')

        while True:
            data = await reader.read(self.config.socket_receive_buffer_size)
            if data == b'':
                self.logger.log_debug('Received EOF. Client disconnected.')
                return
            else:
                writer.write(data)
                await writer.drain()
