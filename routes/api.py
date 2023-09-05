from flask import Blueprint, current_app, jsonify

api = Blueprint('api', __name__)


# api is a given as it is the blueprint. so routes names doesn't need the "api" in their names

@api.route('/users', methods=['GET'])
def get_users():
    print(current_app)
    return jsonify({"HI": "YUES"})


@api.route('/message', methods=['GET'])
def get_message():
    return jsonify({'message': 'Hello, world!'})
