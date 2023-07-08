import logging
import numpy as np

from lib.models.cgm.relay_apsim import RelayApsim
from lib.problems.problem_base import ProblemBase
from lib.utils.date_time_helper import DateTimeHelper
from lib.utils.apsim_season_date_generator import APSIMSeasonDateGenerator

#
# Represents an Environment Typing Problem
#
class EnvironmentTypingProblem(ProblemBase):

    #
    # Construct problem with the given dimensions and variable ranges
    #
    def __init__(self, config, run_job_request, cgm_server_client):
        super().__init__(config, run_job_request, cgm_server_client)

    #
    # Iterate over each population and perform calcs.
    #
    def _evaluate(self, variable_values_for_population, out_objective_values, *args, **kwargs):
        if self.run_errors:
            super()._initialise_algorithm_array(out_objective_values)
            return

        logging.info("Processing APSIM iteration (%d of %d) with %d individuals", 
            self.current_iteration_id, 
            self.run_job_request.Iterations,
            len(variable_values_for_population)
        )

        start_time = DateTimeHelper.get_date_time()

        # Iterate over each environment type that was supplied, calling RelayApsim for each combination.
        for environment_type in self.run_job_request.EnvironmentTypes:

            relay_apsim_request = RelayApsim(
                self.run_job_request, 
                variable_values_for_population, 
                environment_type, 
                APSIMSeasonDateGenerator(
                    self.config,
                    self.run_job_request.APSIMSimulationClockStartDate
                )
            )

            if not super()._handle_evaluate_value_for_population(relay_apsim_request, out_objective_values, variable_values_for_population):
                super()._initialise_algorithm_array(out_objective_values)
                return

        seconds_taken_one_iteration = DateTimeHelper.get_elapsed_seconds_since(start_time)
        estimated_seconds_remaining = (self.run_job_request.Iterations - self.current_iteration_id) * seconds_taken_one_iteration

        logging.info("Finished processing APSIM iteration: %d. Time taken: %s. Estimated finish date time: %s (%s)",  
            self.current_iteration_id, 
            DateTimeHelper.seconds_to_hhmmss_ms(seconds_taken_one_iteration),
            DateTimeHelper.add_seconds_to_datetime_now(estimated_seconds_remaining),
            DateTimeHelper.seconds_to_hhmmss_ms(estimated_seconds_remaining)
        )

        # Increment our iteration ID.
        self.current_iteration_id += 1
