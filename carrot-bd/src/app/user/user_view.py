from staze import View
from flask import request
from app.user.user_service import UserService
from app.user.user import User


class UsersSelfView(View):
    ROUTE: str = '/users/self'

    def get(self):
        user: User = UserService.instance().get_self_user(
            request.headers
        )
        return user.api_dict


class UsersIdView(View):
    ROUTE: str = '/users/<id>'

    def patch(self, id):
        return UserService.instance().patch_user(id, request.json).api_dict
