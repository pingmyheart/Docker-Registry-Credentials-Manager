from flask import Blueprint, request, jsonify

from dto.credential_controller_request import CreateNewUserRequest, ResetUserPasswordRequest
from service import credential_service_bean

credential_bp = Blueprint('credential', __name__, url_prefix='/credential')


@credential_bp.route('/users', methods=['GET'])
def get_all_users():
    response = credential_service_bean.get_all_users()
    return (jsonify(response.model_dump()),
            200 if response.success else 422)


@credential_bp.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    response = credential_service_bean.delete_user(username=username)
    return (jsonify(response.model_dump()),
            200 if response.success else 422)


@credential_bp.route('/users', methods=['POST'])
def save_new_user():
    request_data = CreateNewUserRequest(**request.get_json())
    response = credential_service_bean.save_new_user(service_request=request_data)
    return (jsonify(response.model_dump()),
            200 if response.success else 422)


@credential_bp.route('/users', methods=['PUT'])
def reset_user_password():
    request_data = ResetUserPasswordRequest(**request.get_json())
    response = credential_service_bean.reset_user_password(service_request=request_data)
    return (jsonify(response.model_dump()),
            200 if response.success else 422)
