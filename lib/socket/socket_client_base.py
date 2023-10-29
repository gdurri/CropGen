import logging 

from lib.models.common.message_wrapper import MessageWrapper
from lib.socket.read_message_data  import ReadMessageData
from lib.socket.write_message_data  import WriteMessageData

#
# A socket client base class.
#
class SocketClientBase:
    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config

    #
    # Prepares the data ready to write it to the socket.
    #
    def prepare_data_for_write(self, message):
        message_wrapper = MessageWrapper()
        message_wrapper.set_type_name(message.get_type_name())
        message_wrapper.set_type_body(message.to_json())
        data = message_wrapper.to_json()

        # Send the length of the encoded data as a byte array.
        message_size_byte_array = len(data).to_bytes(
            self.config.SocketDataNumBytesBufferSize, 
            self.config.SocketDataEndianness
        )

        return WriteMessageData(message_size_byte_array, data.encode(self.config.SocketDataEncoding))
    
    #
    # Takes the message and converts it into a message wrapper.
    #
    def create_message_wrapper(self, message_data):
        # If it is an empty message, this is our disconnect message so don't decode it.
        if message_data == b'':
            logging.debug("Received a disconnect message")
            return ReadMessageData([], None, True)
        
        if len(message_data) == 0:
            logging.debug("Received an empty message")
            return ReadMessageData([], None, False)
        
        decoded_message_data = message_data.decode(self.config.SocketDataEncoding)
        message_wrapper = MessageWrapper()
        errors = message_wrapper.parse_from_json_string(decoded_message_data)
        
        return ReadMessageData(errors, message_wrapper)
