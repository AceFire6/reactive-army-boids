import unittest
from unit import Unit
from vec2d import Vec2d


class TestUnit(unittest.TestCase):
    def test___init__(self):
        unit = Unit(Vec2d(0, 0), Vec2d(0, 0), None)
        self.assertIsNotNone(unit)

    def test_contains(self):
        unit = Unit(Vec2d(0, 0), Vec2d(0, 0), None)
        self.assertTrue(unit.contains(Vec2d(5, 0)))

    def test_get_center(self):
        unit = Unit(Vec2d(0, 0), Vec2d(0, 0), None)
        self.assertListEqual([0, 0], unit.get_center())

    def test_get_inverse_square(self):
        unit = Unit(Vec2d(0, 0), Vec2d(0, 0), None)
        other_unit = Unit(Vec2d(10, 0), Vec2d(10, 0), None)
        self.assertEqual(1.0 / 100, unit.get_inverse_square(other_unit))

if __name__ == '__main__':
    unittest.main()
