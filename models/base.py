from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .utils import build_binary_pipeline


@dataclass
class BacktestResult:
    total: int
    correct: int

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total else 0.0


class BaseSportModel:
    MIN_PROBABILITY = 0.01
    MAX_PROBABILITY = 0.99

    def __init__(self, name: str, random_state: int = 42) -> None:
        self.name = name
        self.pipeline = build_binary_pipeline(random_state=random_state)
        self._trained = False

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        if len(X) == 0:
            raise ValueError("Training data is empty")
        self.pipeline.fit(X, y)
        self._trained = True

    def predict_probability(self, features: Iterable[float]) -> float:
        values = np.array([list(features)], dtype=float)
        if not self._trained:
            raise RuntimeError("Model must be trained before prediction")
        probability = self.pipeline.predict_proba(values)[0, 1]
        return float(np.clip(probability, self.MIN_PROBABILITY, self.MAX_PROBABILITY))

    def backtest(self, X: np.ndarray, y: np.ndarray) -> BacktestResult:
        if not self._trained:
            self.train(X, y)
        predictions = self.pipeline.predict(X)
        correct = int((predictions == y).sum())
        return BacktestResult(total=len(y), correct=correct)
