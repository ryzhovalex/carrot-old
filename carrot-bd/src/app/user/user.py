from staze import Model


class User(Model):
    username: str
    task_ids: list[int]
    project_ids: list[int]
    is_logged: bool
    active_token: str
