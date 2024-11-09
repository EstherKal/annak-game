import cv2
import numpy as np
import os
import random
import time


# Define a game object class
class GameObject:
    def __init__(self, obj_type, position, image):
        self.obj_type = obj_type
        self.position = position
        self.image = image
        self.target = None

    def move_towards_target(self):
        if self.target is None:
            return

        current_x, current_y = self.position
        target_x, target_y = self.target
        step_size = 1  # Change this to adjust movement speed

        # Calculate direction vector and move one step
        direction_x = target_x - current_x
        direction_y = target_y - current_y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

        if distance == 0:
            self.target = None
        else:
            move_x = int(step_size * direction_x / distance)
            move_y = int(step_size * direction_y / distance)
            self.position = (current_x + move_x, current_y + move_y)


# Function to read the map from the text file
def read_map_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    map_data = []
    game_objects = []
    reading_world = False
    reading_start = False

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        if line.startswith('+'):
            if line.startswith('+world'):
                reading_world = True
                reading_start = False
            elif line.startswith('+start'):
                reading_world = False
                reading_start = True
            continue

        if reading_world:
            row = list(map(int, line.split()))
            map_data.append(row)
        elif reading_start:
            parts = line.split()
            obj_type = parts[0]
            position = (int(parts[1]), int(parts[2]))
            game_objects.append((obj_type, position))

    if not map_data:
        print("Error: Map data is empty or not loaded correctly.")
    if not game_objects:
        print("Error: Game objects data is empty or not loaded correctly.")

    return map_data, game_objects


# Function to load images from the resource folder
def load_images(folder_path):
    images = {}
    for i in range(1, 7):  # Example: up to 6 images
        image_path = os.path.join(folder_path, f"tile_{i}.png")
        image = cv2.imread(image_path)
        if image is not None:
            images[i] = image
        else:
            print(f"Unable to load image: {image_path}")

    object_images = {}
    object_images["people"] = cv2.imread(os.path.join(folder_path, "person.png"))
    object_images["car"] = cv2.imread(os.path.join(folder_path, "car.png"))
    object_images["truck"] = cv2.imread(os.path.join(folder_path, "truck.png"))
    object_images["helicopter"] = cv2.imread(os.path.join(folder_path, "helicopter.png"))

    return images, object_images


# Function to draw the grid on the image
def draw_grid(image, cell_size, grid_divisions):
    rows = image.shape[0] // cell_size
    cols = image.shape[1] // cell_size

    for i in range(rows + 1):
        cv2.line(image, (0, i * cell_size), (image.shape[1], i * cell_size), (200, 200, 200), 2)
    for j in range(cols + 1):
        cv2.line(image, (j * cell_size, 0), (j * cell_size, image.shape[0]), (200, 200, 200), 2)


    small_cell_size = cell_size // grid_divisions

    for i in range(rows):
        for j in range(cols):
            for k in range(1, grid_divisions):
                cv2.line(image, (j * cell_size + k * small_cell_size, i * cell_size),
                         (j * cell_size + k * small_cell_size, (i + 1) * cell_size), (200, 200, 200), 1)
                cv2.line(image, (j * cell_size, i * cell_size + k * small_cell_size),
                         ((j + 1) * cell_size, i * cell_size + k * small_cell_size), (200, 200, 200), 1)


def main():
    world_map, game_objects_data = read_map_from_file('world.txt')

    if not world_map:
        print("World map is empty or not loaded correctly.")
        return

    images, object_images = load_images('D:/python/Game/tiles')

    if not images:
        print("No images loaded. Please check the image directory and file names.")
        return

    map_height = len(world_map)
    map_width = len(world_map[0])
    tile_size = 20  # Size of each cell in the grid
    cell_size = tile_size * 5  # Size of each main grid cell

    map_image = np.zeros((map_height * cell_size, map_width * cell_size, 3), dtype=np.uint8)

    # Draw the map on the image
    for i in range(map_height):
        for j in range(map_width):
            tile_type = world_map[i][j]
            if tile_type not in images:
                print(f"Tile type {tile_type} not found in images.")
                continue
            tile = cv2.resize(images[tile_type], (cell_size, cell_size))
            y = i * cell_size
            x = j * cell_size
            map_image[y:y + cell_size, x:x + cell_size] = tile
    # Calculate small cell size based on the grid divisions


    # Initialize game objects
    game_objects = []
    for obj_type, position in game_objects_data:
        if obj_type in object_images:
            image = cv2.resize(object_images[obj_type], (tile_size, tile_size))
            game_objects.append(GameObject(obj_type, position, image))
    # Main loop
    while True:
        # Handle object movement
        for obj in game_objects:
            if obj.target is None:
                obj.target = (
                    random.randint(0, map_width * cell_size - 1), random.randint(0, map_height * cell_size - 1))
            obj.move_towards_target()

        # Draw the map and objects
        display_image = map_image.copy()
        draw_grid(display_image, cell_size, 5)
        for obj in game_objects:
            y, x = obj.position
            y_pixel = y * cell_size + (tile_size - obj.image.shape[0]) // 2
            x_pixel = x * cell_size + (tile_size - obj.image.shape[1]) // 2
            display_image[y_pixel:y_pixel + tile_size, x_pixel:x_pixel + tile_size] = obj.image

        # Show the image
        cv2.imshow('World Map', display_image)
        if cv2.waitKey(100) == 27:  # Press 'ESC' to exit
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
