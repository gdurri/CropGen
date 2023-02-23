import socket

from lib.socket.socket_client_base import SocketClientBase
from lib.models.error_message import ErrorMessage

#
# A socket client.
#
class SocketClient (SocketClientBase):

    #
    # Constructor
    #
    def __init__(self, config):
        super().__init__(config)
        self.socket = socket.socket()

    #
    # Connects
    #
    def connect(self, host, port):
        self.socket.connect((host, port))

    #
    # Writes data
    #
    def write_text(self, message):
        prepare_data = super().prepare_data_for_write(message)
        # Send the length of the encoded data as a byte array.
        self.socket.sendall(prepare_data.message_size_byte_array)
        # Now send the data.
        self.socket.sendall(prepare_data.encoded_data)

    #
    # Writes a serialised error message.
    #
    def write_error(self, errors):
        error_message = ErrorMessage(errors) 
        self.write_text(error_message)

    #
    # Reads data
    #
    def read_text(self):
        # Read the message size byte array that proceeds each message.
        message_size_byte_array = self.socket.recv(self.config.socket_data_num_bytes_buffer_size)
        # Convert it to an integer and then use this to read the message itself
        # with the known size.
        message_size_bytes = int.from_bytes(message_size_byte_array, self.config.socket_data_endianness)
        message_data = self.socket.recv(message_size_bytes)

        return super().create_message_wrapper(message_data)
