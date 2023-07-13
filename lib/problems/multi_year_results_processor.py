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
        results_for_individual,
        all_algorithm_outputs,
        all_results_outputs
    ):
        total_outputs = run_job_request.get_total_outputs()
        algorithm_outputs = []
        
        apsim_output = MultiYearResultsProcessor._create_apsim_output(results_for_individual)

        for output_index in range(0, total_outputs):
            request_output = run_job_request.get_output_by_index(output_index)

            # If there is no output or we're not optimising this output, then just skip and move onto the next one.
            if not request_output or not request_output.Optimise: continue

            for aggregate_function in request_output.AggregateFunctions:
                aggregate_function_calculator = AggregateFunctionCalculator(config, aggregate_function)
                raw_output_value = aggregate_function_calculator.calculate_output_value(results_for_individual, output_index)
                output_value = OutputValue(
                    raw_output_value, 
                    aggregate_function.DisplayName, 
                    aggregate_function.Maximise, 
                    aggregate_function.Multiplier
                )

                algorithm_outputs.append(output_value.get_output_value_for_algorithm())
                apsim_output.outputs.append(output_value)

        all_algorithm_outputs.append(algorithm_outputs)
        all_results_outputs.append(apsim_output)

    #
    # Creates an APSIM output, using the simulation id and name from the results.
    #
    @staticmethod
    def _create_apsim_output(results_for_individual):

        first_result = results_for_individual[0]

        simulation_id = first_result.SimulationID
        simulation_name = first_result.SimulationName

        # Determine if there are multiple simulations and if so, assign the simulation ID to 0 and the name to MultiSim.
        for result in results_for_individual:
            if result.SimulationID != simulation_id:
                simulation_id = "0"
                simulation_name = "Multi Simulation"
                break

        return ApsimOutput(simulation_id, simulation_name)
