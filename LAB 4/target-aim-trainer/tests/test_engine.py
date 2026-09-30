import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import pygame

from game.game_engine import GameEngine


class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.engine = GameEngine(700, 500)

    def test_round_end_freezes_results_and_draws_screen(self):
        engine = self.engine
        engine.hits, engine.misses, engine.score = 3, 1, 3
        engine.time_left_frames = 1
        engine.update()
        self.assertTrue(engine.game_over)
        self.assertEqual(engine.accuracy(), 75.0)
        engine.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(engine.target.x, engine.target.y)))
        engine.update()
        self.assertEqual((engine.hits, engine.misses, engine.score), (3, 1, 3))
        screen = pygame.Surface((700, 500))
        engine.render(screen)
        self.assertEqual(tuple(screen.get_at((0, 0)))[:3], (24, 27, 36))

    def test_timeout_counts_as_one_miss_and_respawns(self):
        engine = self.engine
        previous = engine.target
        engine.target.age = engine.target.lifespan_frames - 1
        engine.update()
        self.assertEqual(engine.misses, 1)
        self.assertIsNot(engine.target, previous)
        engine.update()
        self.assertEqual(engine.misses, 1)

    def test_escape_requests_exit(self):
        self.engine.game_over = True
        self.engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
        self.assertTrue(self.engine.quit_requested)

    def test_right_click_does_not_change_statistics(self):
        self.engine.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=3, pos=(0, 0)))
        self.assertEqual((self.engine.hits, self.engine.misses), (0, 0))
