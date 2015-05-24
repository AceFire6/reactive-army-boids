SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

SELECTED_ENTITY = None

DEBUG = False

MAX_SPEED = 2
DRAW_COLLISION = False
DRAW_VISION = False
VISION_RANGE = 150
COLLISION_RANGE = 30

WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 100, 200)
GREEN = (0, 100, 0)

FORCE_PRIORITY_LIST = (
    'avoidance', 'formation',
)

AV_WEIGHT = 0.5
B_WEIGHT = 0.6
F_WEIGHT = 0.6

FORMATION = True
BOUNDARY = True
AVOID = True

MOVE_GRANULARITY = 40


def debug_print(*args):
    if DEBUG:
        string = ''
        for item in args:
            string += ' ' + str(item)
        print string
