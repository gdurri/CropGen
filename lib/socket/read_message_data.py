#
# A class that wraps around a socket read.
#
class ReadMessageData:
    def __init__(self, errors, message_wrapper, is_disconnect_message = False):
        self.errors = errors
        self.message_wrapper = message_wrapper
        self.is_disconnect_message = is_disconnect_message