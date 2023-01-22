from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from lib.jobs import Jobs
from lib.config import Config
from lib.run_job_request import RunJobRequest
from lib.single_year_problem_visualisation import SingleYearProblemVisualisation
from lib.logger import Logger
from lib.jobs_server_client_factory import JobsServerClientFactory

app = Flask(__name__)

# Create a jobs instance and pass it the config.
config = Config()
logger = Logger()
jobs_server_client = JobsServerClientFactory()._create(config, logger)
single_year_problem_visualisation = SingleYearProblemVisualisation(logger, jobs_server_client)
jobs = Jobs(logger, config, single_year_problem_visualisation)

# Swagger Code
swagger_url = '/swagger'
api_url = '/static/swagger.json'
swaggerBlueprint = get_swaggerui_blueprint(
    swagger_url,
    api_url,
    config={
        'app_name': "CropGen"
    }
)
app.register_blueprint(swaggerBlueprint, url_prefix=swagger_url)

# Endpoints
@app.route('/cropgen/run/singleyearproblem', methods = ['POST'])
def cropgen():
    run_job_request = RunJobRequest(logger, request)
    if not run_job_request.valid:
        return jsonify({
            "msg": "Invalid RunJobRequest",
            "errors": run_job_request.errors
        }), 400

    return jobs._run_single_year_problem(run_job_request)

# Main
if __name__ == "__main__":
    app.run()