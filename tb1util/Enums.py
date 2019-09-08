class Direction:
    LEFT,RIGHT,DOWN,UP = range(4)

class GridItemType:
    NONE = 0
    ROAD = 1
    GROUND = 2
    SEMAPH_GREEN = 3
    SEMAPH_RED = 4
    TARGET = 5