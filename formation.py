from vec2d import Vec2d
from unit import Unit
from waypoint import Waypoint


class Formation(object):
    """Formation that handles all units it manages. Used to handle unit
    placement and waypoint updating.
    """
    def __init__(self, file=None):
        """Create a formation. If a filename is specified, the formation
        is loaded from there, otherwise, the file has to be specified later.
        """
        self.waypoint = None
        self._center = Vec2d(0, 0)
        self._direction = Vec2d(0, 0)
        self.positions = []
        self.waypoints = []
        if file:
            self.parse_formation_file(file)

    def parse_formation_file(self, open_file):
        """Open and parse the given formation file. Set up all the required
        variables for movement and units and their waypoints.
        """
        if open_file:
            self._center = Vec2d(eval(open_file.readline()))
            self._direction = Vec2d(eval(open_file.readline()))
            for line in open_file.readlines()[0:]:
                self.positions.append(Vec2d(eval(line)))
                self.waypoints.append(Waypoint(Vec2d(eval(line)), self.center))

    def set_waypoint(self, waypoint_pair_or_x, y=None):
        """Set the formations waypoint. Either using a tuple, or by specifying
        the x and y coordinates as separate arguments.
        """
        if y is None:
            self.waypoint = Vec2d(waypoint_pair_or_x)
        else:
            self.waypoint = Vec2d(waypoint_pair_or_x, y)

    def set_center(self, center_pair_or_x, y=None):
        """Set the center of the formation.Either using a tuple, or by
        specifying the x and y coordinates as separate arguments.
        """
        if y is None:
            self._center = center_pair_or_x
        else:
            self._center = Vec2d(center_pair_or_x, y)

    def gen_and_get_boids(self):
        """Generate all the units in the formation based on their relative
        positions and the formation center. Give them a waypoint managed by
        the formation. Return a list.
        """
        return [Unit((position + self.center), waypoint, self)
                for position, waypoint in zip(self.positions, self.waypoints)]

    @property
    def center(self):
        """Return a Vec2D with the center for drawing purposes."""
        return Vec2d(int(self._center[0]), int(self._center[1]))

    @property
    def direction(self):
        """Get the direction. _direction is its location relative to the
         formation's center. Return Vec2D.
         """
        return self._direction + self._center

    @property
    def facing(self):
        """Return the Vec2D vector describing the facing of the formation."""
        return self.direction - self._center

    def update(self):
        """Update the formation. If the center of the formation is too far
        from its waypoint, movement is started. The formation always moves
        toward direction, however, it rotates to face the waypoint. This allows
        for a more realistic looking movement/rotation.
        """
        if self.waypoint and (self._center.get_distance(self.waypoint) > 10):
            acceleration = self.facing.normalized()
            to_waypoint = self.waypoint - self._center
            rotation = self.facing.get_angle_between(to_waypoint) / 60
            self._direction.rotate(rotation)
            self._center += acceleration
            for waypoint in self.waypoints:
                waypoint.rotate(rotation)
                waypoint.update_position(self.center)
