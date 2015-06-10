from waypoint import Waypoint
from vec2d import Vec2d
import unittest


class TestWaypoint(unittest.TestCase):
    def test_create_waypoint(self):
        waypoint = Waypoint(Vec2d(0, 0), Vec2d(100, 100))
        self.assertIsNotNone(waypoint)

    def test_get_position(self):
        waypoint = Waypoint(Vec2d(0, 0), Vec2d(100, 100))
        self.assertEqual(Vec2d(100, 100), waypoint.get_position())

    def test_update_position(self):
        waypoint = Waypoint(Vec2d(0, 0), Vec2d(100, 100))
        waypoint.update_position(Vec2d(50, 50))
        self.assertEqual(Vec2d(50, 50), waypoint.get_position())

    def test_rotate(self):
        waypoint = Waypoint(Vec2d(10, 0), Vec2d(100, 0))
        waypoint.rotate(90)
        self.assertEqual(Vec2d(100, 10), waypoint.get_position())

if __name__ == '__main__':
    unittest.main()
