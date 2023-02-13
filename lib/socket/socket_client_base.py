from abc import abstractmethod

#
# An abstract socket client base class.
#
class SocketClientBase():
    #
    # Constructor
    #
    def __init__(self, raw_socket):
        self.raw_socket = raw_socket

    #
    # Connect method
    #
    @abstractmethod
    def connect(self):
        pass

    #
    # Connect method
    #
    @abstractmethod
    async def connect_async(self):
        pass

    #
    # Send data method
    #
    @abstractmethod
    def send_text(self, data):
        pass

    #
    # Send data method
    #
    @abstractmethod
    async def send_text_async(self, data):
        pass

    #
    # Send error method
    #
    @abstractmethod
    async def send_error(self, data):
        pass

    #
    # Send error method
    #
    @abstractmethod
    async def send_error_async(self, data):
        pass

    #
    # Receive data method
    #
    @abstractmethod
    async def receive_text(self):
        pass

    #
    # Receive data method
    #
    @abstractmethod
    async def receive_text_async(self):
        pass
