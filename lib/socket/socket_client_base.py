from lib.models.message_wrapper import MessageWrapper

#
# A socket client base class.
#
class SocketClientBase:

    MESSAGE_WRAPPER_TUPLE_MESSAGE_SIZE_INDEX = 0
    MESSAGE_WRAPPER_TUPLE_ENCODED_DATA = 1

    #
    # Constructor
    #
    def __init__(self, config):
        self.config = config

    #
    # Constructs a message wrapper.
    #
    def construct_message_wrapper(self, type_name, type_body):
        message = MessageWrapper(type_name, type_body)
        data = message.to_json()

        # Send the length of the encoded data as a byte array.
        message_size_byte_array = len(data).to_bytes(
            self.config.socket_data_num_bytes_buffer_size, 
            self.config.socket_data_endianness
        )

        return (message_size_byte_array, data.encode(self.config.socket_data_encoding))
