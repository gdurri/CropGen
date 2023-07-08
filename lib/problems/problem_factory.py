from lib.problems.problem import Problem
from lib.problems.environment_typing_problem import EnvironmentTypingProblem

#
# Factory class for creating CGM Clients, depending on the config.
#
class ProblemFactory():

    #
    # Creates an instance of a Problem.
    #
    @staticmethod
    def create(config, run_job_request, cgm_server_client):
        if run_job_request.get_is_environment_typing_run():
            return EnvironmentTypingProblem(config, run_job_request, cgm_server_client )
        else:
            return Problem(config, run_job_request, cgm_server_client )
