from manufacture import Manufacture


class Car(Manufacture):
    Count = 0

    def __init__(self, x, y, grid, config):
        super().__init__(x, y, 2, grid, config)

    def increase_count(self):
        Car.Count += 1
