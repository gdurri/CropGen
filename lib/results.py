import json

class ResultsData:
    def __init__(self, job_id, data_frame):
        self.job_id = job_id
        self.data = data_frame.to_json(indent=2)

class Results:        
    def __init__(self, job_id, data_frame):
        self.type = __class__.__name__
        self.data = ResultsData(job_id, data_frame)

    def to_json(self):
        return json.dumps(
            self, 
            default=lambda
            obj: obj.__dict__,
            indent=2
        )
