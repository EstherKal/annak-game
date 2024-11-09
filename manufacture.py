# המחלקה הזו דומה מאוד לENTITY כרגע זה שתי מחלקות כדי שיהיה קרור אם צריך לבדוק כביש
# אבל צריך בעקרון לסדר את זה אחרת



class Manufacture:
    def __init__(self, x, y, size, grid, config):
        self.x = x
        self.y = y
        self.size = size
        # dict{resource_number, resource_count}
        self.dict_resources = {}
        self.dict_transportation = {}
        self.grid = grid
        self.config = config
        self.build()

    # virtual
    def increase_count(self):
        pass

    # build a car truck helikopter
    def build(self):
        if self.x < 1 or self.y < 1 or self.x + self.size - 1 > len(self.grid[0]) or self.y + self.size - 1 > len(
                self.grid[1]):
            raise Exception("Out of range")

        for i in range(self.y - 1, self.y + self.size - 1):
            for j in range(self.x - 1, self.x + self.size - 1):
                if int(self.grid[i][j].tile.tile_number) != 1:
                    raise Exception("Not a ground can't build")

        if self.has_resources():
            for i in range(self.y - 1, self.y + self.size - 1):
                for j in range(self.x - 1, self.x + self.size - 1):
                    self.grid[i][j].add_entity(self)

            self.increase_count()

    # return true if there is nothing in this place

    def has_resources(self):
        # if there is no entity
        if not self.grid[self.y][self.x].array_entity:
            return True
        # if there is no resources
        if not self.grid[self.y][self.x].array_entity[0].dict_resources:
            return False
        from car import Car
        from truck import Truck
        if isinstance(self, Car):
            type_manufacture = "Car"
        elif isinstance(self, Truck):
            type_manufacture = "Truck"
        else:
            type_manufacture = "Helicopter"
        costs = self.config["Costs"][type_manufacture]
        type_of_resources = self.config["ResourceTypes"]
        for i in range(len(costs)):
            if int(self.grid[self.y][self.x].array_entity[0].dict_resources[type_of_resources[i]]) < int(costs[i]):
                return False
        return True
