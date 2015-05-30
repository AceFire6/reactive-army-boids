SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

DEBUG = False

MAX_SPEED = 2
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
F_WEIGHT = 0.6


def debug_print(*args):
    if DEBUG:
        string = ''
        for item in args:
            string += ' ' + str(item)
        print string
