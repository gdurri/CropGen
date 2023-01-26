from lib.jobs_server_client import JobsServerClient
from lib.jobs_server_client_mock import JobsServerClientMock


class JobsServerClientFactory():

    def _create(self, config, logger):
        if config.use_mock_job_server_client:
            return JobsServerClientMock(logger, config)
        else:
            return JobsServerClient(logger, config)
