from staze import Model


class Task(Model):
    id: int
    content: str
    project_id: int
    is_completed: bool
    creation_timestamp: float
    completion_timestamp: float
