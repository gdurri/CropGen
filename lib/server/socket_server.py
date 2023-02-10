import asyncio
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
        asyncio.ensure_future(
            self.client_listener(client_reader, client_writer)
        )
    
    #
    # Handles listening to the connected client and processing any messages.
    #
    async def client_listener(self, reader, writer):
        client_addr = writer.get_extra_info('peername')
        self.logger.raw_logger.debug('Connected to client %s. Waiting for commands', client_addr)

        while True:
            data = await reader.read(self.config.socket_receive_buffer_size)
            if data == b'':
                self.logger.raw_logger.debug('Received EOF. Client disconnected.')
                return
            else:
                writer.write(data)
                await writer.drain()
