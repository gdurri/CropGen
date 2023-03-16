from lib.problems.single_year_problem_visualisation import SingleYearProblemVisualisation
from lib.utils.constants  import Constants

#
# Factory class for creating CGM Clients, depending on the config.
#
class ProblemFactory():

    #
    # Creates an instance of a Problem.
    #
    @staticmethod
    def create(config, run_job_request):
        cleansed_job_type = run_job_request.JobType.lower().strip()

        if cleansed_job_type == Constants.SOCKET_MESSAGE_JOB_TYPE_SINGLE_YEAR:
            return SingleYearProblemVisualisation(config, run_job_request)
        elif cleansed_job_type == Constants.SOCKET_MESSAGE_JOB_TYPE_MULTI_YEAR:
            return None
        return None
