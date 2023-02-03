from lib.jobs_server.jobs_server_client import JobsServerClient
from lib.jobs_server.jobs_server_client_mock import JobsServerClientMock


class JobsServerClientFactory():

    def _create(self, config):
        if config.use_mock_job_server_client:
            return JobsServerClientMock(config)
        else:
            return JobsServerClient(config)
