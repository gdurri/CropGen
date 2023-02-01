import shutil
import os

from lib.SocketMessages.results_message import ResultsMessage
from lib.SocketMessages.start_of_run_message import StartOfRunMessage
from lib.SocketMessages.end_of_run_message import EndOfRunMessage
from lib.Utils.date_time_helper import DateTimeHelper

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

    def __init__(self, problem):
        self.problem = problem
        self.results_folder = ''
        self.results_folder_for_now = ''
        self.run_start_time = DateTimeHelper._get_date_time()
        self.results_folder = ResultsLogger._get_results_folder_path()

    @staticmethod
    def _get_results_folder_path():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            f'../../{ResultsLogger.RESULTS_FOLDER}/')

    @staticmethod
    def _remove_and_create_results_folder():
        results_folder = ResultsLogger._get_results_folder_path()

        # Remove and recreate the results directory.
        if os.path.exists(results_folder):
            shutil.rmtree(results_folder)
        os.makedirs(results_folder)

    def _construct_results_file_path(self):

        results_folder_for_today = os.path.join(self.results_folder, DateTimeHelper._get_date_now_str())

        # Remove and recreate the results directory.
        if not os.path.exists(results_folder_for_today):
            os.makedirs(results_folder_for_today)

        time_str = DateTimeHelper._get_time_now_str()

        results_folder_for_now = os.path.join(results_folder_for_today, f"{self.problem}_{time_str}")

        # Create a folder within today, for the current time.
        if not os.path.exists(results_folder_for_now):
            os.makedirs(results_folder_for_now)

        self.results_folder_for_now = results_folder_for_now

    def _create_filepath_in_for_now_folder(self, filename):
        return os.path.join(self.results_folder_for_now, filename)

    def _log_problem_entry(self, data):
        date_time_str = DateTimeHelper._get_date_time_now_str()
        data_str = f"{date_time_str}: {str(data)}"
        self._log_entry(self._create_filepath_in_for_now_folder(ResultsLogger.LOG_FILE), data_str)

    def _log_graph(self, graph, graph_file_name_json, graph_file_name_html):
        self._log_entry(self._create_filepath_in_for_now_folder(graph_file_name_json), graph.to_json(pretty=True))
        self._log_entry(self._create_filepath_in_for_now_folder(graph_file_name_html), graph.to_html())

    def _log_raw_results_to_file(self, data_frame, filename):
        self._log_entry(self._create_filepath_in_for_now_folder(filename), data_frame.to_json(indent=2))

    def _log_entry(self, filename, data):
        with open(filename, "a") as file:
            file.write(f"{data} \n")

    # Web socket logging - Async methods.
    async def _run_started(self, job_type, job_id, websocket):
        self._log_problem_entry(f'Run started')
        self._construct_results_file_path()
        self.run_start_time = DateTimeHelper._get_date_time()
        message = StartOfRunMessage(job_type, job_id)
        await websocket.send_text(message.to_json())

    async def _run_ended(self, job_type, job_id, websocket):
        duration_seconds = DateTimeHelper._get_seconds_since_now(self.run_start_time)
        self._log_problem_entry(f'Run finished. Total run time: {duration_seconds} seconds')
        message = EndOfRunMessage(job_type, job_id, duration_seconds)
        await websocket.send_text(message.to_json())

    async def _log_raw_results(self, job_type, job_id, data_frame, websocket):
        message = ResultsMessage(job_type, job_id, data_frame)
        await websocket.send_text(message.to_json())
