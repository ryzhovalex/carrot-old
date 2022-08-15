from typing import TYPE_CHECKING
from staze import Database, validation, parsing, log
from werkzeug import security
from sqlalchemy.ext.hybrid import hybrid_property
from app.user.user import User
from app.auth.auth_error import AuthError

if TYPE_CHECKING:
    hybrid_property = property


class UserOrm(Database.Orm):
    _username: str = Database.column(
        Database.string(150), nullable=False, unique=True)
    _password: str = Database.column(Database.string(150), nullable=False)
    _task_orms: list[TaskOrm] = Database.relationship(
        'TaskOrm',
        backref='user_orm',
        foreign_keys='[TaskOrm.user_id]'
    )
    _project_orms: list[ProjectOrm] = Database.relationship(
        'ProjectOrm',
        backref='user_orm',
        foreign_keys='[ProjectOrm.user_id]'
    )
    _is_logged: bool = Database.column(Database.boolean, default=False)
    _active_token: str = Database.column(Database.string, default='')

    @classmethod
    def create(cls, username: str, password: str) -> 'UserOrm':
        model: 'UserOrm' = cls(
            _username=username,
            _password=security.generate_password_hash(password))
        Database.instance().push(model)
        return cls.get_first(id=model.id)

    @hybrid_property
    def active_token(self) -> str:
        if not self._is_logged:
            raise AuthError('User not logged in')

        return self._active_token

    @hybrid_property
    def username(self) -> str:
        return self._username

    @active_token.setter
    def active_token(self, token: str):
        log.bind(user_id=self.id).info('Set active token')
        validation.validate(token, str)
        self._active_token = token

    def check_password(self, password: str) -> bool:
        """Check given password against hashed one.
        
        Returns:
            bool:
                Whether check is passed.
        """
        return security.check_password_hash(self._password, password)

    @hybrid_property
    def is_logged(self) -> bool:
        return self._is_logged

    @hybrid_property
    def task_ids(self) -> list[int]:
        return [task_orm.id for task_orm in self._task_orms]

    @hybrid_property
    def project_ids(self) -> list[int]:
        return [project_orm.id for project_orm in self._project_orm]

    def model(self) -> User:
        return User(
            username=self.username,
            task_ids=self.task_ids,
            project_ids=self.project_ids,
            is_logged=self.is_logged,
            # Don't request active_token property or you will get an error if
            # user isn't logged
            active_token=self._active_token
        )

    def set_password(self, password: str):
        log.bind(user_id=self.id).info('Set new password for user')
        validation.validate(password, str)
        self._password = password
