from lib.socket.socket_client_base import SocketClientBase
from lib.models.error_message import ErrorMessage

#
# A websocket client.
#
class WebSocketClient(SocketClientBase):
    #
    # Constructor
    #
    def __init__(self, config, raw_socket):
        super().__init__(config, raw_socket)

    #
    # Connect method
    #
    async def connect(self):
        await self.raw_socket.accept()

    #
    # Disconnect method
    #
    async def disconnect(self):
        pass

    #
    # Send data method
    #
    async def send_text(self, data):
        await self.raw_socket.send_text(data)

    #
    # Send data method
    #
    async def send_error(self, errors):
        await self.send_text(ErrorMessage(errors).to_json())

    #
    # Receive data method
    #
    async def receive_text(self):
        return await self.raw_socket.receive_text()
