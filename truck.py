from manufacture import Manufacture


class Truck(Manufacture):
    Count = 0

    def __init__(self, x, y, grid, config):
        super().__init__(x, y, 3, grid ,config)

    def increase_count(self):
        Truck.Count += 1
