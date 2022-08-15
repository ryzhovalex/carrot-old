from staze import View
from app.auth.auth_service import AuthService


class RegisterView(View):
    ROUTE: str = '/register'

    def post(self):
        AuthService.instance().register(request.json)
        return {}


class LoginView(View):
    ROUTE: str = '/login'


class LogoutView(View):
    ROUTE: str = '/logout'
