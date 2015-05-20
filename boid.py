import config
import random
import pygame
from vec2d import Vec2d


class Boid:
    def __init__(self):
        self.position = Vec2d(0, 0)
        self.angle = 0
        self._generate_and_set_position()
        self.velocity = Vec2d(0, 0)
        # self._generate_and_set_velocity()
        self.vertices = [Vec2d(0, 0), Vec2d(0, 0), Vec2d(0, 0)]
        self.generate_vertices()
        self.colour = config.WHITE
        self.selected = False
        # self._generate_and_set_colour()

    def contains(self, mouse_pos):
        return self.position.get_distance(mouse_pos) < 10

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
            if self.velocity != Vec2d(0, 0):
                self.angle = self.velocity.get_angle() - 90
            operation.rotate(self.angle)
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

    def face_nearest_enemy(self, near_obstacles):
        dist = config.VISION_RANGE
        closest_enemy = 0
        for near_obstacle in near_obstacles:
            temp = self.position.get_distance(near_obstacle.position)
            if temp < dist:
                closest_enemy = near_obstacle
                dist = temp
        self.angle = self.position.get_angle_between(closest_enemy.position)
        self.generate_vertices()
        self.colour = config.RED

    def update(self, boids, obstacles=list()):
        if self.colour == config.RED:
            self.colour = config.WHITE
        if self.selected:
            self.colour = config.CYAN
        if not obstacles:
            self.apply_velocity(boids)
        else:
            near_obstacles = [ob for ob in obstacles
                              if config.VISION_RANGE >
                              self.position.get_distance(ob.position)
                              > config.COLLISION_RANGE * 2]
            if not near_obstacles:
                self.apply_velocity(boids, obstacles)
            else:
                self.face_nearest_enemy(near_obstacles)

    def apply_velocity(self, boids, obstacles=list()):
        self.velocity = Vec2d(0, 0)
        # formation = (self.stay_in_formation() * config.F_WEIGHT).normalized()
        boundary = (self.avoid_boundary() * config.B_WEIGHT).normalized()
        # center_mass = (
        #     self.move_to_center(boids) * config.CM_WEIGHT).normalized()
        # velocity_matching = (
        #     self.match_velocity(boids) * config.V_WEIGHT).normalized()
        avoidance = (
            (self.avoid_neighbours(boids) +
             self.avoid_obstacles(obstacles)) * config.AV_WEIGHT).normalized()

        zero = Vec2d(0, 0)
        acceleration = self.accumulate(
            # formation=formation if config.FORMATION else zero,
            boundary=boundary if config.BOUNDARY else zero,
            # center_mass=center_mass if config.CENTER_MASS else zero,
            # velocity_matching=velocity_matching if config.VELOCITY else zero,
            avoidance=avoidance if config.AVOID else zero,
        )

        config.debug_print('ACCELERATION:', acceleration)

        self.velocity += acceleration
        self.velocity = self.velocity.normalized() * config.MAX_SPEED
        self.position += self.velocity
        self.generate_vertices()

    def stay_in_formation(self):
        acceleration = Vec2d(0, 0)

        dist = self.position - config.F_CENTER

        if dist.get_length() > config.F_RADIUS:
            acceleration = -(dist.normalized() * 10)

        return acceleration

    def get_neighbours(self, boids, distance):
        neighbours = []
        for boid in boids:
            if boid != self:
                if self.position.get_distance(boid.position) <= distance:
                    neighbours.append(boid)
        return neighbours

    def avoid_boundary(self):
        rebound = 20
        acceleration = Vec2d(0, 0)

        if self.position.x > config.SCREEN_WIDTH + 40:
            acceleration += Vec2d(-rebound, 0)
        elif self.position.x < -40:
            acceleration += Vec2d(rebound, 0)

        if self.position.y > config.SCREEN_HEIGHT + 40:
            acceleration += Vec2d(0, -rebound)
        elif self.position.y < -40:
            acceleration += Vec2d(0, rebound)

        return acceleration

    def avoid_obstacles(self, obstacles):
        acceleration = Vec2d(0, 0)
        near_obstacles = \
            [ob for ob in obstacles
             if self.position.get_distance(ob.position)
             < config.COLLISION_RANGE * 2]

        if not near_obstacles:
            return acceleration

        for obstacle in near_obstacles:
            distance_mult = self.get_inverse_square(obstacle)
            acceleration += (obstacle.position - self.position) * distance_mult

        return -(acceleration / float(len(list(near_obstacles))))

    def move_to_center(self, boids):
        acceleration = Vec2d(0, 0)
        neighbours = self.get_neighbours(boids, config.VISION_RANGE)

        if not neighbours:
            return acceleration

        for boid in neighbours:
            distance_mult = self.get_inverse_square(boid)
            acceleration += boid.position * distance_mult

        acceleration /= len(neighbours)
        return (acceleration - self.position) / float(config.MOVE_GRANULARITY)

    def match_velocity(self, boids):
        acceleration = Vec2d(0, 0)
        neighbours = self.get_neighbours(boids, config.VISION_RANGE)

        if not neighbours:
            return acceleration

        for boid in neighbours:
            distance_mult = self.get_inverse_square(boid)
            acceleration += boid.velocity * distance_mult

        return acceleration / float(len(neighbours) * config.MOVE_GRANULARITY)

    def avoid_neighbours(self, boids):
        acceleration = Vec2d(0, 0)
        neighbours = self.get_neighbours(boids, config.COLLISION_RANGE)

        if not neighbours:
            return acceleration

        for boid in neighbours:
            distance_mult = self.get_inverse_square(boid)
            acceleration += (boid.position - self.position) * distance_mult

        return -1 * (acceleration / len(neighbours))

    def get_inverse_square(self, other_boid):
        return 1.0 / self.position.get_dist_sqrd(other_boid.position)

    def select(self):
        self.selected = not self.selected
        if self.selected:
            self.colour = config.CYAN
        else:
            self.colour = config.WHITE
