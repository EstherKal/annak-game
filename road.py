from entity import Entity


class Road(Entity):
    Count = 0

    def __init__(self, x, y, grid):
        super().__init__(x, y, 5, grid)

    def increase_count(self):
        Road.Count += 1
