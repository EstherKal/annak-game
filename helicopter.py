from manufacture import Manufacture


class Helicopter(Manufacture):
    Count = 0

    def __init__(self, x, y, grid, config):
        super().__init__(x, y, 2, grid, config)

    def increase_count(self):
        Helicopter.Count += 1
