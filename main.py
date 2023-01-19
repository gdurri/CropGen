from flask import Flask
from blueprints.basic_endpoints import blueprint as basic_endpoints
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

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
app.register_blueprint(basic_endpoints)

# Main
if __name__ == "__main__":
    app.run()