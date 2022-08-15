from pytest import fixture
from app.user.user_test import user_mock, user_id
from app.task.task_test import task_mock, task_id, task_ids
from app.auth.auth_test import login_data, login_user
from app.project.project_test import project_mock, project_id, project_ids


@fixture
def multi_amount() -> int:
    return 3