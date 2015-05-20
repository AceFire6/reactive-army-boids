from vec2d import Vec2d

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

SELECTED_ENTITY = None

DEBUG = False

NUM_BOIDS = 20
MAX_SPEED = 3
DRAW_COLLISION = False
DRAW_VISION = False
VISION_RANGE = 150
COLLISION_RANGE = 30

WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 200, 200)

FORCE_PRIORITY_LIST = (
    'formation', 'boundary', 'avoidance', 'velocity_matching', 'center_mass',
)

V_WEIGHT = 0.4
CM_WEIGHT = 0.3
AV_WEIGHT = 0.5
B_WEIGHT = 0.6
F_WEIGHT = 0.9

FORMATION = True
BOUNDARY = True
AVOID = True
VELOCITY = True
CENTER_MASS = True

MOVE_GRANULARITY = 40
F_RADIUS = 100
F_CENTER = Vec2d(300, 300)


def debug_print(*args):
    if DEBUG:
        string = ''
        for item in args:
            string += ' ' + str(item)
        print string
