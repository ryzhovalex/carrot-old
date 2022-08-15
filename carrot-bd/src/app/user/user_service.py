from typing import Any
from staze import Service, parsing, validation, Database
from werkzeug.datastructures import Headers
from app.user.user import User
from app.user.user_orm import UserOrm


class UserService(Service):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def get_user_for_auth_header(self, auth_header: str) -> User:
        # Auth header in format 'Bearer <jwt_token>'
        token: str = auth_header.split(' ')[1]
        user_orm: UserOrm = UserOrm.get_first(active_token=token)
        return user_orm.model

    def get_self_user(self, headers: Headers) -> User:
        auth_header: str = parsing.parse_key('Authorization', headers, str)
        return self.get_user_for_auth_header(auth_header)

    def patch_user(self, id: int | str, patch_data: Any) -> User:
        id = parsing.parse_int(id)
        data: dict = parsing.parse(data, dict)

        user_orm: UserOrm = UserOrm.get_first(id=id)

        for k, v in data.items():
            match k:
                case 'username':
                    user_orm.username = v
                case 'password':
                    user_orm.set_password(v)
                case _:
                    Database.instance().rollback()
                    raise parsing.ParsingError(
                        f'Unrecognized patch data key {k}')

        model = user_orm.model
        Database.instance().commit() 
        return model
