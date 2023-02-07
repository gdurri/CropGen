from lib.wgp_server.wgp_server_client import WGPServerClient
from lib.wgp_server.wgp_server_client_mock import WGPServerClientMock

#
# Factor class for creating WGP Server Clients, depending on the config.
#
class WGPServerClientFactory():

    #
    # Creates an instance of a WGP Server Client.
    #
    def create(self, config):
        if config.use_mock_wgp_server_client:
            return WGPServerClientMock(config)
        else:
            return WGPServerClient(config)
