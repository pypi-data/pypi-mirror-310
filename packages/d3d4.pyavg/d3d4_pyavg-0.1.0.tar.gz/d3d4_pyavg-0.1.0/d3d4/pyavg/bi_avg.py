from threading import Lock
from typing import Tuple


class Stat:
    def __init__(self, alpha: float = 0.3, beta: float = 0.2):
        """
        Initialize CacheStats with smoothing parameters.

        :param alpha: Smoothing factor for average values.
        :param beta: Smoothing factor for trend values.
        """
        if not (0 < alpha <= 1 and 0 < beta <= 1):
            raise ValueError("alpha and beta must be in the range (0, 1]")

        self.alpha = alpha
        self.beta = beta

        self.hit_count = 0
        self.miss_count = 0

        self.hit_duration_avg = 0.0
        self.miss_duration_avg = 0.0

        self.hit_trend = 0.0
        self.miss_trend = 0.0

        self.lock = Lock()

    def __str__(self) -> str:
        return f"BiAvg<{self.alpha}/{self.beta}>"

    def hit(self, start: float, end: float):
        """
        Update hit statistics with a new duration.
        :param start: Start time in seconds.
        :param end: End time in seconds.
        """
        duration = end - start  # Convert to microseconds
        with self.lock:
            self.hit_count += 1
            prev_avg = self.hit_duration_avg
            self.hit_duration_avg = self.alpha * duration + (1 - self.alpha) * (
                self.hit_duration_avg + self.hit_trend
            )
            self.hit_trend = (
                self.beta * (self.hit_duration_avg - prev_avg)
                + (1 - self.beta) * self.hit_trend
            )

    def miss(self, start: float, end: float):
        """
        Update miss statistics with a new duration.
        :param start: Start time in seconds.
        :param end: End time in seconds.
        """
        duration = end - start  # Convert to microseconds
        with self.lock:
            self.miss_count += 1
            prev_avg = self.miss_duration_avg
            self.miss_duration_avg = self.alpha * duration + (1 - self.alpha) * (
                self.miss_duration_avg + self.miss_trend
            )
            self.miss_trend = (
                self.beta * (self.miss_duration_avg - prev_avg)
                + (1 - self.beta) * self.miss_trend
            )

    def get(self) -> Tuple[float, float, float]:
        """
        Get the current hit rate, average hit duration, and average miss duration.
        :return: Tuple of hit rate, average hit duration (in microseconds), and average miss duration (in microseconds).
        """
        with self.lock:
            total = self.hit_count + self.miss_count
            hit_rate = self.hit_count / total if total > 0 else 0.0
            return hit_rate, self.hit_duration_avg, self.miss_duration_avg
