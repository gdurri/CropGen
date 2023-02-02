from lib.models.model import Model

class WGPServerRequestBody:
    def __init__(self, job_id, population, inputs):
        self.job_id = job_id
        self.population = population

class WGPServerRequest(Model):
    def __init__(self, job_type, job_id, population, inputs, outputs):
        self.job_type = job_type
        self.body = WGPServerRequestBody(job_id, population, inputs, outputs)
