from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from lib.jobs import Jobs
from lib.config import Config
from lib.run_job_request import RunJobRequest

app = Flask(__name__)

# Create a jobs instance and pass it the config.
jobs = Jobs(Config())

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
@app.route('/cropgen/run/', methods = ['POST'])
def cropgen():
    run_job_request = RunJobRequest(request)
    if not run_job_request.valid:
        return jsonify({
            "msg": "Invalid RunJobRequest",
            "errors": run_job_request.errors
        }), 400

    result = jobs._run(run_job_request)
    return jsonify(
        result=result
    )

# Main
if __name__ == "__main__":
    app.run()