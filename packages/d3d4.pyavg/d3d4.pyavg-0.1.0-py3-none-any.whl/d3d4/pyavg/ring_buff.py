class RingBuff:
    def __init__(self, size=100) -> None:
        self.buff = [0] * size
        self.size = size
        self.sum = 0
        self.count = 0
        self.index = 0

    def Add(self, value: int):
        if self.count >= self.size:
            self.sum -= self.buff[self.index]
        else:
            self.count += 1

        self.buff[self.index] = value
        self.sum += value

        self.index = (self.index + 1) % self.size

    def Average(self) -> float:
        if self.count == 0:
            return 0.0
        return self.sum / float(self.count)


class Stat:
    def __init__(self, size: int) -> None:
        self.size = size
        self.hit_rate = RingBuff(size)
        self.hit_duration = RingBuff(size)
        self.miss_duration = RingBuff(size)

    def __str__(self) -> str:
        return f"Rb{self.size}"

    def hit(self, start, end):
        self.hit_rate.Add(1)
        self.hit_duration.Add(end - start)

    def miss(self, start, end):
        self.hit_rate.Add(0)
        self.miss_duration.Add(end - start)

    def get(self):
        return (
            f"{self.hit_rate.Average()}",
            self.hit_duration.Average(),
            self.miss_duration.Average(),
        )
