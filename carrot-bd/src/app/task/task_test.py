from staze import Test, Mock, App, Database, validation, parsing, HttpClient
from app.task.task_orm import TaskOrm
from pytest import fixture
from app.task.task import Task
from app.project.project_orm import ProjectOrm
from app.project.builtin_project_ids_enum import BuiltinProjectIdsEnum
from app.user.user_orm import UserOrm


class TaskMock(Mock):
    content: str


@fixture
def task_mock(self) -> TaskMock:
    return TaskMock(content='Do some stuff')


@fixture
def task_id(
        self, app: App, db: Database,
        user_id: int,
        task_mock: TaskMock) -> int:
    with app.app_context():
        orm = TaskOrm.create(
            content=task_mock.content,
            user_id=user_id)
        id = orm.id
        db.push(orm)
        return id


@fixture
def task_ids(
        self, app: App, db: Database, task_mock: TaskMock,
        user_id: int,
        multi_amount: int) -> list[int]:
    with app.app_context():
        ids: list[int] = []
        for x in range(multi_amount):
            orm = TaskOrm.create(
                content=task_mock.content+str(x),
                user_id=user_id)
            ids.append(orm.id)
            db.push(orm)
        return ids


class TestApiTasksSelf(Test):
    def test_get(
            self, app: App, db: Database, http: HttpClient,
            task_ids: list[int], multi_amount: int,
            authorization_header: str):
        with app.app_context():
            response = http.get(
                '/tasks/self',
                200,
                headers={'Authorization': authorization_header})

            json: dict = parsing.parse(response.json, dict)
            tasks_json: list = parsing.parse_key('tasks', json, list)
            assert len(tasks_json) == multi_amount

            for task_json in tasks_json:
                Task(**task_json['task'])


class TestApiTasksId(Test):
    def test_patch_content(
        self, app: App, db: Database, http: HttpClient,
        task_orm: TaskOrm
    ):
        with app.app_context():
            response = http.patch(
                f'/tasks/{task_orm.id}',
                200,
                json={
                    'content': 'newcontent'
                }
            )

            json: dict = parsing.parse(response.json, dict)
            task: Task = Task(**json['task'])
            task_orm = TaskOrm.get_first(id=task.id)

            assert task_orm.content == 'newcontent'

    def test_patch_project(
        self, app: App, db: Database, http: HttpClient,
        task_orm: TaskOrm, project_orm: ProjectOrm
    ):
        with app.app_context():
            response = http.patch(
                f'/tasks/{task_orm.id}',
                200,
                json={
                    'project_id': project_orm.id
                }
            )

            json: dict = parsing.parse(response.json, dict)
            task: Task = Task(**json['task'])
            task_orm = TaskOrm.get_first(id=task.id)

            assert task_orm.project_id == project_orm.id

    def test_patch(
        self, app: App, db: Database, http: HttpClient,
        task_orm: TaskOrm, project_orm: ProjectOrm
    ):
        with app.app_context():
            response = http.patch(
                f'/tasks/{task_orm.id}',
                200,
                json={
                    'content': 'newcontent',
                    'project_id': project_orm.id
                }
            )

            json: dict = parsing.parse(response.json, dict)
            task: Task = Task(**json['task'])
            task_orm = TaskOrm.get_first(id=task.id)

            assert task_orm.content == 'newcontent'
            assert task_orm.project_id == project_orm.id


class TestApiTasks(Test):
    def test_post(
        self, app: App, db: Database, http: HttpClient,
        task_mock: TaskMock
    ):
        with app.app_context():
            response = http.post(
                '/tasks',
                200,
                json={
                    'content': 'Pet cat'
                })
            
            json: dict = parsing.parse(response.json, dict)
            task: Task = Task(**json['task'])
            task_orm = TaskOrm.get_first(id=task.id)

            assert task_orm.content == 'Pet cat'
            assert task_orm.project_id == BuiltinProjectIdsEnum.UNASSIGNED

    def test_post_with_project(
        self, app: App, db: Database, http: HttpClient,
        task_mock: TaskMock, project_orm: ProjectOrm
    ):
        with app.app_context():
            response = http.post(
                '/tasks',
                200,
                json={
                    'content': 'Pet cat',
                    'project_id': project_orm.id
                })
            
            json: dict = parsing.parse(response.json, dict)
            task: Task = Task(**json['task'])
            task_orm = TaskOrm.get_first(id=task.id)

            assert task_orm.content == 'Pet cat'
            assert task_orm.project_id == project_orm.id


class TestApiTasksIdComplete(Test):
    def post(
        self, app: App, db: Database, http: HttpClient, task_id: int
    ):
        with app.app_context():
            response = http.post(
                f'/tasks/{task_id}/complete',
                200
            )

            json: dict = parsing.parse(response.json, dict)
            task = Task(**json['task'])
            task_orm = TaskOrm.get_first(id=task.id)

            assert task.is_completed
            assert task_orm.is_completed
