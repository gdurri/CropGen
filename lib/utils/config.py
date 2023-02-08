import json
import os

#
# The config for this application.
#
class Config:
    # The environment variable that is created only when running in docker.
    RUNNING_IN_DOCKER_ENV = 'RUNNING_IN_DOCKER'

    #
    # Constructor.
    #
    def __init__(self):
        self.data = self._parse()
        self._populate_from_data()

    #
    # Parses the config JSON file and stores it in memory.
    #
    def _parse(self):
        relative_path = '../../config/config.json'
        current_script_dir = os.path.dirname(os.path.realpath(__file__))
        config_file_full_path = os.path.join(current_script_dir, relative_path)

        with open(config_file_full_path) as json_config_file:
            data = json.load(json_config_file)

        return data

    #
    # Populates itself using the config JSON data.
    #
    def _populate_from_data(self):
        self.wgp_end_point = self._get_config_setting('wgpEndPoint')
        self.use_mock_wgp_client = self._get_config_setting('useMockWgpClient')
        self.reverse_mocked_results = self._get_config_setting('reverseMockedResults')
        self.socket_server_port = self._get_config_setting('socketServerPort')
        self.web_server_log_level = self._get_config_setting('webServerLogLevel')

    #
    # Safely gets a config setting, taking into consideration docker
    # and defaults if it isn't present.
    #
    def _get_config_setting(self,
                            config_key,
                            check_for_docker=False,
                            value_if_docker=None):
        if not check_for_docker:
            return self.data[config_key]

        if self._is_running_in_docker():
            return value_if_docker

        return self.data[config_key]

    #
    # Checks if we are running in docker, using the env var.
    #
    def _is_running_in_docker(self):
        return os.environ.get(Config.RUNNING_IN_DOCKER_ENV, False)
