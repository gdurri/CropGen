import datetime
import time
import shutil
import os
import json

from lib.results import Results

class ResultsLogger:

    RESULTS_FOLDER = 'results'
    LOG_FILE = 'logs.txt'
    DESIGN_SPACE_GRAPH_JSON = 'design_space_graph.json'
    DESIGN_SPACE_GRAPH_HTML = 'design_space_graph.html'
    OBJECTIVE_SPACE_GRAPH_JSON = 'objective_space_graph.json'
    OBJECTIVE_SPACE_GRAPH_HTML = 'objective_space_graph.html'
    ALL_INDIVIDUALS_GRAPH_JSON = 'all_individuals_graph.json'
    ALL_INDIVIDUALS_GRAPH_HTML = 'all_individuals_graph.html'
    ALL_OBJECTIVES_SPACE_GRAPH_JSON = 'all_objectives_graph.json'
    ALL_OBJECTIVES_SPACE_GRAPH_HTML = 'all_objectives_graph.html'
    YIELD_OVER_MATURITY_GRAPH_JSON = 'yield_over_maturity_graph.json'
    YIELD_OVER_MATURITY_GRAPH_HTML = 'yield_over_maturity_graph.html'
    OPT_DATA_FRAME_JSON = 'opt_data.json'
    ALL_DATA_FRAME_JSON = 'all_data.json'

    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%H.%M.%S'

    def __init__(self, problem):
        self.problem = problem
        self.results_folder = ''
        self.results_folder_for_now = ''
        self.run_started_time = 0.0
        self.results_folder = ResultsLogger._get_results_folder_path()

    @staticmethod
    def _get_results_folder_path():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            f'../{ResultsLogger.RESULTS_FOLDER}/')

    @staticmethod
    def _remove_and_create_results_folder():
        results_folder = ResultsLogger._get_results_folder_path()

        # Remove and recreate the results directory.
        if os.path.exists(results_folder):
            shutil.rmtree(results_folder)
        os.makedirs(results_folder)

    def _run_started(self):
        self._construct_results_file_path()
        self.run_started_time = time.time()
        self._log_problem_entry(f'Run started')

    def _run_ended(self):
        self._log_problem_entry(
            f'Run finished. Total run time: {time.time() - self.run_started_time} seconds'
        )

    def _construct_results_file_path(self):
        now = datetime.datetime.now()

        results_folder_for_today = os.path.join(self.results_folder,
                                                now.strftime(self.DATE_FORMAT))
        # Remove and recreate the results directory.
        if not os.path.exists(results_folder_for_today):
            os.makedirs(results_folder_for_today)

        time_str = now.strftime(self.TIME_FORMAT)

        results_folder_for_now = os.path.join(results_folder_for_today,
                                              f"{self.problem}_{time_str}")

        # Create a folder within today, for the current time.
        if not os.path.exists(results_folder_for_now):
            os.makedirs(results_folder_for_now)

        self.results_folder_for_now = results_folder_for_now

    def _create_filepath_in_for_now_folder(self, filename):
        return os.path.join(self.results_folder_for_now, filename)

    def _log_problem_entry(self, data):
        date_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
        data_str = f"{date_time_str}: {str(data)}"
        self._log_entry(
            self._create_filepath_in_for_now_folder(ResultsLogger.LOG_FILE),
            data_str)

    def _log_graph(self, graph, graph_file_name_json, graph_file_name_html):
        self._log_entry(
            self._create_filepath_in_for_now_folder(graph_file_name_json),
            graph.to_json(pretty=True))
        self._log_entry(
            self._create_filepath_in_for_now_folder(graph_file_name_html),
            graph.to_html())

    def _log_raw_results_to_file(self, data_frame, filename):
        self._log_entry(self._create_filepath_in_for_now_folder(filename),
                        data_frame.to_json(indent=2))

    async def _log_raw_results(self, data_frame, job_id, websocket):
        results = Results(job_id, data_frame)
        await websocket.send_text(results.to_json())

    def _log_entry(self, filename, data):
        with open(filename, "a") as file:
            file.write(f"{data} \n")
