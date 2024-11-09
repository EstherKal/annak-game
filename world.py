import json

from actions import Actions
from helicopter import Helicopter
from car import Car
from truck import Truck
from road import Road
from village import Village
from city import City
from tile import Tile
from cell import Cell
from person import Person


class World:
    def __init__(self, data, file_direct):
        self.data = data
        self.grid = []
        self.file_direct = file_direct
        with open(self.file_direct, 'r') as f:
            self.config = json.load(f)
        self.tile_size = self.config["Sizes"]["Tile"][0]
        f.close()
        self.initialize_tiles()
        self.select = Cell(-1, -1)
        self.rain_wood = 0
        self.rain_wool = 0
        self.actions=Actions(self)

    def initialize_tiles(self):
        rows = len(self.data)
        cols = len(self.data[0])
        self.grid = [[None for _ in range(cols * 5)] for _ in range(rows * 5)]

        for i in range(rows):
            for j in range(cols):
                num = self.data[i][j]
                tile = Tile(num)
                for x in range(5):
                    for y in range(5):
                        self.grid[i * 5 + x][j * 5 + y] = Cell(i * 5 + x, j * 5 + y, tile)

        return self.grid

    def print_matrix(self):
        for row in self.grid:
            for cell in row:
                if cell.array_entity:
                    print(f"T({cell.array_entity[0].size})", end=" ")
                else:
                    print("T(0)", end=" ")
            print()

