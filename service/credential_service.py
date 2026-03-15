import logging

import bcrypt

from configuration import EnvironmentConfiguration
from dto.credential_controller_request import CreateNewUserRequest, ResetUserPasswordRequest
from dto.credential_service_response import GetAllUsersResponse, DeleteUserResponse, SaveNewUserResponse, \
    ResetUserPasswordResponse


class CredentialService:
    def __init__(self, env: EnvironmentConfiguration):
        self.env = env
        self.log = logging.getLogger(__name__)

    def get_all_users(self) -> GetAllUsersResponse:
        htpasswd_file_path = self.env.get('HTPASSWD_FILE_PATH')
        self.log.info(f"Reading htpasswd file from: {htpasswd_file_path}")
        try:
            with open(htpasswd_file_path, 'r') as file:
                users = []
                for line in file:
                    if ':' in line:
                        username = line.split(':')[0].strip()
                        users.append(username)
                self.log.info(f"Found users: {users}")
                return GetAllUsersResponse(success=True,
                                           message="OK",
                                           users=users)
        except FileNotFoundError:
            self.log.error(f"htpasswd file not found at: {htpasswd_file_path}")
            return GetAllUsersResponse(success=False,
                                       message=f"htpasswd file not found at: {htpasswd_file_path}")
        except Exception as e:
            self.log.error(f"Error reading htpasswd file: {e}")
            return GetAllUsersResponse(success=False,
                                       message=f"Error reading htpasswd file: {e}")

    def delete_user(self, username: str) -> DeleteUserResponse:
        htpasswd_file_path = self.env.get('HTPASSWD_FILE_PATH')
        self.log.info(f"Attempting to delete user '{username}' from htpasswd file at: {htpasswd_file_path}")
        try:
            with open(htpasswd_file_path, 'r') as file:
                lines = file.readlines()
            with open(htpasswd_file_path, 'w') as file:
                user_deleted = False
                for line in lines:
                    if line.startswith(username + ':'):
                        user_deleted = True
                        self.log.info(f"User '{username}' found and will be deleted.")
                        continue  # Skip writing this line to delete the user
                    file.write(line)
                if not user_deleted:
                    self.log.warning(f"User '{username}' not found in htpasswd file.")
                return DeleteUserResponse(success=user_deleted,
                                          message="OK" if user_deleted else f"User '{username}' not found.",
                                          deleted_user=username if user_deleted else None)
        except FileNotFoundError:
            self.log.error(f"htpasswd file not found at: {htpasswd_file_path}")
            return DeleteUserResponse(success=False,
                                      message=f"htpasswd file not found at: {htpasswd_file_path}")
        except Exception as e:
            self.log.error(f"Error deleting user from htpasswd file: {e}")
            return DeleteUserResponse(success=False,
                                      message=f"Error deleting user from htpasswd file: {e}")

    def save_new_user(self, service_request: CreateNewUserRequest) -> SaveNewUserResponse:
        # check if user already exists
        if service_request.username in self.get_all_users().users:
            self.log.warning(f"User '{service_request.username}' already exists. Cannot create duplicate user.")
            return SaveNewUserResponse(success=False,
                                       message=f"User '{service_request.username}' already exists.")

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(service_request.password.encode('utf-8'), bcrypt.gensalt())
        self.log.info(f"Password for user '{service_request.username}' hashed successfully.")
        htpasswd_file_path = self.env.get('HTPASSWD_FILE_PATH')
        self.log.info(
            f"Attempting to save new user '{service_request.username}' to htpasswd file at: {htpasswd_file_path}")
        try:
            with open(htpasswd_file_path, 'a') as file:
                file.write(f"{service_request.username}:{hashed_password.decode()}\n")
            self.log.info(f"User '{service_request.username}' successfully added to htpasswd file.")
            return SaveNewUserResponse(success=True,
                                       message="OK",
                                       created_user=service_request.username)
        except FileNotFoundError:
            self.log.error(f"htpasswd file not found at: {htpasswd_file_path}")
            return SaveNewUserResponse(success=False,
                                       message=f"htpasswd file not found at: {htpasswd_file_path}")
        except Exception as e:
            self.log.error(f"Error saving new user to htpasswd file: {e}")
            return SaveNewUserResponse(success=False,
                                       message=f"Error saving new user to htpasswd file: {e}")

    def reset_user_password(self, service_request: ResetUserPasswordRequest) -> ResetUserPasswordResponse:
        # check if user exists
        if service_request.username not in self.get_all_users().users:
            self.log.warning(f"User '{service_request.username}' does not exist. Cannot reset password.")
            return ResetUserPasswordResponse(success=False,
                                             message=f"User '{service_request.username}' does not exist.")

        # delete the user
        response = self.delete_user(username=service_request.username)
        if not response.success:
            self.log.error(f"Failed to delete user '{service_request.username}' for password reset: {response.message}")
            return ResetUserPasswordResponse(success=False,
                                             message=f"Failed to delete user '{service_request.username}' for password reset: {response.message}")

        # create new user
        response = self.save_new_user(service_request=CreateNewUserRequest(username=service_request.username,
                                                                           password=service_request.password))
        if not response.success:
            self.log.error(f"Failed to create user '{service_request.username}' for password reset: {response.message}")
            return ResetUserPasswordResponse(success=False,
                                             message=f"Failed to create user '{service_request.username}' for password reset: {response.message}")

        return ResetUserPasswordResponse(success=True,
                                         message="OK",
                                         updated_user=service_request.username)
