from staze import Service


class AuthService(Service):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
