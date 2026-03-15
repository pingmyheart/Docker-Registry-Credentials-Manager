import os

from dotenv import load_dotenv


class EnvironmentConfiguration:
    def __init__(self):
        load_dotenv()

    def get(self, key: str) -> str:
        return os.getenv(key)
