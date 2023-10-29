#
# A class that wraps around a socket write.
#
class WriteMessageData:
    def __init__(self, message_size_byte_array, encoded_data):
        self.message_size_byte_array = message_size_byte_array
        self.encoded_data = encoded_data