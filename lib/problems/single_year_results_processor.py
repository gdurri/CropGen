from lib.problems.output_value import OutputValue
from lib.problems.apsim_output import ApsimOutput

#
# Helper for processing the single year results.
#
class SingleYearResultsProcessor():
    
    #
    # Handles the results for a single year sim.
    #
    @staticmethod
    def process_results(
        run_job_request,
        results_for_individual,
        all_algorithm_outputs,
        all_results_outputs
    ):
        assert(len(results_for_individual) == 1)
        apsim_result = results_for_individual[0]

        total_outputs = min(run_job_request.get_total_outputs(), len(apsim_result.Values))
        algorithm_outputs = []

        apsim_output = ApsimOutput(apsim_result.SimulationID, apsim_result.SimulationName)

        for output_index in range(0, total_outputs):
            raw_apsim_output = apsim_result.Values[output_index]
            request_output = run_job_request.get_output_by_index(output_index)
            
            # If there is no output or we're not optimising this output, then just skip and move onto the next one.
            if not request_output or not request_output.Optimise: continue

            output_value = OutputValue(
                raw_apsim_output, 
                request_output.ApsimOutputName, 
                request_output.Maximise, 
                request_output.Multiplier
            )
            algorithm_outputs.append(output_value.get_output_value_for_algorithm())
            apsim_output.outputs.append(output_value)

        all_algorithm_outputs.append(algorithm_outputs)
        all_results_outputs.append(apsim_output)
