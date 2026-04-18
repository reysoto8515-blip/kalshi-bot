from .base import BaseSportModel


class EsportsModel(BaseSportModel):
    def __init__(self, random_state: int = 42) -> None:
        super().__init__(name="esports", random_state=random_state)
