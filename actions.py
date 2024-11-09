from helicopter import Helicopter
from car import Car
from truck import Truck
from road import Road
from village import Village
from city import City
from cell import Cell
from person import Person


class Actions:
    def __init__(self, world):
        self.world = world

    # =======================start============
    def resource(self, index):
        x = int(index.arguments[2])
        y = int(index.arguments[3])
        if not self.world.grid[y][x].array_entity:
            self.world.grid[y][x].tile.resource_amount += int(index.arguments[0])
        else:
            if index.arguments[1] in self.world.grid[y][x].array_entity[0].dict_resources:
                self.world.grid[y][x].array_entity[0].dict_resources += int(index.arguments[0])
            else:
                self.world.grid[y][x].array_entity[0].dict_resources[index.arguments[1]] = int(index.arguments[0])

    def people_start(self, index):
        x = int(index.arguments[1])
        y = int(index.arguments[2])
        person = Person(x, y, self.world.grid)
        self.world.grid[y][x].add_entity(person)

    def build_start(self, index):
        x = int(index.arguments[1])
        y = int(index.arguments[2])
        if index.arguments[0] == 'City':
            City(x, y, self.world.grid, self.world.config, from_steps=False)

        elif index.arguments[0] == 'Village':
            Village(x, y, self.world.grid, self.world.config, from_steps=False)
        else:
            Road(x, y, self.world.grid)

    def make_empty(self, index):
        x = int(index.arguments[0])
        y = int(index.arguments[1])
        self.world.grid[y][x].array_entity[0].dict_resources.clear()

    def resources(self, index):
        x = int(index.arguments[4])
        y = int(index.arguments[5])

        type_entity = {
            City: 'City',
            Truck: 'Truck',
            Village: 'Village',
            Car: 'Car',
            Helicopter: 'Helicopter'
        }
        # see what class it is and find the array capacity in config
        for entity_class, entity_name in type_entity.items():
            if isinstance(self.world.grid[y][x].array_entity[0], entity_class):
                capacity_array = self.world.config["Capacities"][entity_name]
                break
        name_of_resources = self.world.config["ResourceTypes"]
        # if there is resources add more
        if self.world.grid[y][x].array_entity[0].dict_resources:
            for i in range(4):
                # if it's more than the capacity so put the capacity amount if not put the amount that was given
                # amount_of_resource = int(self.grid[y][x].array_entity[0].dict_resources[name_of_resources[i]])
                if (int(self.world.grid[y][x].array_entity[0].dict_resources[name_of_resources[i]]) + int(
                        index.arguments[i])) > int(capacity_array[i]):
                    self.world.grid[y][x].array_entity[0].dict_resources[name_of_resources[i]] = int(capacity_array[i])
                else:
                    self.world.grid[y][x].array_entity[0].dict_resources[name_of_resources[i]] += int(
                        index.arguments[i])
        # if there are no resources
        else:
            # put either capacity amount or given amount
            for i in range(4):
                if int(index.arguments[i]) > int(capacity_array[i]):
                    self.world.grid[y][x].array_entity[0].dict_resources[name_of_resources[i]] = int(capacity_array[i])
                else:
                    self.world.grid[y][x].array_entity[0].dict_resources[name_of_resources[i]] = int(index.arguments[i])

    def start(self, start):
        actions = {
            'Resource': self.resource,
            'People': self.people_start,
            'Build': self.build_start,
            'MakeEmpty': self.make_empty,
            'Resources': self.resources
            # 'Manufacture': self.manufacture
        }
        for index in start:
            if index.name in actions:
                actions[index.name](index)

    # ===============================steps==================

    def people(self, index):
        x = int(index.arguments[1])
        y = int(index.arguments[2])
        entity = self.world.grid[int(self.world.select.y)][int(self.world.select.x)].array_entity[0]
        entity_map = {
            City: "City",
            Village: "Village",
            Road: "Road",
        }
        capacite_entity = int(self.world.config["Capacities"][entity_map.get(type(entity))][4])
        if int(index.arguments[0]) > capacite_entity:
            index.arguments[0] = capacite_entity
        self.world.grid[y][x].array_entity[0].dict_resources["people"] = int(index.arguments[0])

    def select_func(self, index):
        # קודם לאנטטטי שאין שם משאב
        self.world.select = Cell(index.arguments[0], index.arguments[1],
                                 self.world.grid[int(index.arguments[1])][int(index.arguments[0])].tile)

    def work(self, index):

        self.world.grid[int(self.world.select.x)][int(self.world.select.y)].array_entity.pop(0)
        x = int(index.arguments[0])
        y = int(index.arguments[1])
        self.world.grid[y][x].tile.resource_amount -= 1

    def build(self, index):
        x = int(index.arguments[1])
        y = int(index.arguments[2])
        if index.arguments[0] == 'City':
            City(x, y, self.world.grid, self.world.config)
        elif index.arguments[0] == 'Village':
            Village(x, y, self.world.grid, self.world.config)
        else:
            Road(x, y, self.world.grid, self.world.config)

    def rain(self, index):
        self.world.rain_wood += int(index.arguments[0])
        while self.world.rain_wood >= self.world.config["Rains"]["Wood"]:
            self.world.rain_wood -= int(index.arguments[0])
            for i in range(0, len(self.world.grid), 5):
                for j in range(0, len(self.world.grid[0]), 5):
                    if int(self.world.grid[i][j].tile.tile_number) == 3:
                        self.world.grid[i][j].tile.resource_amount += 1
        self.world.rain_wool += int(index.arguments[0])
        while self.world.rain_wool >= self.world.config["Rains"]["Wool"]:
            self.world.rain_wool -= int(index.arguments[0])
            for i in range(0, len(self.world.grid), 5):
                for j in range(0, len(self.world.grid[0]), 5):
                    if int(self.world.grid[i][j].tile.tile_number) == 4:
                        self.world.grid[i][j].tile.resource_amount += 1

    def take_resources(self, index):
        x = int(index.arguments[0])
        y = int(index.arguments[1])
        x_selected = int(self.world.select.x)
        y_selected = int(self.world.select.y)
        if isinstance(self.world.grid[y_selected][x_selected].array_entity[0], Car):
            trans = "Car"
        elif isinstance(self.world.grid[y_selected][x_selected].array_entity[0], Truck):
            trans = "Truck"
        elif isinstance(self.world.grid[y_selected][x_selected].arrey_entity[0], Helicopter):
            trans = "Helicopter"

        # אם אני יום אחד ארצה לגשת למערך של משאבים בעיר ולקחת מכולם
        # list_of_resources=list(self.grid[y][x].array_entity[0].dict_resources.keys)

        # the first resource that is in the entity
        resource_to_take = next(iter(self.world.grid[y][x].array_entity[0].dict_resources))

        # finds the number of the resource in the resource array in the config
        for index, resource in enumerate(self.world.config["ResourceTypes"]):
            if resource == resource_to_take:
                num_of_resource = index
                break
        # keeps the capacity of this resource for the selected entity
        capacity = self.world.config["Capacities"][trans][num_of_resource]
        # if the entity has the resource return
        if resource_to_take in self.world.grid[y_selected][x_selected].array_entity[0].dict_resources:
            if capacity == self.world.grid[y_selected][x_selected].array_entity[0].dict_resources[resource_to_take]:
                return
        # add to the entity the resource with the amount
        self.world.grid[y_selected][x_selected].array_entity[0].dict_resources[resource_to_take] = capacity

        if not self.world.grid[y][x].array_entity:
            self.world.grid[y][x].tile.resource_amount -= 1

        # take off capacity amount from the resource
        else:
            for resource, amount in self.world.grid[y][x].array_entity[0].dict_resources.items():
                self.world.grid[y][x].array_entity[0].dict_resources[resource] = amount - capacity

    def manufacture(self, index):

        x = int(index.arguments[1])
        y = int(index.arguments[2])
        if index.arguments[0] == 'Car':
            Car(x, y, self.world.grid, self.world.config)
        elif index.arguments[0] == 'Truck':
            Truck(x, y, self.world.grid, self.world.config)
        else:
            Helicopter(x, y, self.world.grid, self.world.config)

    def steps(self, steps):
        actions = {
            'Select': self.select_func,
            'Work': self.work,
            'Build': self.build,
            'Rain': self.rain,
            'People': self.people,
            'TakeResources': self.take_resources,
            'Manufacture': self.manufacture

        }

        for index in steps:
            if index.name in actions:
                actions[index.name](index)

        # =================asserts=================

    def selected_category(self, index):
        x = int(self.world.select.x)
        y = int(self.world.select.y)
        # if it's a city village or road print the entity
        if self.world.grid[y][x].array_entity:
            if isinstance(self.world.grid[y][x].array_entity[0], City):
                print(index, " City")
            elif isinstance(self.world.grid[y][x].array_entity[0], Village):
                print(index, " Village")
            elif isinstance(self.world.grid[y][x].array_entity[0], Road):
                print(index, " Road")
        else:
            name = ""
            for key, val in self.world.config["Tiles"].items():
                if val == int(self.world.grid[y][x].tile.tile_number):
                    name = key
                    break
            print(index, name)

    def selected_resource(self, index):
        string = ""
        x = int(self.world.select.x)
        y = int(self.world.select.y)
        if not self.world.grid[y][x].array_entity:
            # לבדור עם המערך ריק ואם לר ללכך לאניטטי ומספיס כמה משאבים יש לו
            tile_number = self.world.grid[y][x].tile.tile_number
            for i in range(0, 4):
                if int(tile_number) - 3 == i:
                    string += str(self.world.grid[int(self.world.select.y)][
                                      int(self.world.select.x)].tile.resource_amount) + " "
                else:
                    string += "0 "
            print(index, string)
        else:
            dict_resorces = {'Wood': 0,
                             'Wool': 0,
                             'Iron': 0,
                             'Blocks': 0}
            resources = self.world.grid[y][x].array_entity[0].dict_resources
            for resource, amount in resources.items():
                dict_resorces[resource] += amount
            print(index, [val for val in dict_resorces.values()])

    def city_count(self, index):
        print(index, " ", City.Count)

    def village_count(self, index):
        print(index, " ", Village.Count)

    def road_count(self, index):
        print(index, " ", Road.Count)

    def car_count(self, index):
        print(index, " ", Car.Count)

    def truck_count(self, index):
        print(index, " ", Truck.Count)

    def helicopter_count(self, index):
        print(index, " ", Helicopter.Count)

        # ?????????????????

    def selected_complete(self, index):
        print(index, False)

    def selected_people(self, index):
        x = int(self.world.select.x)
        y = int(self.world.select.y)
        amount_people = self.world.grid[y][x].array_entity[0].dict_resources["people"]
        print(index, amount_people)
        # return self.select

    def selected_transportation(self, index):
        transportation = index[8:]
        x = int(self.world.select.x)
        y = int(self.world.select.y)
        transportation_amount = self.world.grid[y][x].array_entity[0].dict_transportation[transportation]
        print(index, transportation_amount)

    def asserts(self, asserts):
        actions = {
            'SelectedCategory': self.selected_category,
            'SelectedResource': self.selected_resource,
            'CityCount': self.city_count,
            'VillageCount': self.village_count,
            'RoadCount': self.road_count,
            'SelectedComplete': self.selected_complete,
            'SelectedPeople': self.selected_people,
            'SelectedCar': self.selected_transportation,
            'SelectedTruck': self.selected_transportation,
            'SelectedHelicopter': self.selected_transportation,
            'CarCount': self.car_count,
            'TruckCount': self.truck_count,
            'HelicopterCount': self.helicopter_count
        }
        for index in asserts:
            if index in actions:
                actions[index](index)
