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
    def write_text(self, type_name, type_body):
        message_wrapper = super().construct_message_wrapper(type_name, type_body)
        message_size_byte_array = message_wrapper[SocketClientBase.MESSAGE_WRAPPER_TUPLE_MESSAGE_SIZE_INDEX]
        encoded_data = message_wrapper[SocketClientBase.MESSAGE_WRAPPER_TUPLE_ENCODED_DATA]

        # Send the length of the encoded data as a byte array.
        self.socket.sendall(message_size_byte_array)
        # Now send the data.
        self.socket.sendall(encoded_data)

    #
    # Writes a serialised error message.
    #
    def write_error(self, errors):
        error_message = ErrorMessage(errors) 
        self.write_text(error_message.get_type_name(), error_message.to_json())

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

        # If it is an empty message, this is our disconnect message so don't decode it.
        if message_data == b'':
            return message_data
        
        # It's not a disconnect to decode it.
        return message_data.decode(self.config.socket_data_encoding)