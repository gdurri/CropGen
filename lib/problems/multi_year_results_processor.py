import logging

from lib.problems.output_value import OutputValue
from lib.problems.apsim_output import ApsimOutput

from lib.aggregate_functions.aggregate_function_calculator import AggregateFunctionCalculator

#
# Helper for processing the single year results.
#
class MultiYearResultsProcessor():
    
    #
    # Handles the results for a single year sim.
    #
    @staticmethod
    def process_results(
        run_job_request,
        config, 
        apsim_simulation_id_str, 
        apsim_simulation_name_str,
        results_for_individual,
        all_algorithm_outputs,
        all_results_outputs
    ):
        total_outputs = run_job_request.get_total_outputs()
        algorithm_outputs = []
        
        apsim_output = ApsimOutput(apsim_simulation_id_str, apsim_simulation_name_str)

        for output_index in range(0, total_outputs):
            request_output = run_job_request.get_output_by_index(output_index)

            # If there is no output move onto the next one.
            if not request_output: continue

            if request_output.AggregateFunctions:
                MultiYearResultsProcessor.process_output_aggregate_functions(
                    config,
                    request_output,
                    output_index,
                    apsim_simulation_name_str,
                    results_for_individual,
                    algorithm_outputs,
                    apsim_output
                )
            else:
                MultiYearResultsProcessor.process_output(
                    request_output,
                    algorithm_outputs,
                    apsim_output
                )

        all_algorithm_outputs.append(algorithm_outputs)
        all_results_outputs.append(apsim_output)

    #
    # Processes the output, using all of it's aggregate functions.
    #
    @staticmethod
    def process_output_aggregate_functions(
        config,
        request_output,
        output_index,
        apsim_simulation_name_str,
        results_for_individual,
        algorithm_outputs,
        apsim_output
    ):
        for aggregate_function in request_output.AggregateFunctions:
            aggregate_function_calculator = AggregateFunctionCalculator(config, apsim_simulation_name_str, aggregate_function)
            raw_output_value = aggregate_function_calculator.calculate_output_value(results_for_individual, output_index)
            output_value = OutputValue(
                raw_output_value, 
                aggregate_function.DisplayName, 
                aggregate_function.Maximise, 
                aggregate_function.Multiplier
            )

            # If we're optimising this value then we need to store it in the algorithm outputs.
            if request_output.Optimise:
                algorithm_outputs.append(output_value.get_output_value_for_algorithm())

            apsim_output.outputs.append(output_value)

    #
    # Processes the output.
    #
    @staticmethod
    def process_output(
        request_output,
        algorithm_outputs,
        apsim_output
    ):
        logging.warn("Processing Apsim Output: '%s', in a MultiYear simulation, without any aggregate functions. Returning 0.0", request_output.ApsimOutputName)

        output_value = OutputValue(
            0.0, 
            request_output.ApsimOutputName, 
            request_output.Maximise, 
            request_output.Multiplier
        )

        # If we're optimising this value then we need to store it in the algorithm outputs.
        if request_output.Optimise:
            algorithm_outputs.append(output_value.get_output_value_for_algorithm())

        apsim_output.outputs.append(output_value)
