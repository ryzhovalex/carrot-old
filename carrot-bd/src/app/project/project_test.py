from staze import Test, Mock, App, Database, validation, parsing, HttpClient
from app.task.task_orm import TaskOrm
from warepy import get_enum_values
from pytest import fixture
from .project import Project
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
def project_orm(
        app: App, database: Database,
        project_mock: ProjectMock) -> ProjectOrm:
    with app.app_context():
        return ProjectOrm.create(name=project_mock.name)


@fixture
def project_orms(
        app: App, database: Database, project_mock: ProjectMock,
        multi_amount: int) -> list[ProjectOrm]:
    with app.app_context():
        orms: list[ProjectOrm] = []
        for x in range(multi_amount):
            orms.append(ProjectOrm.create(name=project_mock.name+str(x)))
        return orms


class TestApiProjectsSelf(Test):
    def test_get(
        self, app: App, database: Database, project_orms: list[ProjectOrm],
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
        self, app: App, database: Database, http: HttpClient,
        project_orm: ProjectOrm
    ):
        with app.app_context():
            response = http.patch(
                f'/projects/{project_orm.id}',
                200,
                json={
                    'name': 'newname'
                }
            )

            project_orm = ProjectOrm.get_first(id=project_orm.id)

            assert project_orm.name == 'newname'


class TestApiProjects(Test):
    def test_post(
        self, app: App, database: Database, http: HttpClient,
        project_mock: ProjectMock, user_orm: UserOrm
    ):
        with app.app_context():
            response = http.post(
                '/projects',
                200,
                json={
                    'name': project_mock.name,
                    'user_id': user_orm.id
                }
            )   

            json: dict = parsing.parse(response.json, dict)
            project = Project(**json['project'])
            project_orm = ProjectOrm.get_first(id=project.id)

            assert project_orm.name == project_mock.name
            assert project_orm.user_id == user_orm.id
