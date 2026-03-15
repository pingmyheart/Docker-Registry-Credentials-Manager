from typing import Optional

from dto.base_response import BaseResponse


class DeleteUserResponse(BaseResponse):
    deleted_user: Optional[str] = None


class GetAllUsersResponse(BaseResponse):
    users: Optional[list] = None


class SaveNewUserResponse(BaseResponse):
    created_user: Optional[str] = None
