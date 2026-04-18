from .base import BaseSportModel


class SoccerModel(BaseSportModel):
    def __init__(self, random_state: int = 42) -> None:
        super().__init__(name="soccer", random_state=random_state)
