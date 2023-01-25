import json
from lib.logger import Logger

class RunJobRequest:
  # Constants
  JOB_ID_JSON_ATTRIBUTE = 'jobId'

  def __init__(self, request_data):
    self.logger = Logger()
    self.errors = []
    self._parse(request_data)

  def _parse(self, payload):

    self.valid = True
    if RunJobRequest.JOB_ID_JSON_ATTRIBUTE in payload:
      self.job_id = payload[RunJobRequest.JOB_ID_JSON_ATTRIBUTE]
    else:
        self.valid = False
        job_id_missing_error = f"No {RunJobRequest.JOB_ID_JSON_ATTRIBUTE} specified"
        self.errors.append(job_id_missing_error)
        self.logger._log_warn(job_id_missing_error)
