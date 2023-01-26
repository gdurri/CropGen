import random


class JobsServerClientMock:
    WATER_USE = 'WaterUse'
    YIELD = 'Yield'
    RANDOM_INT_MIN = 0
    RANDOM_INT_MAX = 1000

    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

    def _run(self, job_id, individuals, traits, inputs):
        results = {
            self.WATER_USE:
            [random.randint(self.RANDOM_INT_MIN, self.RANDOM_INT_MAX)],
            self.YIELD:
            [random.randint(self.RANDOM_INT_MIN, self.RANDOM_INT_MAX)]
        }

        self.logger._log_debug(
            f"{self.__class__.__name__} run called with job_id:{job_id}. Returning mock result: {results}"
        )

        return results

    def _run_complete(self, job_id):
        self.logger._log_debug(
            f"{self.__class__.__name__} run complete called with job_id:{job_id}."
        )
