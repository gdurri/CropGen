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
        self.is_running_in_docker = self._is_running_in_docker()
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
        self.wgp_socket_timeout_seconds = self._get_config_setting('wgpSocketTimeoutSeconds')
        self.use_mock_wgp_client = self._get_config_setting('useMockWgpClient', False)        
        self.reverse_mocked_results = self._get_config_setting('reverseMockedResults', False)
        self.socket_server_host = self._get_config_setting('socketServerHost', 'localhost')
        self.socket_server_port = self._get_config_setting('socketServerPort', 8000)
        self.socket_receive_buffer_size = self._get_config_setting('socketReceiveBufferSize', 1024)
        self.web_server_log_level = self._get_config_setting('webServerLogLevel', 'info')

    #
    # Safely gets a config setting, taking into consideration docker
    # and defaults if it isn't present.
    #
    def _get_config_setting(
        self,
        config_key,
        default_if_not_present = None
    ):
        # Any config value can be overriden by simply appending the word Docker 
        # to the end of the key in the config json file. Construct a docker key
        # so that we can check for the presence of this.
        docker_override_config_key = f"{config_key}Docker"

        # Check for a Docker config override key.
        if self._get_config_exists(docker_override_config_key) and self.is_running_in_docker:
            return self._get_config_value(docker_override_config_key, default_if_not_present)

        return self._get_config_value(config_key, default_if_not_present)

    #
    # Checks if we are running in docker, using the env var.
    #
    def _is_running_in_docker(self):
        return os.environ.get(Config.RUNNING_IN_DOCKER_ENV, False)

    #
    # Safely extracts the value using the key, or defaults if it's not present.
    #
    def _get_config_value(
        self,
        config_key, 
        default_if_not_present = None
    ):
        value = default_if_not_present
        if self._get_config_exists(config_key):
            value = self.data[config_key]        
        return value

    #
    # Checks if the config key exists
    #
    def _get_config_exists(self, config_key):
        return config_key in self.data
