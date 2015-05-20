from vec2d import Vec2d


class Formation(object):
    def __init__(self, center=None):
        self.waypoint = Vec2d(0, 0)
        self.center = center or Vec2d(0, 0)

    def set_waypoint(self, waypoint_vec_or_x, y=None):
        if y is None:
            self.waypoint = waypoint_vec_or_x
        else:
            self.waypoint = Vec2d(waypoint_vec_or_x, y)

    def set_center(self, center_vec_or_x, y=None):
        if y is None:
            self.waypoint = center_vec_or_x
        else:
            self.waypoint = Vec2d(center_vec_or_x, y)
