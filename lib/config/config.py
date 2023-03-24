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
        self._populate_from_data(self._parse())

    #
    # Serialises itself to JSON.
    #
    def to_json(self):
        return json.dumps(
            self, 
            default = lambda
            obj: obj.__dict__,
            indent = 2
        )

    #
    # Parses the config JSON file and stores it in memory.
    #
    def _parse(self):
        config_file_full_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        with open(config_file_full_path) as json_config_file:
            data = json.load(json_config_file)

        return data

    #
    # Populates itself using the config JSON data.
    #
    def _populate_from_data(self, data):
        self.socket_server_host = self._get_config_setting(data, 'socketServerHost', 'localhost')
        self.socket_server_port = self._get_config_setting(data, 'socketServerPort', 8000)
        self.socket_data_num_bytes_buffer_size = self._get_config_setting(data, 'socketDataNumBytesBufferSize', 4)
        self.socket_data_endianness = self._get_config_setting(data, 'socketDataEndianness', 'big')        
        self.socket_data_encoding = self._get_config_setting(data, 'socketDataEncoding', 'utf-8')
        self.socket_timeout_seconds = self._get_config_setting(data, 'socketTimeoutSeconds', 120.0)
        self.socket_timeout_test_connection_seconds = self._get_config_setting(data, 'socketTimeoutTestConnectionSeconds', 2.0)
        self.web_server_log_level = self._get_config_setting(data, 'webServerLogLevel', 'info')
        self.results_publisher_timeout_seconds = self._get_config_setting(data, 'resultsPublisherTimeoutSeconds', 'info')

    #
    # Safely gets a config setting, taking into consideration docker
    # and defaults if it isn't present.
    #
    def _get_config_setting(
        self,
        data,
        config_key,
        default_if_not_present = None
    ):
        # Any config value can be overriden by simply appending the word Docker 
        # to the end of the key in the config json file. Construct a docker key
        # so that we can check for the presence of this.
        docker_override_config_key = f"{config_key}Docker"

        # Check for a Docker config override key.
        if self._get_config_exists(data, docker_override_config_key) and self.is_running_in_docker:
            return self._get_config_value(data, docker_override_config_key, default_if_not_present)

        return self._get_config_value(data, config_key, default_if_not_present)

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
        data,
        config_key, 
        default_if_not_present = None
    ):
        value = default_if_not_present
        if self._get_config_exists(data, config_key):
            value = data[config_key]        
        return value

    #
    # Checks if the config key exists
    #
    def _get_config_exists(self, data, config_key):
        return config_key in data
