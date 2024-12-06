import math
from time import monotonic_ns


class Stat:
    def __init__(self, tau=60):
        self.hit_rate = 0.0
        self.hit_avg_duration = 0.0
        self.miss_avg_duration = 0.0
        self.last_update = monotonic_ns()
        self.tau = tau
        self.total_hits = 0
        self.total_misses = 0
    
    def __str__(self) -> str:
        return f'Smooth<{self.tau}>'

    def _update_smooth(self, old_value, current_value, elapsed_time):
        exp_factor = math.exp(-elapsed_time / self.tau)
        return old_value * exp_factor + current_value * (1 - exp_factor)

    def hit(self, start, end):
        elapsed_time = end - start
        now = end
        time_since_update = now - self.last_update

        # Update smoothed averages
        self.hit_avg_duration = self._update_smooth(
            self.hit_avg_duration, elapsed_time, time_since_update
        )

        self.total_hits += 1
        hit_rate_current = self.total_hits / (self.total_hits + self.total_misses)
        self.hit_rate = self._update_smooth(self.hit_rate, hit_rate_current, time_since_update)

        # Update last update timestamp
        self.last_update = now

    def miss(self, start, end):
        elapsed_time = end - start
        now = end
        time_since_update = now - self.last_update

        # Update smoothed averages
        self.miss_avg_duration = self._update_smooth(
            self.miss_avg_duration, elapsed_time, time_since_update
        )

        self.total_misses += 1
        hit_rate_current = self.total_hits / (self.total_hits + self.total_misses)
        self.hit_rate = self._update_smooth(self.hit_rate, hit_rate_current, time_since_update)

        # Update last update timestamp
        self.last_update = now

    def get(self):
        return (
            self.hit_rate,
            self.hit_avg_duration,
            self.miss_avg_duration,
        )