from actions import Actions
from world import World


class Game:
    def __init__(self, world_data, config_file):
        self.world = World(world_data, config_file)
        self.actions = Actions(self.world)

    def start(self, start_data):
        self.actions.start(start_data)

    def steps(self, steps_data):
        self.actions.steps(steps_data)

    def asserts(self, assertions_data):
        self.actions.asserts(assertions_data)
