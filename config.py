SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

DEBUG = False

NUM_BOIDS = 20
MAX_SPEED = 3
DRAW_COLLISION = False
DRAW_VISION = False
VISION_RANGE = 80
COLLISION_RANGE = 30

FORCE_PRIORITY_LIST = (
    'boundary', 'avoidance', 'velocity_matching', 'center_mass',
)

V_WEIGHT = 0.4
CM_WEIGHT = 0.3
AV_WEIGHT = 0.6
B_WEIGHT = 0.7

MOVE_GRANULARITY = 40


def debug_print(*args):
    if DEBUG:
        string = ''
        for item in args:
            string += ' ' + str(item)
        print string
