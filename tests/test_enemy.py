import unittest
from enemy import Enemy
from vec2d import Vec2d


class TestEnemy(unittest.TestCase):
    def test___init__(self):
        enemy = Enemy(Vec2d(0, 0), Vec2d(200, 200))
        self.assertIsNotNone(enemy)

    def test_update_and_apply_velocity(self):
        enemy = Enemy(Vec2d(0, 0), Vec2d(200, 200))
        enemy_pos = Vec2d(enemy.position.x, enemy.position.y)
        enemy.update()
        self.assertNotEquals(enemy_pos, enemy.position)

if __name__ == '__main__':
    unittest.main()
