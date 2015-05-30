from boid import Boid
from vec2d import Vec2d


class Enemy(object, Boid):
    def __init__(self, start, end):
        Boid.__init__(self, start, None, None)
        self._start = Vec2d(start.x, start.y)
        self._end = end
        self._target = end

    def apply_velocity(self, **kwargs):
        if self.position.get_distance(self._target) < 30:
            if self._target == self._start:
                self._target = self._end
            else:
                self._target = self._start

        direction = (self._target - self.position).normalized()
        self.velocity = direction * 2
        self.position += self.velocity
        self.generate_vertices()

    def update(self, **kwargs):
        self.apply_velocity()
