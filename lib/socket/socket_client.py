from lib.socket.socket_client_base import SocketClientBase
from lib.models.error_message import ErrorMessage

#
# A websocket client.
#
class SocketClient(SocketClientBase):
    #
    # Constructor
    #
    def __init__(self, config, reader, writer):
        super().__init__(None)
        self.config = config
        self.reader = reader
        self.writer = writer

    #
    # Connect method
    #
    def connect(self):
        raise NotImplementedError("connect not implemented")
    
    #
    # Connect method
    #
    async def connect_async(self):
        raise NotImplementedError("connect_async not implemented")

    #
    # Send data method
    #
    def send_text(self, data):
        raise NotImplementedError("send_text not implemented")

    #
    # Send data method
    #
    async def send_text_async(self, data):
        self.writer.write(data.encode('ascii'))
        await self.writer.drain()

    #
    # Send data method
    #
    def send_error(self, errors):
        raise NotImplementedError("send_error not implemented")

    #
    # Send data method
    #
    async def send_error_async(self, errors):
        await self.send_text_async(ErrorMessage(errors).to_json())

    #
    # Receive data method
    #
    def receive_text(self):
        raise NotImplementedError("receive_text not implemented")

    #
    # Receive data method
    #
    async def receive_text_async(self):
        return await self.reader.read(
            self.config.socket_receive_buffer_size
        )