from .base import BaseSportModel


class NBAModel(BaseSportModel):
    def __init__(self, random_state: int = 42) -> None:
        super().__init__(name="nba", random_state=random_state)
