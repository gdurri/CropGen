from lib.problems.single_year_problem_visualisation import SingleYearProblemVisualisation
from lib.problems.multi_year_problem_visualisation import MultiYearProblemVisualisation
from lib.models.run_job_request import RunJobRequest
from lib.models.error_message import ErrorMessage
from lib.utils.constants import Constants


class RunMessageProcessor():
    #
    # Constructor
    #
    def __init__(self, config, websocket):
        self.config = config
        self.websocket = websocket

    #
    # Processes the run message passed in from the websocket.
    #
    async def process_run_message(self, job_type, body):
        # Construct a Run Job Request, using the JSON body.
        run_job_request = RunJobRequest(body)
        # If it's invalid, send a socket message and return.
        if not run_job_request.is_valid():
            await self.websocket.send_text(ErrorMessage(run_job_request.errors).to_json())
            return

        # Next step is to try and create a "Problem" using the job type.
        problem = self._create_problem(job_type, run_job_request)

        # If a valid "Problem" was created, call the run function.
        if problem:
            await problem.run(self.websocket)
        # Otherwise send an error message.
        else:
            await self.websocket.send_text(ErrorMessage(f"Unknown run job type: {job_type}.").to_json())

    #
    # Constructs a problem using the job type, or None if we don't know 
    # how to handle this job type.
    #
    def _create_problem(self, job_type, run_job_request):
        cleansed_job_type = job_type.lower().strip()

        if cleansed_job_type == Constants.JOB_TYPE_SINGLE_YEAR:
            return SingleYearProblemVisualisation(self.config, run_job_request)
        elif cleansed_job_type == Constants.JOB_TYPE_MULTI_YEAR:
            return MultiYearProblemVisualisation(self.config, run_job_request)
        return None
