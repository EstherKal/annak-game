


class Entity:
    def __init__(self, x, y, size, grid, config, from_steps=True):
        self.x = x
        self.y = y
        self.size = size
        # dict{resource_number, resource_count}
        self.dict_resources = {}
        self.dict_transportation = {}
        self.grid = grid
        self.config = config
        self.build(from_steps)

    # virtual
    def increase_count(self):
        pass

    # build a city road or village
    def build(self, from_steps):
        if self.x < 1 or self.y < 1 or self.x + self.size - 1 > len(self.grid[0]) or self.y + self.size - 1 > len(
                self.grid[1]):
            raise Exception("Out of range")

        for i in range(self.y - 1, self.y + self.size - 1):
            for j in range(self.x - 1, self.x + self.size - 1):
                if int(self.grid[i][j].tile.tile_number) != 1:
                    raise Exception("Not a ground can't build a city")

        # check if there is a road
        from road import Road
        if from_steps and not isinstance(self, Road):
            # if there is no road
            if not self.check_road():
                return

        for i in range(self.y - 1, self.y + self.size - 1):
            for j in range(self.x - 1, self.x + self.size - 1):
                self.grid[i][j].add_entity(self)

        #add resources
        from city import City
        if isinstance(self, City):
            type_entity = "City"
        else:
            type_entity = "Village"
        name_of_resources = self.config["ResourceTypes"]
        amount_of_resources = self.config["Capacities"][type_entity]
        for i in range(len(name_of_resources)):
            self.dict_resources[name_of_resources[i]] = amount_of_resources[i]

        self.increase_count()

    # check if there is a road
    def check_road(self):

        check_cells = []
        if self.size == 20:
            # Specific check cells for a city (48 cells)
            check_cells = [
                              (self.x - 2, self.y + i) for i in range(3, 15)  # Left side
                          ] + [
                              (self.x + self.size - 1, self.y + i) for i in range(3, 15)  # Right side
                          ] + [
                              (self.x + i, self.y - 2) for i in range(3, 15)  # Top side
                          ] + [
                              (self.x + i, self.y + self.size - 1) for i in range(3, 15)  # Bottom side
                          ]

        elif self.size == 10:
            # Specific check cells for a village (8 cells)
            check_cells = [
                (self.x - 2, self.y + 3), (self.x - 2, self.y + 4),
                (self.x + self.size - 1, self.y + 3), (self.x + self.size - 1, self.y + 4),
                (self.x + 3, self.y - 2), (self.x + 4, self.y - 2),
                (self.x + 3, self.y + self.size - 1), (self.x + 4, self.y + self.size - 1)
            ]

        for (cx, cy) in check_cells:
            if self.is_road(cx, cy):
                return True

        return False

    # if the cell is a road
    def is_road(self, x, y):
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return self.grid[y][x].array_entity
        return False

