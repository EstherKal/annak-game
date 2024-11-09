from entity import Entity


class Person(Entity):
    def __init__(self, x, y, grid):
        # צריך לקחת את האחד מהjson
        super().__init__(x, y, 1, grid)

# work_target_x
# work_target_y
# enum [work,]
