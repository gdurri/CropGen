from lib.cgm_server.cgm_client import CGMClient
from lib.cgm_server.cgm_client_mock import CGMClientMock

#
# Factory class for creating CGM Clients, depending on the config.
#
class CGMClientFactory():

    #
    # Creates an instance of a CGM Client.
    #
    def create(self, config):
        if config.use_mock_cgm_client:
            return CGMClientMock(config)
        else:
            return CGMClient(config)
