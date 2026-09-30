import unittest

from game.target import Target


class CollisionTests(unittest.TestCase):
    def test_late_click_outside_visible_circle_is_miss(self):
        target = Target(100, 100)
        target.age = 80
        self.assertEqual(target.drawn_radius(), 15)
        self.assertFalse(target.contains_point(130, 100))

    def test_hit_boundary_matches_integer_drawing_radius(self):
        target = Target(100, 100)
        for age in (0, 30, 60, 89):
            target.age = age
            radius = target.drawn_radius()
            self.assertTrue(target.contains_point(100 + radius, 100))
            self.assertFalse(target.contains_point(100 + radius + 0.1, 100))

    def test_expired_target_cannot_be_hit(self):
        target = Target(100, 100)
        target.age = target.lifespan_frames
        self.assertFalse(target.contains_point(100, 100))
