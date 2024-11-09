class Cell:
    def __init__(self, x, y, tile=None):
        self.x = x
        self.y = y
        self.array_entity = []
        self.tile = tile

    def add_entity(self, entity):
        self.array_entity.append(entity)
