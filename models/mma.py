from .base import BaseSportModel


class MMAModel(BaseSportModel):
    def __init__(self, random_state: int = 42) -> None:
        super().__init__(name="mma", random_state=random_state)
