from pytest import fixture
from staze import Test, App, Database, log, HttpClient, parsing, validation
from warepy import get_enum_values
from app.auth.login_data import LoginData
from app.auth.auth_service import AuthService
from app.user.user import User
from app.auth.auth_error import AuthError
from app.project.builtin_project_ids_enum import BuiltinProjectIdsEnum
from app.user.user_test import UserMock
from app.user.user_orm import UserOrm
from app.task.task_orm import TaskOrm
from app.project.project_orm import ProjectOrm


@fixture
def login_data(user_mock: UserMock) -> LoginData:
    return LoginData(
        username=user_mock.username,
        password=user_mock.password)


@fixture
def login_user(
        app: App, db: Database,
        login_data: LoginData, user_id: int) -> None:
    with app.app_context():
        AuthService.instance().login(login_data)


@fixture
def authorization_header(app: App, db: Database, login_user) -> str:
    with app.app_context():
        user_orm: UserOrm = UserOrm.get_first()
        return 'Bearer ' + user_orm.active_token


class TestApiRegister(Test):
    def test_post(
        self, app: App, db: Database, http: HttpClient,
        user_mock: UserMock
    ):
        with app.app_context():
            response = http.post(
                '/register', 200,
                json={
                    'username': user_mock.username,
                    'password': user_mock.password
                })

            json: dict = parsing.parse(response.json, dict)

            user: User = User(**json['user'])
            user_orm: UserOrm = UserOrm.get_first(id=user.id)

            assert user_orm.username == user_mock.username
            assert user_orm.check_password(user_mock.password)
            # Ensure default projects are created for user
            assert user_orm.project_ids == get_enum_values(
                BuiltinProjectIdsEnum)


class TestApiLogin(Test):
    def test_post(
            self, app: App, db: Database, http: HttpClient,
            login_data: LoginData):
        with app.app_context():
            response = http.post('/login', 200, json=login_data.dict())

            json: dict = parsing.parse(response.json, dict)
            user_token: str = parsing.parse_key('user_token', json, str) 
            assert user_token == UserOrm.get_first().active_token


class TestApiLogout(Test):
    def test_post(
            self, app: App, db: Database, http: HttpClient,
            authorization_header: str):
        with app.app_context():
            response = http.post(
                '/logout',
                200,
                json=login_data.dict(),
                headers={'Authorization': authorization_header})

            user_orm: UserOrm = UserOrm.instance().get_first()

            assert not user_orm.is_logged
            try:
                user_orm.active_token
            except AuthError:
                pass
            else:
                raise AssertionError()
