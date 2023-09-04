from flask import Blueprint, jsonify

api = Blueprint('api', __name__)


# api is a given as it is the blueprint. so routes names doesn't need the "api" in their names

@api.route('/users', methods=['GET'])
def get_users():
    # Implementation here
    return jsonify({'message': 'Hello, world!'})


@api.route('/message', methods=['GET'])
def get_message():
    return jsonify({'message': 'Hello, world!'})
