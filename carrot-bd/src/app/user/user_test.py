from pytest import fixture
from staze import Test, Mock, App, Database, HttpClient, parsing, validation
from app.user.user_orm import UserOrm
from app.user.user import User


class UserMock(Mock):
    username: str
    password: str


@fixture
def user_mock() -> UserMock:
    return UserMock(username='ryzhovalex', password='1234')


@fixture
def user_orm(app: App, database: Database, user_mock: UserMock) -> UserOrm:
    with app.app_context():
        return UserOrm.create(
            username=user_mock.username, password=user_mock.password)


class TestApiUsersSelf(Test):
    def test_get(
            self, app: App, database: Database, authorization_header: str,
            http: HttpClient):
        with app.app_context():
            response = http.get(
                '/users/self', 200,
                headers={'Authorization': authorization_header})

            json: dict = parsing.parse(response.json, dict)
            user_json: dict = parsing.parse_key('user', json, dict)
            User(**user_json)


class TestApiUsersId(Test):
    def test_patch_username(
        self, app: App, database: Database, user_orm: UserOrm, http: HttpClient
    ):
        with app.app_context():
            response = http.patch(
                f'/users/{user_orm.id}', 200,
                json={
                    'username': 'newuser'
                })
            
            user_orm = UserOrm.get_first()
            assert user_orm.username == 'newuser'

    def test_patch_password(
        self, app: App, database: Database, user_orm: UserOrm, http: HttpClient
    ):
        with app.app_context():
            response = http.patch(
                f'/users/{user_orm.id}', 200,
                json={
                    'password': 'donuts'
                })
            
            user_orm = UserOrm.get_first()
            assert user_orm.check_password('donuts')

    def test_patch(
        self, app: App, database: Database, user_orm: UserOrm, http: HttpClient
    ):
        with app.app_context():
            response = http.patch(
                f'/users/{user_orm.id}', 200,
                json={
                    'username': 'newuser',
                    'password': 'donuts'
                })
            
            user_orm = UserOrm.get_first()
            assert user_orm.username == 'newuser'
            assert user_orm.check_password('donuts')
