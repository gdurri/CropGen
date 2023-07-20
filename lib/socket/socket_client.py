import logging
import socket

from lib.socket.socket_client_base import SocketClientBase
from lib.models.run.error_message import ErrorMessage

#
# A socket client.
#
class SocketClient (SocketClientBase):

    #
    # Constructor
    #
    def __init__(self, config):
        super().__init__(config)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #
    # Connects
    #
    def connect(self, host, port):
        try:
            self.socket.connect((host, port))
        except ConnectionRefusedError:
            logging.error("Connection refused: Failed to connect to %s:%s", host, port)
            raise

    #
    # Sets the timeout
    #
    def set_timeout(self, timeout_seconds):
        # Only apply the timeout if one has been configured and it is greater than the default of 0.
        if timeout_seconds > 0:
            try:
                self.socket.settimeout(timeout_seconds)
            except socket.error as e:
                logging.error("Socket timeout error: %s", str(e))
                raise

    #
    # Writes data
    #
    def write_text(self, message):
        prepare_data = super().prepare_data_for_write(message)
        try:
            self.socket.sendall(prepare_data.message_size_byte_array)
            self.socket.sendall(prepare_data.encoded_data)
        except socket.error as e:
            logging.error("Socket write error: %s", str(e))
            raise

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
        try:
            message_size_bytes = self.read_message_size_int()
            logging.info("%s - Received message size: '%d' bytes", self.__class__.__name__, message_size_bytes)
            message_data = self.read_data(message_size_bytes)
            return super().create_message_wrapper(message_data)
        except socket.error as e:
            logging.error("Socket read error: %s", str(e))
            raise

    
    def read_message_size_int(self):
        data = b''
        bytes_to_receive = self.config.socket_data_num_bytes_buffer_size

        while len(data) < bytes_to_receive:
            chunk = self.socket.recv(bytes_to_receive - len(data))
            if not chunk:
                # Connection closed prematurely
                logging.warning(
                    "%s - Connection closed prematurely. Expected %d bytes, received %d bytes.",
                    __class__.__name__, bytes_to_receive, len(data)
                )
                return 0

            data += chunk

        # Convert the received bytes to an integer
        received_int = int.from_bytes(data, byteorder=self.config.socket_data_endianness)

        return received_int

    #
    # Reads the data
    #
    def read_data(self, message_size_bytes):
        # Initialize our buffer
        message_data = bytearray()

        # Now iterate calling receive each time until we've read all of the data.
        buffer_pos = 0
        while buffer_pos < message_size_bytes:
            remaining_bytes = message_size_bytes - buffer_pos
            read_data = self.socket.recv(min(self.config.socket_receive_buffer_size, remaining_bytes))
            read_data_length = len(read_data)
            if read_data_length == 0:
                # The connection was closed prematurely
                logging.warning(
                    "%s - Connection closed prematurely. Expected %d bytes, received %d bytes.",
                    __class__.__name__, message_size_bytes, buffer_pos
                )
                return bytearray()  # Return an empty byte array

            message_data += read_data
            buffer_pos += read_data_length

        logging.debug("%s - Finished reading message. Message Size Bytes: '%d'", __class__.__name__, message_size_bytes)

        return message_data
