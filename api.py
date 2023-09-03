from flask import Blueprint, jsonify

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def get_users():
    # Implementation here
    pass


@api.route('/api/message', methods=['GET'])
def get_message():
    return jsonify({'message': 'Hello, world!'})

