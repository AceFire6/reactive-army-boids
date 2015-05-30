from vec2d import Vec2d
from boid import Boid
from waypoint import Waypoint


class Formation(object):
    def __init__(self, filename=None):
        self.waypoint = None
        self._center = Vec2d(0, 0)
        self._direction = Vec2d(0, 0)
        self.positions = []
        self.waypoints = []
        if filename:
            self.parse_formation_file(filename)

    def parse_formation_file(self, open_file):
        if open_file:
            self._center = Vec2d(eval(open_file.readline()))
            self._direction = Vec2d(eval(open_file.readline()))
            for line in open_file.readlines()[0:]:
                self.positions.append(Vec2d(eval(line)))
                self.waypoints.append(Waypoint(Vec2d(eval(line)), self.center))

    def set_waypoint(self, waypoint_pair_or_x, y=None):
        if y is None:
            self.waypoint = Vec2d(waypoint_pair_or_x)
        else:
            self.waypoint = Vec2d(waypoint_pair_or_x, y)

    def set_center(self, center_pair_or_x, y=None):
        if y is None:
            self.waypoint = center_pair_or_x
        else:
            self.waypoint = Vec2d(center_pair_or_x, y)

    def gen_and_get_boids(self):
        return [Boid(start_pos=(position + self.center), waypoint=waypoint)
                for position, waypoint in zip(self.positions, self.waypoints)]

    @property
    def center(self):
        return Vec2d(int(self._center[0]), int(self._center[1]))

    @property
    def direction(self):
        return self._direction + self._center

    @property
    def facing(self):
        return self.direction - self._center

    def update(self):
        if self.waypoint and (self._center.get_distance(self.waypoint) > 10):
            acceleration = self.facing.normalized()
            to_waypoint = self.waypoint - self._center
            rotation = self.facing.get_angle_between(to_waypoint) / 60
            self._direction.rotate(rotation)
            self._center += acceleration
            for waypoint in self.waypoints:
                waypoint.rotate(rotation)
                waypoint.update_position(self.center)
