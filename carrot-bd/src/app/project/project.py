from staze import Model


class Project(Model):
    id: int
    name: str
    user_id: int
    task_ids: list[int]
