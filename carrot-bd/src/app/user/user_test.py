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
def user_id(app: App, db: Database, user_mock: UserMock) -> int:
    with app.app_context():
        orm = UserOrm.create(
            username=user_mock.username, password=user_mock.password)
        id = orm.id
        db.push(orm)
        return id


class TestApiUsersSelf(Test):
    def test_get(
            self, app: App, db: Database, authorization_header: str,
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
        self, app: App, db: Database, user_id: int, http: HttpClient
    ):
        with app.app_context():
            response = http.patch(
                f'/users/{user_id}', 200,
                json={
                    'username': 'newuser'
                })
            
            json: dict = parsing.parse(response.json, dict)
            user: User = User(**json['user'])
            user_orm = UserOrm.get_first(id=user.id)
            assert user_orm.username == 'newuser'

    def test_patch_password(
        self, app: App, db: Database, user_id: int, http: HttpClient
    ):
        with app.app_context():
            response = http.patch(
                f'/users/{user_id}', 200,
                json={
                    'password': 'donuts'
                })
            
            json: dict = parsing.parse(response.json, dict)
            user: User = User(**json['user'])
            user_orm = UserOrm.get_first(id=user.id)
            assert user_orm.check_password('donuts')

    def test_patch(
        self, app: App, db: Database, user_id: int, http: HttpClient
    ):
        with app.app_context():
            response = http.patch(
                f'/users/{user_id}', 200,
                json={
                    'username': 'newuser',
                    'password': 'donuts'
                })
            
            json: dict = parsing.parse(response.json, dict)
            user: User = User(**json['user'])
            user_orm = UserOrm.get_first(id=user.id)
            assert user_orm.username == 'newuser'
            assert user_orm.check_password('donuts')
