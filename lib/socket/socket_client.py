import asyncio

from lib.socket.socket_client_base import SocketClientBase
from lib.models.error_message import ErrorMessage

#
# A websocket client.
#
class SocketClient(SocketClientBase):
    ENCODING = 'utf-8'
    LITTLE_ENDIAN = "little"

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
        #client_reader, client_writer = yield from asyncio.open_connection("host", 9999)
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
        # Send the length of the encoded data as a byte array.
        message_size_byte_array = len(data).to_bytes(4, SocketClient.LITTLE_ENDIAN)
        self.writer.write(message_size_byte_array)
        # Now send the data.
        self.writer.write(data.encode(SocketClient.ENCODING))
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
    async def receive_text_async(self, encoding=ENCODING):
        # Read the message size byte array that proceeds each message.
        message_size_byte_array = await self.reader.read(4)
        # Convert it to an integer and then use this to read the message itself
        # with the known size.
        message_size_bytes = int.from_bytes(message_size_byte_array, SocketClient.LITTLE_ENDIAN)
        message_data = await self.reader.readexactly(message_size_bytes)

        # If it is an empty message, this is our disconnect message so don't decode it.
        if message_data == b'':
            return message_data
        
        # It's not a disconnect to decode it.
        return message_data.decode(encoding)