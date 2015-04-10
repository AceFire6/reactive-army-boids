import config
from vec2d import Vec2d
from boid import Boid

test_boid = Boid()
vertices = test_boid.vertices
velocity = test_boid.velocity
position = test_boid.position


def test_boid_uniqueness():
    boid2 = Boid()

    assert test_boid != boid2


def test_boid_generated_values():
    # Colour
    assert len(test_boid.colour) == 3
    assert type(test_boid.colour) == tuple
    for i in test_boid.colour:
        assert type(i) == int

    # Position
    assert type(position) == Vec2d
    assert 1 <= position.x <= config.SCREEN_WIDTH
    assert 1 <= position.y <= config.SCREEN_HEIGHT

    # Velocity
    assert type(velocity) == Vec2d
    assert -config.MAX_SPEED <= velocity.x <= config.MAX_SPEED
    assert -config.MAX_SPEED <= velocity.y <= config.MAX_SPEED

    # Vertices
    operations = (Vec2d(0, 10), Vec2d(5, -5), Vec2d(-5, -5))
    assert type(vertices) == list
    for vertex in vertices:
        assert type(vertex) == Vec2d
    direction_angle = velocity.get_angle() - 90
    assert vertices[0] == position + operations[0].rotated(direction_angle)
    assert vertices[1] == position + operations[1].rotated(direction_angle)
    assert vertices[2] == position + operations[2].rotated(direction_angle)


def test_boid_get_center():
    assert test_boid.get_center() == Vec2d(int(position.x), int(position.y))
    
def test_accumulator():
    assert 1 == 1

