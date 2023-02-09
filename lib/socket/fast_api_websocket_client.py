from lib.socket.socket_client_base import SocketClientBase
from lib.models.error_message import ErrorMessage

#
# A websocket client.
#
class FastAPIWebSocketClient(SocketClientBase):
    #
    # Constructor
    #
    def __init__(self, raw_socket):
        super().__init__(raw_socket)

    #
    # Connect method
    #
    def connect(self):
        raise NotImplementedError("connect not implemented")
    
    #
    # Connect method
    #
    async def connect_async(self):
        await self.raw_socket.accept()        

    #
    # Send data method
    #
    def send_text(self, data):
        raise NotImplementedError("send_text not implemented")

    #
    # Send data method
    #
    async def send_text_async(self, data):
        await self.raw_socket.send_text(data)

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
        return await self.raw_socket.receive_text()