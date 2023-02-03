import json
import os


class Config:
    RUNNING_IN_DOCKER_ENV = 'RUNNING_IN_DOCKER'

    def __init__(self):

        self.data = self._parse()
        self._populate_from_data()

    def _parse(self):
        relative_path = '../../config/config.json'
        current_script_dir = os.path.dirname(os.path.realpath(__file__))
        config_file_full_path = os.path.join(current_script_dir, relative_path)

        with open(config_file_full_path) as json_config_file:
            data = json.load(json_config_file)

        return data

    def _populate_from_data(self):
        self.jobs_base_url = self._get_config_setting('jobsBaseUrl')
        self.sim_gen_url = self._get_config_setting('simGenUrl')
        self.use_mock_wgp_server_client = self._get_config_setting('useMockWgpServerClient')
        self.show_graphs_when_generated = self._get_config_setting('showGraphsWhenGenerated', True, False)
        self.output_graphs_to_file = self._get_config_setting('outputGraphsToFile')
        self.socket_server_port = self._get_config_setting('socketServerPort')

    def _get_config_setting(self,
                            config_key,
                            check_for_docker=False,
                            value_if_docker=None):
        if not check_for_docker:
            return self.data[config_key]

        if self._is_running_in_docker():
            return value_if_docker

        return self.data[config_key]

    def _is_running_in_docker(self):
        return os.environ.get(Config.RUNNING_IN_DOCKER_ENV, False)

    def _get_sim_gen_url(self):
        return os.path.join(self.jobs_base_url, self.sim_gen_url)
