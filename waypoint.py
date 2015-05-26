class Waypoint(object):
    def __init__(self, relative_pos, center):
        self.relative_pos = relative_pos
        self.center = center

    def get_position(self):
        return self.relative_pos + self.center

    def update_position(self, new_center):
        self.center = new_center

    def rotate(self, rotation):
        self.relative_pos.rotate(rotation)
