import time
from threading import Lock
from typing import Tuple


class Stat:
    def __init__(self, alpha: float = 0.5, beta: float = 0.3, gamma: float = 0.2, integral_limit: float = 200):
        """
        Initialize CacheStats with PID-like smoothing parameters.
        :param alpha: Proportional coefficient.
        :param beta: Integral coefficient.
        :param gamma: Derivative coefficient.
        """

        # alpha + beta should ber equal 1 for better percision
        if not (0 < alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1):
            raise ValueError("alpha, beta, and gamma must be in the range [0, 1] and alpha > 0")

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.integral_limit = integral_limit

        self.hit_count = 0
        self.miss_count = 0

        self.hit_integral = 0.0
        self.miss_integral = 0.0

        self.hit_prev_value = None
        self.miss_prev_value = None

        self.hit_duration_avg = 0.0
        self.miss_duration_avg = 0.0

        self.lock = Lock()
    def __str__(self) -> str:
        return f'PID<{self.alpha},{self.beta},{self.gamma},{self.integral_limit}>'

    def hit(self, start: float, end: float):
        """
        Update hit statistics with a new duration.
        :param start: Start time in seconds.
        :param end: End time in seconds.
        """
        duration = end - start  # Convert to microseconds
        with self.lock:
            self.hit_count += 1

            # Update integral component
            # self.hit_integral += duration
            self.hit_integral = (
                self.hit_integral * (self.integral_limit - 1) + duration
            ) / self.integral_limit

            # Update derivative component
            derivative = 0.0
            if self.hit_prev_value is not None:
                derivative = duration - self.hit_prev_value

            # Calculate new average with PID components
            self.hit_duration_avg = (
                self.alpha * duration +
                self.beta * self.hit_integral +
                self.gamma * derivative
            )

            # Store current value for next derivative calculation
            self.hit_prev_value = duration

    def miss(self, start: float, end: float):
        """
        Update miss statistics with a new duration.
        :param start: Start time in ns.
        :param end: End time in ns.
        """
        duration = end - start  # Convert to microseconds
        with self.lock:
            self.miss_count += 1

            # Update integral component
            # self.miss_integral += duration
            self.miss_integral = (
                self.miss_integral * (self.integral_limit - 1) + duration
            ) / self.integral_limit

            # Update derivative component
            derivative = 0.0
            if self.miss_prev_value is not None:
                derivative = duration - self.miss_prev_value

            # Calculate new average with PID components
            self.miss_duration_avg = (
                self.alpha * duration +
                self.beta * self.miss_integral +
                self.gamma * derivative
            )

            # Store current value for next derivative calculation
            self.miss_prev_value = duration

    def get(self) -> Tuple[float, float, float]:
        """
        Get the current hit rate, average hit duration, and average miss duration.
        :return: Tuple of hit rate, average hit duration (ns), and average miss duration (ns).
        """
        with self.lock:
            total = self.hit_count + self.miss_count
            hit_rate = self.hit_count / total if total > 0 else 0.0
            return hit_rate, int(self.hit_duration_avg), int(self.miss_duration_avg)
