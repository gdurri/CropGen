from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from lib.jobs import Jobs
from lib.config import Config

app = Flask(__name__)

# Create a jobs instance and pass it the config.
jobs = Jobs(Config())

# Swagger Code
swaggerUrl = '/swagger'
apiUrl = '/static/swagger.json'
swaggerBlueprint = get_swaggerui_blueprint(
    swaggerUrl,
    apiUrl,
    config={
        'app_name': "CropGen"
    }
)
app.register_blueprint(swaggerBlueprint, url_prefix=swaggerUrl)

# Endpoints
@app.route('/cropgen/run/', methods = ['POST'])
def cropgen():
    result = jobs._run()
    return jsonify(
        result=result
    )

# Main
if __name__ == "__main__":
    app.run()