from typing import TYPE_CHECKING
from staze import Database, log, parsing, validation
from app.project.project import Project
from sqlalchemy.ext.hybrid import hybrid_property

if TYPE_CHECKING:
    from app.task.task_orm import TaskOrm
    hybrid_property = property


class ProjectOrm(Database.Orm):
    _name: str = Database.column(Database.string(150), nullable=False)
    _task_orms: list['TaskOrm'] = Database.relationship(
        'TaskOrm',
        backref='project_orms',
        foreign_keys='[TaskOrm.user_id]'
    )
    _user_id: int = Database.column(
        Database.integer, Database.foreign_key('user_orm.id')
    )

    @classmethod
    def create(cls, name: str, user_id: int) -> 'ProjectOrm':
        validation.validate(name, str)
        validation.validate(user_id, int)

        model = cls(_name=name, _user_id=user_id)
        log.bind(project_id=model.id).info('Create project')
        return model
        
    @hybrid_property
    def user_id(self) -> int:
        return self._user_id

    @hybrid_property
    def task_ids(self) -> list[int]:
        return [orm.id for orm in self._task_orms]

    @hybrid_property
    def model(self) -> Project:
        return Project(
            id=self.id,
            name=self.name, user_id=self.user_id, task_ids=self.task_ids)

    @hybrid_property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        validation.validate(value, str)
        self._name = value
