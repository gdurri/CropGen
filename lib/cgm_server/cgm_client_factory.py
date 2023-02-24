from lib.cgm_server.cgm_client import CGMClient

#
# Factory class for creating CGM Clients, depending on the config.
#
class CGMClientFactory():

    #
    # Creates an instance of a CGM Client.
    #
    def create(self, config):
        return CGMClient(config)
