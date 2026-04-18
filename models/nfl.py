from .base import BaseSportModel


class NFLModel(BaseSportModel):
    def __init__(self, random_state: int = 42) -> None:
        super().__init__(name="nfl", random_state=random_state)
