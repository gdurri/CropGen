from lib.cgm_server.cgm_client import CGMClient

#
# Factory class for creating CGM Clients, depending on the config.
#
class CGMClientFactory():

    #
    # Creates an instance of a CGM Client.
    #
    @staticmethod
    def create(host, port, config):
        return CGMClient(host, port, config)
