from pydantic import BaseModel


class CreateNewUserRequest(BaseModel):
    username: str
    password: str
