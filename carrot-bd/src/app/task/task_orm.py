from datetime import datetime, timezone
from typing import TYPE_CHECKING
from staze import Database, validation, parsing, log
from app.project.builtin_project_ids_enum import BuiltinProjectIdsEnum
from app.task.task import Task
from app.task.task_error import TaskError
from sqlalchemy.ext.hybrid import hybrid_property

if TYPE_CHECKING:
    hybrid_property = property


class TaskOrm(Database.Orm):
    _content: str = Database.column(Database.string(250), nullable=False)
    _project_id: int = Database.column(
        Database.integer, Database.foreign_key('project_orm.id'))
    _is_completed: bool = Database.column(
        Database.boolean, default=False
    )
    _creation_timestamp: float = Database.column(
        Database.float, nullable=False)
    _completion_timestamp: float = Database.column(
        Database.float, default=0.0
    )
    # TODO: Add due date...

    @classmethod
    def create(cls, content: str, project_id: int | None = None) -> 'TaskOrm':
        validation.validate(content, str)
        if project_id is None:
            # Add task to unassigned project by default
            project_id = BuiltinProjectIdsEnum.UNASSIGNED.value

        validation.validate(project_id, [int])

        model = cls(
            _content=content,
            _project_id=project_id,
            _creation_timestamp=datetime.now(timezone.utc).timestamp())
        log.bind(task_id=model.id).info('Create task')
        Database.instance().push(model)
        return cls.get_first(id=model.id)

    @hybrid_property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str):
        validation.validate(value, str)
        log.bind(task_id=self.id).info(f'Change task content to {value}')
        self._content = value

    @hybrid_property
    def project_id(self) -> int:
        return self._project_id

    @hybrid_property
    def is_completed(self) -> bool:
        return self._is_completed

    @hybrid_property
    def creation_timestamp(self) -> float:
        return self._creation_timestamp

    @hybrid_property
    def completion_timestamp(self) -> float:
        if not self.is_completed:
            raise TaskError('Task is not completed')

        return self._completion_timestamp

    @hybrid_property
    def model(self) -> Task:
        return Task(
            content=self.content,
            is_completed=self.is_completed,
            project_id=self.project_id,
            creation_timestamp=self.creation_timestamp,
            completion_timestamp=self.completion_timestamp
        )
