import unittest
from vec2d import Vec2d
from formation import Formation


class TestFormation(unittest.TestCase):
    def test___init__(self):
        formation = Formation(open('test_formation.fm'))
        self.assertIsNotNone(formation)

    def test_center(self):
        formation = Formation(open('test_formation.fm'))
        self.assertEqual(Vec2d(291, 214), formation.center)

    def test_direction(self):
        formation = Formation(open('test_formation.fm'))
        self.assertEqual(Vec2d(290, 305), formation.direction)

    def test_facing(self):
        formation = Formation(open('test_formation.fm'))
        self.assertEqual(Vec2d(-1, 91), formation.facing)

    def test_gen_and_get_boids(self):
        formation = Formation(open('test_formation.fm'))
        self.assertEqual(6, len(formation.gen_and_get_boids()))

    def test_set_center(self):
        formation = Formation(open('test_formation.fm'))
        old_center = formation.center
        formation.set_center(300, 300)
        self.assertEqual(Vec2d(300, 300), formation.center)
        self.assertNotEqual(old_center, formation.center)

    def test_set_waypoint(self):
        formation = Formation(open('test_formation.fm'))
        formation.set_waypoint(500, 500)
        self.assertEqual(Vec2d(500, 500), formation.waypoint)

if __name__ == '__main__':
    unittest.main()
