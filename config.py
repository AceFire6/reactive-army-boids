SCREEN_WIDTH = 600  # The width of the formation designer and simulation
SCREEN_HEIGHT = 600  # The height of the formation designer and simulation

MAX_SPEED = 2  # Max speed of a unit
VISION_RANGE = 150  # The vision range of a unit
COLLISION_RANGE = 20  # The collision range of a unit

# Colour definitions for easy referencing
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 100, 200)
GREEN = (0, 100, 0)

# The priority and order the forces are applied in.
FORCE_PRIORITY_LIST = (
    'avoidance', 'formation',
)

AV_WEIGHT = 0.5  # The weighting of avoidance behaviours
F_WEIGHT = 0.6  # The weighting of the formation behaviour
