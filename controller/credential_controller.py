from flask import Blueprint, request

from service import credential_service_bean

credential_bp = Blueprint('credential', __name__, url_prefix='/credential')


@credential_bp.route('/users', methods=['GET'])
def get_all_users():
    return credential_service_bean.get_all_users()


@credential_bp.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    return credential_service_bean.delete_user(username=username)


@credential_bp.route('/users', methods=['POST'])
def save_new_user():
    json_data = request.get_json()
    username = json_data.get('username')
    password = json_data.get('password')
    return credential_service_bean.save_new_user(username=username,
                                                 password=password)
