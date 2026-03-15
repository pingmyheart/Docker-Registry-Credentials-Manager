from pydantic import BaseModel


class CreateNewUserRequest(BaseModel):
    username: str
    password: str


class ResetUserPasswordRequest(BaseModel):
    username: str
    password: str
