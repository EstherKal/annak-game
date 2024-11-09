import numpy as np

from game import Game
from input import Input
"""
+World
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
+Start
Build City 1 1
+Input
Build City 31 1
Wait 1
Select 32 2
+Asserts
SelectedCategory


+World
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
+Start
Build City 1 1
+Input
Build Village 31 1
Wait 1
Select 32 2
+Asserts
VillageCount
SelectedCategory
"""

"""
+World
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
+Start
Build City 1 1
Resources 0 0 10 0 1 1
+Input
Manufacture Helicopter 1 1
+Asserts
HelicopterCount
"""
def main():
    my_input_text = Input()
    my_input_text.parse_and_store()

    config_file = "configuration.json"
    game = Game(my_input_text.world.data, config_file)
    game.start(my_input_text.start)
    game.steps(my_input_text.steps)
    game.asserts(my_input_text.asserts)


if __name__ == "__main__":
    main()
"""
+World
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
+Start
Build Village 1 1
MakeEmpty 1 1
Resource 10 Wood 1 1
People 1 22 2
Resource 1 Wood 22 2
+Input
Select 22 2
Wait 2000
Select 1 1
+Asserts
SelectedResource
"""
