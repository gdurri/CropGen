from flask import Blueprint

blueprint = Blueprint('api', __name__, url_prefix='/cropgen')

@blueprint.route('/run', methods = ['PUT'])
def cropgen():
        return {'message': 'Running CropGen...'}
