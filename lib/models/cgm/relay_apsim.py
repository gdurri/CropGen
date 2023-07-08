from lib.models.common.model import Model

#
# A WGP Server request object that invokes APSIM runs, calling update parameters and passing in 
# the input values that will override the input traits that were sent in the InitWorkers request.
#
class RelayApsim(Model):
    INPUT_START_INDEX = 0
    #
    # Constructor
    #
    def __init__(
        self, 
        run_job_request, 
        generated_input_values, 
        environment_type=None, 
        season_date_generator=None
    ):
        self.JobID = run_job_request.JobID
        self.Individuals = run_job_request.Individuals
        self.Inputs = []
        self.SimulationNames = []
        self.SystemPropertyValues = []

        self.initialise(generated_input_values, environment_type, season_date_generator)

    #
    # Handles the more complex class initialisation.
    #
    def initialise(self, generated_input_values, environment_type, season_date_generator):

        if environment_type:
            return self.initialise_for_env_typing(environment_type, season_date_generator, generated_input_values)
        else:
            return self.add_inputs(generated_input_values)
        
    #
    # Sets up the input values, simulation names and system property values, for a request with env typing.
    #
    def initialise_for_env_typing(self, environment_type, season_date_generator, generated_input_values):
        if not environment_type.Environments:
            raise Exception("Cannot construct %s because the Environments are null", self.get_type_name())
        
        self.SimulationNames.append(environment_type.Name)

        input_id = RelayApsim.INPUT_START_INDEX

        for environment in environment_type.Environments:
            environment_type = environment.Type

            for season in environment.Seasons:
                start_date = season_date_generator.generate_start_date_from_season(season)
                end_date = season_date_generator.generate_end_date_from_season(season)

                for individual in range(RelayApsim.INPUT_START_INDEX, len(generated_input_values)):
                    self.add_inputs_for_individual(input_id, generated_input_values[individual])
                    self.SystemPropertyValues.append(start_date)
                    self.SystemPropertyValues.append(end_date)
                    input_id += 1

    #
    # Adds all of the inputs.
    #
    def add_inputs(self, generated_input_values):
        for individual in range(RelayApsim.INPUT_START_INDEX, len(generated_input_values)):
            self.add_inputs_for_individual(individual, generated_input_values[individual])

    #
    # Adds all of the inputs.
    #
    def add_inputs_for_individual(self, individual, inputs):

        # Add the iteration id to the beginning of the array. 
        # We use the individual index for a convenient auto incrementing id.
        values = [individual]

        # Iterate over all of the input values that were passed in,
        # adding each one to the values array
        for input_value in inputs:
            values.append(input_value)

        # Now add the complete list of values which will contain the iteration
        # id, followed by all of the input values.
        self.Inputs.append(values)
    
    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
