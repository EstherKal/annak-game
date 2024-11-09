

class Command:
    WORLD = 'World'
    START = 'Start'
    INPUT = 'Input'
    ASSERTS = 'Asserts'

    WAIT = 'Wait'

    SELECT = "Select"
    MOVE = "Move"
    WORK = "Work"
    DEPOSIT = "Deposit"
    TAKE_RESOURCES = "TakeResources"
    BUILD = "Build"
    MANUFACTURE = "Manufacture"
    PEOPLE = "People"
    RESOURCE = "Resource"
    RESOURCES = "Resources"
    MAKE_EMPTY = "MakeEmpty"
    RAIN = "Rain"
    ROBBER = "Robber"
    MAKE_ROBBER = "MakeRobber"

    def __init__(self, name):
        self.name = name
        self.arguments = []
        self.data = []
