from boid import Boid
from vec2d import Vec2d
import config


class Enemy(object, Boid):
    def __init__(self, velocity):
        Boid.__init__(self)
        self.velocity = Vec2d(velocity)

    def apply_velocity(self, boids, **kwargs):
        if (self.position.x > config.SCREEN_WIDTH) or (self.position.x < 0):
            self.velocity = -self.velocity

        self.position += self.velocity
        self.generate_vertices()
