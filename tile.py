class Tile:

    def __init__(self, tile_number):
        # self.x = x
        # self.y = y
        self.tile_number = tile_number
        # צריך לאתחל את המשאבים לפי המספר שקיבל........
        self.resource_amount = 0

        def print_resources():
            print([resource for resource in self.resources])

        def update_tile(resources, people):
            self.resources = resources
            self.people = people
