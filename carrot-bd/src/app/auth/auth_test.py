from pytest import fixture
from staze import Test, App, Database, log, HttpClient, parsing, validation
from app.auth.login_data import LoginData


@fixture
def login_data(user_mock: UserMock) -> LoginData:
    login_data: LoginData = LoginData(
        username=user_mock.username,
        password=user_mock.password)


@fixture
def login_user(app: App, database: Database, login_data: LoginData) -> None:
    with app.app_context():
        AuthService.instance().login(login_data)


@fixture
def authorization_header(app: App, database: Database, login_user) -> str:
    with app.app_context():
        user_orm: UserOrm = UserOrm.get_first()
        return 'Bearer ' + user_orm.active_token


class TestApiLogin(Test):
    def test_post(
            self, app: App, db: Database, http: HttpClient,
            login_data: LoginData):
        with app.app_context():
            response = http.post('/login', 200, json=login_data.dict())

            json: dict = parsing.parse(response.json, dict)
            parsing.parse_key('user_token', json, str) 


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

            assert not user_orm.is_logged()
            try:
                user_orm.active_token
            except AuthError:
                pass
            else:
                raise AssertionError()
