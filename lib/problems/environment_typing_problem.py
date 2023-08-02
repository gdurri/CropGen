import logging

from lib.models.cgm.relay_apsim import RelayApsim
from lib.problems.problem_base import ProblemBase
from lib.utils.apsim_season_date_generator import APSIMSeasonDateGenerator
from lib.utils.date_time_helper import DateTimeHelper

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
    # Iterate over each population and perform calculations
    #
    def _evaluate(self, variable_values_for_population, out_objective_values, *args, **kwargs):
        if self.run_errors:
            super()._initialize_algorithm_array(out_objective_values)
            return

        logging.info("Processing APSIM iteration (%d of %d) with %d individuals", 
            self.current_iteration_id, 
            self.run_job_request.Iterations,
            len(variable_values_for_population)
        )

        start_time = DateTimeHelper.get_date_time()

        response = self._perform_relay_apsim_request(variable_values_for_population)

        if not super()._handle_evaluate_value_for_population(response, out_objective_values, variable_values_for_population):
            super()._initialize_algorithm_array(out_objective_values)
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

    #
    # Creates request(s) and runs apsim.
    #
    def _perform_relay_apsim_request(self, variable_values_for_population):

        season_date_generator = APSIMSeasonDateGenerator(self.config, self.run_job_request.APSIMSimulationClockStartDate)

        max_individuals = self.run_job_request.MaxIndividualsInOneRelayApsimRequest

        if (max_individuals and
            max_individuals > 0 and 
            max_individuals < len(variable_values_for_population)
        ):
            return self._perform_relay_apsim_staggered_requests(variable_values_for_population, season_date_generator, max_individuals)
        else:
            return self._perform_relay_apsim_one_request(variable_values_for_population, season_date_generator)
    
    #
    # Creates request(s) and runs apsim.
    #
    def _perform_relay_apsim_staggered_requests(self, variable_values_for_population, season_date_generator, max_individuals):
        # Initialize an empty list to store the responses
        responses = []        

        relay_apsim_request = RelayApsim(self.run_job_request.JobID, self.run_job_request.Individuals)
        individual_index = RelayApsim.INPUT_START_INDEX
        individual_counter = 0
        
        for environment_type in self.run_job_request.EnvironmentTypes:
            for environment in environment_type.Environments:
                for season in environment.Seasons:

                    start_date = season_date_generator.generate_start_date_from_season(season)
                    end_date = season_date_generator.generate_end_date_from_season(season)

                    for individual in range(0, len(variable_values_for_population)):
                        relay_apsim_request.SystemPropertyValues.append([str(individual_index), start_date, end_date])
                        relay_apsim_request.SimulationNames.append([str(individual_index), environment_type.Name])

                        relay_apsim_request.add_inputs_for_individual(individual_index, variable_values_for_population[individual])

                        if self._has_reached_max_individuals(individual_counter, max_individuals):
                            responses.append(self._call_relay_apsim(relay_apsim_request))
                            individual_counter = 0
                        else:
                            individual_counter +=1

                        individual_index += 1
                        
                    if len(relay_apsim_request.Inputs) > 0:
                        responses.append(super()._call_relay_apsim(relay_apsim_request))

        response = super()._stitch_responses_into_response(responses)
        return response

    #
    # Works out if we've reached the last 
    #
    def _has_reached_max_individuals(self, individual_counter, max_individuals):
        return individual_counter >= max_individuals

    #
    # Creates request(s) and runs apsim.
    #
    def _perform_relay_apsim_one_request(self, variable_values_for_population, season_date_generator):
        
        relay_apsim_request = RelayApsim(self.run_job_request.JobID, self.run_job_request.Individuals)
        relay_apsim_request.add_inputs_for_env_typing(self.run_job_request.EnvironmentTypes, season_date_generator, variable_values_for_population)
        response = super()._call_relay_apsim(relay_apsim_request)
        return response
