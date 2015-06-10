import config
from vec2d import Vec2d


class Unit:
    """Unit class. Its waypoint is handled by its formation."""
    def __init__(self, start_pos, waypoint, formation):
        """Create a unit with start_pos and a waypoint controlled by formation
        Initially the unit's velocity is 0. Its vertices are generated based
        on its facing and its colour is set to white.
        """
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
        """Determine if the mouse_pos is on this unit. Return boolean."""
        return self.position.get_distance(mouse_pos) < 10

    def get_center(self):
        """Return the center of the unit as a list. For drawing purposes."""
        return [int(self.position.x), int(self.position.y)]

    def generate_vertices(self):
        """Generate and set the unit's vertices."""
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
        """Tally the forces applied to the unit and clamp them if they breach
        the specified maximum force magnitude. This is to prioritise the most
        important forces. Return a Vec2D containing the acceleration based on
        the forces.
        """
        accumulator = 0
        acceleration = Vec2d(0, 0)
        for key in config.FORCE_PRIORITY_LIST:
            force = kwforces.get(key)
            if force:
                if accumulator < 0.8:
                    accumulator += force.get_length()
                    acceleration += force
        return acceleration

    def face_nearest_enemy(self, near_obstacles):
        """Make the unit face the nearest enemy if there are any enemies within
        the unit's range.
        """
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

    def update(self, units, obstacles=list()):
        """Update the unit's state and velocity."""
        dist = config.COLLISION_RANGE * 5
        obstacles = [ob for ob in obstacles
                     if ob.position.get_distance(self.position) < dist]

        if self.colour == config.RED:
            self.colour = config.WHITE
        if not obstacles:
            self.facing = None
            self.apply_velocity(units)
        else:
            self.face_nearest_enemy(obstacles)

    def apply_velocity(self, units, obstacles=list()):
        """Calculate and apply velocity to the unit based on the formation
        and avoidance rules.
        """
        self.velocity = Vec2d(0, 0)
        formation = (self.stay_in_formation() * config.F_WEIGHT).normalized()
        avoidance = (self.avoid_neighbours(units)).normalized()

        acceleration = self.accumulate(
            formation=formation, avoidance=avoidance)

        self.velocity += acceleration
        self.velocity = self.velocity.normalized() * config.MAX_SPEED
        self.position += self.velocity
        self.generate_vertices()

    def stay_in_formation(self):
        """Calculates the acceleration needed to head towards the unit's
        waypoint and returns a Vec2D with the acceleration normalized and
        multiplied by 10 and the inverse of the distance squared. This makes
        the unit decelerate as it approaches its waypoint.
        """
        acceleration = Vec2d(0, 0)

        dist = self.waypoint.get_position() - self.position

        if dist.get_length() > 2:
            inv_dist = 1.0 / self.position.get_dist_sqrd(
                self.waypoint.get_position())
            acceleration = dist.normalized() * (10 * inv_dist)

        return acceleration

    def get_neighbours(self, units, distance):
        """Find the units within distance of this unit. Return a list."""
        neighbours = []
        for unit in units:
            if unit != self:
                if self.position.get_distance(unit.position) <= distance:
                    neighbours.append(unit)
        return neighbours

    def avoid_obstacles(self, obstacles):
        """The avoidance rule. Calculates the acceleration needed to avoid the
        given obstacles. Return a Vec2D with the acceleration.
        """
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

    def avoid_neighbours(self, units):
        """Collision avoidance rule. Calculates the acceleration needed to
        avoid collisions with other units.
        Return a Vec2D with the acceleration.
        """
        acceleration = Vec2d(0, 0)
        neighbours = self.get_neighbours(units, config.COLLISION_RANGE)

        if not neighbours:
            return acceleration

        for unit in neighbours:
            distance_mult = self.get_inverse_square(unit)
            acceleration += (unit.position - self.position) * distance_mult

        return -1 * (acceleration / len(neighbours))

    def get_inverse_square(self, other_unit):
        """Calculate the inverse distance square between this unit and
        other_unit. Return a float.
        """
        return 1.0 / self.position.get_dist_sqrd(other_unit.position)
