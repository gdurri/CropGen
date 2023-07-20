import asyncio
import logging

from lib.socket.socket_client_async import SocketClientAsync
from lib.message_processing.message_processor import MessageProcessor

#
# A socket server that handles incoming requests from clients.
#
class SocketServer():

    #
    # Constructor
    #
    def __init__(self, config, server_state):
        self.config = config
        self.server_state = server_state

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
        socket_client = SocketClientAsync(self.config, reader, writer)
        client_address = writer.get_extra_info('peername')
        logging.debug("Connected to client '%s'. Waiting for commands", client_address)

        while True:
            read_message_data = await socket_client.read_text_async()

            if read_message_data.is_disconnect_message:
                logging.debug("Disconnected from '%s'", client_address)
                return
            else:
                message_processor = MessageProcessor(self.config, socket_client, self.server_state)
                await message_processor.process_message(read_message_data)
