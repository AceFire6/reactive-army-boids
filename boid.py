import config
from vec2d import Vec2d


class Boid:
    def __init__(self, start_pos, waypoint, formation):
        self.position = start_pos
        self._formation = formation
        self.facing = None
        self.waypoint = waypoint
        self.angle = 0
        self.velocity = Vec2d(0, 0)
        self.vertices = [Vec2d(0, 0), Vec2d(0, 0), Vec2d(0, 0)]
        self.generate_vertices()
        self.colour = config.WHITE

    def contains(self, mouse_pos):
        return self.position.get_distance(mouse_pos) < 10

    def get_center(self):
        return [int(self.position.x), int(self.position.y)]

    def generate_vertices(self):
        operations = (Vec2d(0, 10), Vec2d(5, -5), Vec2d(-5, -5))
        new_vertices = []
        for vertex, operation in zip(self.vertices, operations):
            if self.velocity != Vec2d(0, 0) and not self.facing:
                self.angle += (self.velocity.get_angle() - 90
                               - self.angle) / 10
            elif self.facing:
                self.angle += (self.facing.get_angle() - 90 - self.angle) / 40
            elif self.velocity == Vec2d(0, 0) and self._formation:
                self.angle += (self._formation.facing.get_angle() - 90
                               - self.angle) / 40
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
        dist = config.COLLISION_RANGE * 5
        closest_enemy = None
        for near_obstacle in near_obstacles:
            temp = self.position.get_distance(near_obstacle.position)
            if temp < dist:
                closest_enemy = near_obstacle
                dist = temp
        if closest_enemy:
            self.facing = closest_enemy.position - self.position
            self.generate_vertices()
            self.colour = config.RED
        else:
            self.facing = None

    def update(self, boids, obstacles=list()):
        dist = config.COLLISION_RANGE * 5
        obstacles = [ob for ob in obstacles
                     if ob.position.get_distance(self.position) < dist]

        if self.colour == config.RED:
            self.colour = config.WHITE
        if not obstacles:
            self.facing = None
            self.apply_velocity(boids)
        else:
            self.face_nearest_enemy(obstacles)

    def apply_velocity(self, boids, obstacles=list()):
        self.velocity = Vec2d(0, 0)
        formation = (self.stay_in_formation() * config.F_WEIGHT).normalized()
        avoidance = (self.avoid_neighbours(boids)).normalized()

        acceleration = self.accumulate(
            formation=formation, avoidance=avoidance)

        config.debug_print('ACCELERATION:', acceleration)

        self.velocity += acceleration
        self.velocity = self.velocity.normalized() * config.MAX_SPEED
        self.position += self.velocity
        self.generate_vertices()

    def stay_in_formation(self):
        acceleration = Vec2d(0, 0)

        dist = self.waypoint.get_position() - self.position

        if dist.get_length() > 2:
            inv_dist = 1.0 / self.position.get_dist_sqrd(
                self.waypoint.get_position())
            acceleration = dist.normalized() * (10 * inv_dist)

        return acceleration

    def get_neighbours(self, boids, distance):
        neighbours = []
        for boid in boids:
            if boid != self:
                if self.position.get_distance(boid.position) <= distance:
                    neighbours.append(boid)
        return neighbours

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
