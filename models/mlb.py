from .base import BaseSportModel


class MLBModel(BaseSportModel):
    def __init__(self, random_state: int = 42) -> None:
        super().__init__(name="mlb", random_state=random_state)
