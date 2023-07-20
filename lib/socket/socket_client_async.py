import logging

from lib.socket.socket_client_base import SocketClientBase
from lib.models.run.error_message import ErrorMessage

#
# An async socket client.
#
class SocketClientAsync(SocketClientBase):

    #
    # Constructor
    #
    def __init__(self, config, reader, writer):
        super().__init__(config)
        self.reader = reader
        self.writer = writer

    #
    # Writes data
    #
    async def write_text_async(self, message):
        prepare_data = super().prepare_data_for_write(message)
        try:
            self.writer.write(prepare_data.message_size_byte_array)
            self.writer.write(prepare_data.encoded_data)
            await self.writer.drain()
        except Exception as e:
            logging.error("Error writing data: %s", str(e))
            raise

    #
    # Writes a serialised error message.
    #
    async def write_error_async(self, errors):
        error_message = ErrorMessage(errors)
        try:
            await self.write_text_async(error_message)
        except Exception as e:
            logging.error("Error writing error message: %s", str(e))
            raise

    #
    # Reads data
    #
    async def read_text_async(self):
        try:
            message_size_byte_array = await self.reader.read(self.config.socket_data_num_bytes_buffer_size)
            message_size_bytes = int.from_bytes(message_size_byte_array, self.config.socket_data_endianness)
            logging.debug("%s - Received message size: '%d' bytes", __class__.__name__, message_size_bytes)
            message_data = await self.reader.readexactly(message_size_bytes)
            logging.debug("Socket data message received")
            return super().create_message_wrapper(message_data)
        except Exception as e:
            logging.error("Error reading data: %s", str(e))
            raise
