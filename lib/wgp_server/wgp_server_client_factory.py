from lib.wgp_server.wgp_server_client import WGPServerClient
from lib.wgp_server.wgp_server_client_mock import WGPServerClientMock


class WGPServerClientFactory():

    def _create(self, config):
        if config.use_mock_wgp_server_client:
            return WGPServerClientMock(config)
        else:
            return WGPServerClient(config)
