from lib.wgp_server.wgp_client import WGPClient
from lib.wgp_server.wgp_client_mock import WGPClientMock

#
# Factory class for creating WGP Clients, depending on the config.
#
class WGPClientFactory():

    #
    # Creates an instance of a WGP Client.
    #
    def create(self, config):
        if config.use_mock_wgp_client:
            return WGPClientMock(config)
        else:
            return WGPClient(config)
