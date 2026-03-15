import logging

import bcrypt

from configuration import EnvironmentConfiguration


class CredentialService:
    def __init__(self, env: EnvironmentConfiguration):
        self.env = env
        self.log = logging.getLogger(__name__)

    def get_all_users(self) -> list:
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
                return users
        except FileNotFoundError:
            self.log.error(f"htpasswd file not found at: {htpasswd_file_path}")
            return []
        except Exception as e:
            self.log.error(f"Error reading htpasswd file: {e}")
            return []

    def delete_user(self, username: str) -> list:
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
                return [username] if user_deleted else []
        except FileNotFoundError:
            self.log.error(f"htpasswd file not found at: {htpasswd_file_path}")
            return []
        except Exception as e:
            self.log.error(f"Error deleting user from htpasswd file: {e}")
            return [False]

    def save_new_user(self, username: str, password: str) -> list:
        # check if user already exists
        if username in self.get_all_users():
            self.log.warning(f"User '{username}' already exists. Cannot create duplicate user.")
            return []

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.log.info(f"Password for user '{username}' hashed successfully.")
        htpasswd_file_path = self.env.get('HTPASSWD_FILE_PATH')
        self.log.info(f"Attempting to save new user '{username}' to htpasswd file at: {htpasswd_file_path}")
        try:
            with open(htpasswd_file_path, 'a') as file:
                file.write(f"{username}:{hashed_password.decode()}\n")
            self.log.info(f"User '{username}' successfully added to htpasswd file.")
            return [username]
        except FileNotFoundError:
            self.log.error(f"htpasswd file not found at: {htpasswd_file_path}")
            return []
        except Exception as e:
            self.log.error(f"Error saving new user to htpasswd file: {e}")
            return []
