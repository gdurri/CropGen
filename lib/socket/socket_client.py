import socket

from lib.models.error_message import ErrorMessage

#
# A websocket client.
#
class SocketClient():

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config
        self.socket = socket.socket()

    #
    # Connects
    #
    def connect(self, host, port):
        self.socket.connect((host, port))

    #
    # Writes data
    #
    def write_text(self, data):
        # Send the length of the encoded data as a byte array.
        message_size_byte_array = len(data).to_bytes(4, self.config.socket_data_endianness)
        self.socket.sendall(message_size_byte_array)
        # Now send the data.
        self.socket.sendall(data.encode(self.config.socket_data_encoding))

    #
    # Writes a serialised error message.
    #
    def write_error(self, errors):
        self.write_text_async(ErrorMessage(errors).to_json())

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