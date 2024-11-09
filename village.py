from entity import Entity


class Village(Entity):
    Count = 0

    def __init__(self, x, y, grid, config, from_steps=True):
        # בעקרון צריך לשלוף מהJSON את הגודל
        super().__init__(x, y, 10, grid, config, from_steps)

    def increase_count(self):
        Village.Count += 1
