from pytest import fixture
from staze import Test, Mock


class UserMock(Mock):
    username: str
    password: str


@fixture
def user_mock() -> UserMock:
    return UserMock(username='ryzhovalex', password='1234')
