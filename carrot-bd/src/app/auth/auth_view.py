from staze import View
from flask import request
from app.auth.auth_service import AuthService


class RegisterView(View):
    ROUTE: str = '/register'

    def post(self):
        AuthService.instance().register(request.json)
        return {}


class LoginView(View):
    ROUTE: str = '/login'

    def post(self):
        token: str = AuthService.instance().login(request.json)
        return {
            'user_token': token
        }


class LogoutView(View):
    ROUTE: str = '/logout'

    def post(self):
        AuthService.instance().logout(request.headers)
        return {}
        