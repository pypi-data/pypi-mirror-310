import typing as t


class Stat:
    hit_count = 0.0
    miss_count = 0.0
    hit_duration = 0.0
    miss_duration = 0.0

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Average"

    def hit(self, start, end):
        duration = end - start
        self.hit_count += 1
        self.hit_duration += duration

    def miss(self, start, end):
        duration = end - start
        self.miss_count += 1
        self.miss_duration += duration

    def get(self) -> t.Tuple[float, float, float]:
        if self.hit_count + self.miss_count != 0:
            hit_rate = self.hit_count / (self.hit_count + self.miss_count)
        else:
            hit_rate = 0.0
        if self.hit_count == 0:
            avg_hit_time = 0
        else:
            avg_hit_time = self.hit_duration / self.hit_count

        if self.miss_count == 0:
            avg_miss_time = 0.0
        else:
            avg_miss_time = self.miss_duration / self.miss_count

        return f"{hit_rate:.4f}", int(avg_hit_time), int(avg_miss_time)
