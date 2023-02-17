from lib.models.error_message import ErrorMessage

#
# A websocket client.
#
class SocketClientAsync():

    #
    # Constructor
    #
    def __init__(self, config, reader, writer):
        super().__init__(None)
        self.config = config
        self.reader = reader
        self.writer = writer

    #
    # Writes data
    #
    async def write_text_async(self, data):
        # Send the length of the encoded data as a byte array.
        message_size_byte_array = len(data).to_bytes(4, self.config.socket_data_endianness)
        self.writer.write(message_size_byte_array)
        # Now send the data.
        self.writer.write(data.encode(self.config.socket_data_encoding))
        await self.writer.drain()

    #
    # Writes a serialised error message.
    #
    async def write_error_async(self, errors):
        await self.write_text_async(ErrorMessage(errors).to_json())

    #
    # Reads data
    #
    async def read_text_async(self, encoding):
        # Read the message size byte array that proceeds each message.
        message_size_byte_array = await self.reader.read(4)
        # Convert it to an integer and then use this to read the message itself
        # with the known size.
        message_size_bytes = int.from_bytes(message_size_byte_array, self.config.socket_data_endianness)
        message_data = await self.reader.readexactly(message_size_bytes)

        # If it is an empty message, this is our disconnect message so don't decode it.
        if message_data == b'':
            return message_data
        
        # It's not a disconnect to decode it.
        return message_data.decode(encoding)