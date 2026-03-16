from flask import Blueprint, render_template, request

from dto.credential_controller_request import CreateNewUserRequest, ResetUserPasswordRequest
from service import credential_service_bean

view_controller_bp = Blueprint('view_controller', __name__, )


@view_controller_bp.route('/', methods=['GET'])
def index():
    service_response = credential_service_bean.get_all_users()
    users: list[str] = service_response.users if service_response.success else []
    users = sorted(users)
    return render_template('index.html', users=users)


@view_controller_bp.route('/users/new', methods=['POST'])
def create_new_user():
    request_form = request.form
    service_request = CreateNewUserRequest(username=request_form.get('username'), password=request_form.get('password'))
    credential_service_bean.save_new_user(service_request=service_request)
    service_response = credential_service_bean.get_all_users()
    users: list[str] = service_response.users if service_response.success else []
    users = sorted(users)
    return render_template('index.html', users=users)


@view_controller_bp.route('/users/delete/<username>', methods=['POST'])
def delete_user(username):
    credential_service_bean.delete_user(username=username)
    service_response = credential_service_bean.get_all_users()
    users: list[str] = service_response.users if service_response.success else []
    users = sorted(users)
    return render_template('index.html', users=users)


@view_controller_bp.route('/users/reset_password/<username>', methods=['POST'])
def reset_user_password(username):
    request_form = request.form
    service_request = ResetUserPasswordRequest(username=username, password=request_form.get('password'))
    credential_service_bean.reset_user_password(service_request=service_request)
    service_response = credential_service_bean.get_all_users()
    users: list[str] = service_response.users if service_response.success else []
    users = sorted(users)
    return render_template('index.html', users=users)
