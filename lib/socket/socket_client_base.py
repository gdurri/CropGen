from abc import abstractmethod

from lib.logging.logger import Logger

#
# An abstract socket client base class.
#
class SocketClientBase():
    #
    # Constructor
    #
    def __init__(self, config, raw_socket):
        self.config = config
        self.logger = Logger()
        self.raw_socket = raw_socket

    #
    # Connect method
    #
    @abstractmethod
    async def connect(self):
        pass

    #
    # Disconnect method
    #
    @abstractmethod
    async def disconnect(self):
        pass

    #
    # Send data method
    #
    @abstractmethod
    async def send_text(self, data):
        pass

    #
    # Send error method
    #
    @abstractmethod
    async def send_error(self, data):
        pass

    #
    # Receive data method
    #
    @abstractmethod
    async def receive_text(self):
        pass
