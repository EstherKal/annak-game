from math import ceil
import cv2
import numpy as np


class GameObject:
    def __init__(self, startX, startY, img):
        self.x = startX
        self.y = startY
        self.targetX = startX
        self.targetY = startY
        self.isMoving = False
        self.image = img.copy()


def read_map_from_file(filename):
    map_data = []
    parsing_world = False

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "+World":
                parsing_world = True
                continue
            if line == "+Start":
                break
            if parsing_world:
                row = list(map(int, line.split()))
                map_data.append(row)

    return map_data


def read_commands_from_file(filename):
    commands = []
    parsing_commands = False

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "+Start":
                parsing_commands = True
                continue
            if parsing_commands:
                commands.append(line)

    return commands
def load_images(folder_path):
    images = {}
    # load images of tiles into images
    for i in range(1, 7):
        image_path = f"{folder_path}/tile_{i}.png"
        image = cv2.imread(image_path)
        if image is not None:
            images[i] = image.copy()
        else:
            print(f"Unable to load image: {image_path}")
    # load other img
    city_path = f"{folder_path}/city.png"
    road_path = f"{folder_path}/road.png"
    village_path = f"{folder_path}/village.png"
    person_path = f"{folder_path}/person.png"
    car_path = f"{folder_path}/car.png"
    truck_path = f"{folder_path}/truck.png"
    helicopter_path = f"{folder_path}/helicopter.png"

    for path, key in zip([city_path, road_path, village_path, person_path, car_path, truck_path, helicopter_path],
                         [100, 101, 102, 200, 201, 202, 203]):
        image = cv2.imread(path)
        if image is not None:
            images[key] = image.copy()
        else:
            print(f"Unable to load image: {path}")

    return images


def draw_grid(image, cell_size, grid_divisions):
    #?????????????????????????
    #cell_size=48 grid_d=5
    # איך הוא יודע שזה שבע שורות ושבע עשרה עמודות
    rows = image.shape[0] // cell_size
    cols = image.shape[1] // cell_size

    small_cell_size = cell_size // grid_divisions

    for i in range(rows):
        for j in range(cols):
            top_left_x = j * cell_size
            top_left_y = i * cell_size

            # Draw the smaller cells within each larger cell
            for k in range(grid_divisions + 1):
                # Vertical lines
                cv2.line(image, (top_left_x + k * small_cell_size, top_left_y),
                         (top_left_x + k * small_cell_size, top_left_y + cell_size), (200, 200, 200), 1)
                # Horizontal lines
                cv2.line(image, (top_left_x, top_left_y + k * small_cell_size),
                         (top_left_x + cell_size, top_left_y + k * small_cell_size), (200, 200, 200), 1)

            # Draw the thicker border around each larger cell
            cv2.rectangle(image, (top_left_x, top_left_y),
                          (top_left_x + cell_size, top_left_y + cell_size), (200, 200, 200), 2)  # Adjust thickness as needed


def process_commands(commands, map_image, images, cell_size, grid_divisions):
    rows = map_image.shape[0] // cell_size
    cols = map_image.shape[1] // cell_size

    for command in commands:
        parts = command.split()
        action = parts[0]
        type_object = parts[1]
        x = int(parts[2])
        y = int(parts[3])

        x //= grid_divisions
        y //= grid_divisions

        if action == "Build":
            if x < 0 or y < 0 or x >= cols or y >= rows:
                print(f"Coordinates out of bounds: ({x}, {y})")
                continue

            key_mapping = {
                "City": 100,
                "Road": 101,
                "Village": 102,
                "People": 200,
                "Car": 201,
                "Truck": 202,
                "Helicopter": 203
            }

            if type_object in key_mapping:
                type_key = key_mapping[type_object]
                if type_key in images:
                    object_selected = images[type_key]
                    obj_width, obj_height = cell_size, cell_size

                    if type_object == "City":
                        obj_width, obj_height = cell_size * 4, cell_size * 4
                    elif type_object == "Village":
                        obj_width, obj_height = cell_size * 2, cell_size * 2
                    elif type_object == "People":
                        obj_width, obj_height = cell_size // 5, cell_size // 5
                    elif type_object in ["Car", "Helicopter"]:
                        obj_width, obj_height = int(cell_size * 0.4), int(cell_size * 0.4)
                    elif type_object == "Truck":
                        obj_width, obj_height = int(cell_size * 0.6), int(cell_size * 0.6)

                    # Resize object to fit into the cell
                    object_resized = cv2.resize(object_selected, (obj_width, obj_height))

                    roi = np.s_[y * cell_size:(y * cell_size + obj_height), x * cell_size:(x * cell_size + obj_width)]

                    if roi[0].stop <= map_image.shape[0] and roi[1].stop <= map_image.shape[1]:
                        map_image[roi] = object_resized
                    else:
                        print(f"Object dimensions exceed map boundaries for type {type_object} at ({x}, {y})")
                else:
                    print(f"Image for type {type_object} not found in images dictionary.")


def main():
    world_map = read_map_from_file("input.txt")

    if not world_map:
        print("Failed to load map from file.")
        return -1

    commands = read_commands_from_file("input.txt")

    images = load_images(r"D:\python\Game\graph\images")

    if len(images) < 8:
        print("Failed to load one or more images.")
        return -1

    map_width = len(world_map[0])
    map_height = len(world_map)
    map_image = np.ones((map_height * images[1].shape[0], map_width * images[1].shape[1], 3), dtype=np.uint8) * 255
#????????????????????????????????????????????
    #למה זה 48 מאיפה זה מגיע?
    cell_size = images[1].shape[0]
    grid_divisions = 5

    for i in range(map_height):
        for j in range(map_width):
            tile_type = world_map[i][j]
            if tile_type in images:
                tile = images[tile_type]
                roi = np.s_[
                      i * tile.shape[0]:(i * tile.shape[0] + tile.shape[0]),
                      j * tile.shape[1]:(j * tile.shape[1] + tile.shape[1])
                      ]
                map_image[roi] = tile

    draw_grid(map_image, cell_size, grid_divisions)

    process_commands(commands, map_image, images, cell_size, grid_divisions)

    cv2.imshow("Map", map_image)
    cv2.waitKey(0)

    move_objects_randomly(objects, map_image, map_width, map_height, cell_size)

if __name__ == "__main__":
    main()
