from staze import Test, Mock, App, Database, validation, parsing, HttpClient
from app.task.task_orm import TaskOrm
from warepy import get_enum_values
from pytest import fixture
from app.project.project import Project
from app.task.task import Task
from app.project.project_orm import ProjectOrm
from app.project.builtin_project_ids_enum import BuiltinProjectIdsEnum
from app.user.user_orm import UserOrm


class ProjectMock(Mock):
    name: str


@fixture
def project_mock() -> ProjectMock:
    return ProjectMock(name='Cats')


@fixture
def project_id(
        app: App, db: Database,
        project_mock: ProjectMock, user_id: int) -> int:
    with app.app_context():
        orm = ProjectOrm.create(name=project_mock.name, user_id=user_id)
        id = orm.id
        db.push(orm)
        return id


@fixture
def project_ids(
        app: App, db: Database, project_mock: ProjectMock,
        multi_amount: int, user_id: int) -> list[int]:
    with app.app_context():
        ids: list[int] = []
        for x in range(multi_amount):
            orm = ProjectOrm.create(
                name=project_mock.name+str(x),
                user_id=user_id)
            ids.append(orm.id)
            db.push(orm)
        return ids


class TestApiProjectsSelf(Test):
    def test_get(
        self, app: App, db: Database, project_orms: list[ProjectOrm],
        multi_amount: int, http: HttpClient, authorization_header: str
    ):
        with app.app_context():
            response = http.get(
                '/projects/self',
                200,
                headers={'Authorization': authorization_header}
            )

            json: dict = parsing.parse(response, dict)
            projects_json: list = parsing.parse_key('projects', json, list)
            assert len(projects_json) == \
                len(get_enum_values(BuiltinProjectIdsEnum)) + multi_amount

            for project_json in projects_json:
                Project(**project_json['project'])


class TestApiProjectsId(Test):
    def test_patch(
        self, app: App, db: Database, http: HttpClient,
        project_id: int
    ):
        with app.app_context():
            response = http.patch(
                f'/projects/{project_id}',
                200,
                json={
                    'name': 'newname'
                }
            )

            json: dict = parsing.parse(response.json, dict)
            project: Project = Project(**json['project'])
            project_orm = ProjectOrm.get_first(id=project_id)

            assert project_orm.name == 'newname'


class TestApiProjects(Test):
    def test_post(
        self, app: App, db: Database, http: HttpClient,
        project_mock: ProjectMock, user_id: int
    ):
        with app.app_context():
            response = http.post(
                '/projects',
                200,
                json={
                    'name': project_mock.name,
                    'user_id': user_id
                }
            )   

            json: dict = parsing.parse(response.json, dict)
            project = Project(**json['project'])
            project_orm = ProjectOrm.get_first(id=project.id)

            assert project_orm.name == project_mock.name
            assert project_orm.user_id == user_id
