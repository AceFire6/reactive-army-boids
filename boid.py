import config
import random
from vec2d import Vec2d


class Boid:
    def __init__(self):
        self.position = Vec2d(0, 0)
        self._generate_and_set_position()
        self.velocity = Vec2d(0, 0)
        self._generate_and_set_velocity()
        self.vertices = [Vec2d(0, 0), Vec2d(0, 0), Vec2d(0, 0)]
        self.generate_vertices()

        self.colour = (0, 0, 0)
        self._generate_and_set_colour()

    def get_center(self):
        return [int(self.position.x), int(self.position.y)]

    def _generate_and_set_colour(self):
        self.colour = (random.randint(40, 255),
                       random.randint(40, 255),
                       random.randint(40, 255))
        config.debug_print('COLOUR', self.colour)

    def _generate_and_set_position(self):
        self.position.x = random.randint(1, config.SCREEN_WIDTH)
        self.position.y = random.randint(1, config.SCREEN_HEIGHT)
        config.debug_print('POSITION', self.position)

    def _generate_and_set_velocity(self):
        self.velocity.x = random.random() * config.MAX_SPEED
        self.velocity.x *= (-1 if random.randint(0, 1) == 1 else 1)
        self.velocity.y = random.random() * config.MAX_SPEED
        self.velocity.y *= (-1 if random.randint(0, 1) == 1 else 1)
        config.debug_print('VELOCITY', self.velocity)

    def generate_vertices(self):
        operations = (Vec2d(0, 10), Vec2d(5, -5), Vec2d(-5, -5))
        new_vertices = []
        for vertex, operation in zip(self.vertices, operations):
            operation.rotate(self.velocity.get_angle() - 90)
            vertex = self.position + operation
            new_vertices.append(vertex)

        self.vertices = new_vertices

    def accumulate(self, **kwforces):
        accumulator = 0
        acceleration = Vec2d(0, 0)
        for key in config.FORCE_PRIORITY_LIST:
            config.debug_print(key)
            force = kwforces.get(key)
            config.debug_print(force)
            if force:
                config.debug_print('ACCUM:', accumulator)
                if accumulator < 0.8:
                    accumulator += force.get_length()
                    config.debug_print(force.get_length())
                    acceleration += force
        return acceleration

    def apply_velocity(self, boids):
        center_mass = (
            self.move_to_center(boids) * config.CM_WEIGHT).normalized()
        velocity_matching = (
            self.match_velocity(boids) * config.V_WEIGHT).normalized()
        avoidance = (
            self.avoid_neighbours(boids) * config.AV_WEIGHT).normalized()

        acceleration = self.accumulate(
            center_mass=center_mass,
            velocity_matching=velocity_matching,
            avoidance=avoidance,
        )

        config.debug_print('ACCELERATION:', acceleration)

        self.velocity += acceleration
        self.velocity = self.velocity.normalized() * config.MAX_SPEED
        self.position += self.velocity

        if self.position.x > config.SCREEN_WIDTH:
            self.position.x = 1
        elif self.position.x < 0:
            self.position.x = config.SCREEN_WIDTH

        if self.position.y > config.SCREEN_HEIGHT:
            self.position.y = 1
        elif self.position.y < 0:
            self.position.y = config.SCREEN_HEIGHT

        self.generate_vertices()

    def get_neighbours(self, boids, distance):
        neighbours = []
        for boid in boids:
            if boid != self:
                if self.position.get_distance(boid.position) <= distance:
                    neighbours.append(boid)
        return neighbours

    def move_to_center(self, boids):
        acceleration = Vec2d(0, 0)
        neighbours = self.get_neighbours(boids, config.VISION_RANGE)

        if not neighbours:
            return acceleration

        for boid in neighbours:
            acceleration += boid.position

        acceleration /= len(neighbours)
        return (acceleration - self.position) / config.MOVE_GRANULARITY

    def match_velocity(self, boids):
        acceleration = Vec2d(0, 0)
        neighbours = self.get_neighbours(boids, config.VISION_RANGE)

        if not neighbours:
            return acceleration

        for boid in neighbours:
            acceleration += boid.velocity

        return acceleration / (len(neighbours) * config.MOVE_GRANULARITY)

    def avoid_neighbours(self, boids):
        acceleration = Vec2d(0, 0)
        neighbours = self.get_neighbours(boids, config.COLLISION_RANGE)

        if not neighbours:
            return acceleration

        for boid in neighbours:
            acceleration += (boid.position - self.position)

        return -1 * (acceleration / len(neighbours))
