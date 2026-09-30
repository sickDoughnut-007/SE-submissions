import os
import unittest
from unittest.mock import patch, Mock
import wave

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import pygame
from game.sound import SoundFeedback


class SoundTests(unittest.TestCase):
    def test_generated_audio_is_a_valid_nonempty_wav(self):
        with wave.open(SoundFeedback._wav(((880, 0.07),)), "rb") as stream:
            self.assertEqual(stream.getframerate(), 44100)
            self.assertEqual(stream.getnchannels(), 1)
            self.assertGreater(stream.getnframes(), 0)

    def test_missing_audio_device_does_not_crash(self):
        with patch("pygame.mixer.get_init", return_value=None), patch("pygame.mixer.init", side_effect=pygame.error("no device")):
            sound = SoundFeedback()
        self.assertFalse(sound.available)
        sound.play("hit")
        sound.toggle_mute()

    def test_mute_blocks_playback_and_stops_existing_effects(self):
        with patch("pygame.mixer.get_init", return_value=(44100, -16, 2)), patch("pygame.mixer.Sound", side_effect=lambda **kwargs: Mock()):
            sound = SoundFeedback()
        sound.play("hit")
        sound.effects["hit"].play.assert_called_once()
        sound.toggle_mute()
        for effect in sound.effects.values():
            effect.stop.assert_called_once()
        sound.play("hit")
        sound.effects["hit"].play.assert_called_once()
        sound.toggle_mute()
        sound.play("hit")
        self.assertEqual(sound.effects["hit"].play.call_count, 2)
