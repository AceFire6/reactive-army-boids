import config
from vec2d import Vec2d
from boid import Boid

test_boid = Boid()
vertices = test_boid.vertices
velocity = test_boid.velocity
position = test_boid.position

near_boid = Boid()
near_boid.position = test_boid.position + Vec2d(30, 0)

far_boid = Boid()
far_boid.position = test_boid.position + Vec2d(100, 0)

boids = [test_boid, near_boid, far_boid]


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


def test_accumulate():
    kwargs = dict(
        avoidance=Vec2d(0.4, 0.4),
        velocity_matching=Vec2d(0.3, 0.3),
        center_mass=Vec2d(0.4, 0.4),
    )
    accel = test_boid.accumulate(**kwargs)
    assert accel == Vec2d(0.7, 0.7)


def test_get_neighbours():
    boid2 = Boid()
    boid2.position = test_boid.position + Vec2d(3, 3)

    neighbours = test_boid.get_neighbours([boid2, ], 3)
    assert type(neighbours) == list
    assert len(neighbours) == 0

    neighbours = test_boid.get_neighbours([boid2], 5)
    assert len(neighbours) == 1
    assert neighbours[0] == boid2


def test_move_to_center():
    acceleration = test_boid.move_to_center([])
    assert acceleration == Vec2d(0, 0)

    acceleration = test_boid.move_to_center(boids)
    assert acceleration == ((near_boid.position - test_boid.position) /
                            config.MOVE_GRANULARITY)


def test_match_velocity():
    acceleration = test_boid.match_velocity([])
    assert acceleration == Vec2d(0, 0)

    acceleration = test_boid.match_velocity(boids)
    assert acceleration == near_boid.velocity / config.MOVE_GRANULARITY


def test_avoid_neighbours():
    acceleration = test_boid.avoid_neighbours([])
    assert acceleration == Vec2d(0, 0)

    acceleration = test_boid.avoid_neighbours(boids)
    assert acceleration == test_boid.position - near_boid.position
