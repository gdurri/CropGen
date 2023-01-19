import random
from flask import Blueprint, request, jsonify

blueprint = Blueprint('api', __name__, url_prefix='/cropgen')

@blueprint.route('/run', methods = ['PUT', 'POST'])
def cropgen():
    randomNumber = random.randint(0, 10000)
    return jsonify(
        result=randomNumber
    )
