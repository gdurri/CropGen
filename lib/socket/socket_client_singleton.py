#
# A socket client singleton.
#
class SocketClientSingleton:

    def __new__(self, socket_client):
        self.instance = None

        if self.instance is None:
            self.socket_client = socket_client
            self.instance = super(SocketClientSingleton, self).__new__(self)
        return self.instance

    @classmethod
    def get_instance(self):
        if self.instance is None:
            self.instance = self()
        return self.instance
    
    #
    # Connects to the specified end point.
    #
    def connect(self, host, port):
        self.socket_client.connect(host, port)

    #
    # Sends a message
    #
    def write_text(self, message):
        self.socket_client.write_text(message)

    
    #
    # Reads a message
    #
    def read_text(self):
        return self.socket_client.read_text()
