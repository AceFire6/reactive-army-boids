from formation_designer import add_tuple
import unittest
from formation_designer import distance_to
from formation_designer import close_to
from formation_designer import get_closest
from formation_designer import get_closest_and_dist


class TestAddTuple(unittest.TestCase):
    def test_add_tuple_returns_tuple_for_t1_equal_tuple_and_t2_equal_tuple(self):
        self.assertEqual((3, 5), add_tuple((1, 2), (2, 3)))


class TestDistanceTo(unittest.TestCase):
    def test_distance_to_returns_111803398875_for_point1_equal_tuple_and_point2_equal_tuple(self):
        self.assertEqual(111.80339887498948, distance_to((100, 50), (0, 0)))

    def test_distance_to_returns_111803398875_for_point1_equal_tuple_and_point2_equal_tuple_case_2(self):
        self.assertEqual(111.80339887498948, distance_to((200, 50), (100, 100)))

    def test_distance_to_returns_1500_for_point1_equal_tuple_and_point2_equal_tuple(self):
        self.assertEqual(150.0, distance_to((200, 50), (50, 50)))

    def test_distance_to_returns_206155281281_for_point1_equal_tuple_and_point2_equal_tuple(self):
        self.assertEqual(206.15528128088303, distance_to((200, 50), (0, 0)))

    def test_distance_to_returns_20_for_point1_equal_tuple_and_point2_equal_tuple(self):
        self.assertEqual(2.0, distance_to((0, 0), (2, 0)))

    def test_distance_to_returns_269258240357_for_point1_equal_tuple_and_point2_equal_tuple(self):
        self.assertEqual(269.2582403567252, distance_to((200, 50), (300, 300)))

    def test_distance_to_returns_320156211872_for_point1_equal_tuple_and_point2_equal_tuple(self):
        self.assertEqual(320.1562118716424, distance_to((100, 50), (300, 300)))

    def test_distance_to_returns_500_for_point1_equal_tuple_and_point2_equal_tuple(self):
        self.assertEqual(50.0, distance_to((100, 50), (100, 100)))

    def test_distance_to_returns_500_for_point1_equal_tuple_and_point2_equal_tuple_case_2(self):
        self.assertEqual(50.0, distance_to((100, 50), (50, 50)))


class TestCloseTo(unittest.TestCase):
    def test_close_to_returns_list_for_placed_units_equal_list_and_point_equal_tuple(self):
        self.assertEqual([], close_to((200, 50), [(0, 0), (100, 100), (50, 50), (300, 300)]))


class TestGetClosest(unittest.TestCase):
    def test_get_closest_returns_tuple_for_close_units_equal_list_and_point_equal_tuple(self):
        obj = (100, 100)
        self.assertEqual(obj, get_closest((100, 50), [(0, 0), obj, (50, 50), (300, 300)]))


class TestGetClosestAndDist(unittest.TestCase):
    def test_get_closest_and_dist_returns_tuple_for_close_units_equal_list_and_point_equal_tuple(self):
        obj = (100, 100)
        self.assertEqual((obj, 50.0), get_closest_and_dist((100, 50), [(0, 0), obj, (50, 50), (300, 300)]))

if __name__ == '__main__':
    unittest.main()
