from lib.logging.logger import Logger


class RunJobRequest:
    # Constants
    JOB_ID_JSON_ATTRIBUTE = 'jobId'

    def __init__(self, request_data):
        self.logger = Logger()
        self.errors = []
        self._parse(request_data)

    def _parse(self, payload):
        self.valid = False
        if RunJobRequest.JOB_ID_JSON_ATTRIBUTE in payload:
            self.job_id = payload[RunJobRequest.JOB_ID_JSON_ATTRIBUTE]
            self.valid = True
        else:
            self.errors.append(f"No {RunJobRequest.JOB_ID_JSON_ATTRIBUTE} specified")
