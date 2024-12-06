import typing as t

class Stat:

    def __init__(self, alpha: float) -> None:
        self.hit_avg = 0.0
        self.duration_hit = 0.0
        self.duration_miss = 0.0

        self.alpha = 1
        self.steps = 1
        if alpha > 1:
            self.steps = alpha
            self.is_avg = True
        elif alpha <= 1:
            self.alpha = alpha
            self.is_avg = False

    def __str__(self) -> str:
        return f"ExpSmooth({self.alpha}/{self.steps})"

    def hit(self, start, end):
        duration = end - start

        if self.is_avg:
            new_duration = (
                self.duration_hit * (self.steps - 1) + duration
            ) / self.steps
        else:
            new_duration = self.alpha * duration + (1 - self.alpha) * self.duration_hit
        self.duration_hit = new_duration

        if not self.is_avg:
            new_avg = self.alpha * 1.0 + (1 - self.alpha) * self.hit_avg
        else:
            new_avg = (self.hit_avg * (self.steps - 1) + 1) / self.steps
        self.hit_avg = new_avg

    def miss(self, start, end):
        duration = end - start

        if self.is_avg:
            new_duration = (
                self.duration_miss * (self.steps - 1) + duration
            ) / self.steps
        else:
            new_duration = self.alpha * duration + (1 - self.alpha) * self.duration_miss
        self.duration_miss = new_duration

        if not self.is_avg:
            new_avg = (1 - self.alpha) * self.hit_avg
        else:
            new_avg = self.hit_avg * self.steps / (self.steps + 1)
        self.hit_avg = new_avg

    def get(self) -> t.Tuple[float, float, float]:
        return (
            f"{self.hit_avg:.4f}",
            int(self.duration_hit),
            int(self.duration_miss),
        )
