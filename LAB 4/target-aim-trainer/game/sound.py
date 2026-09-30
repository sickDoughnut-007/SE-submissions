"""Small generated WAV effects; no external audio files are required."""

from array import array
from io import BytesIO
import math
import sys
import wave

import pygame


class SoundFeedback:
    def __init__(self):
        self.available = False
        self.muted = False
        self.effects = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=1)
            for name, notes in {
                "hit": ((880, 0.07), (1320, 0.07)),
                "miss": ((220, 0.12), (165, 0.10)),
                "end": ((523, 0.13), (659, 0.13), (784, 0.20)),
            }.items():
                self.effects[name] = pygame.mixer.Sound(file=self._wav(notes))
            self.available = True
        except pygame.error:
            # The rest of the game remains playable without an audio device.
            self.effects.clear()

    @staticmethod
    def _wav(notes):
        rate = 44100
        samples = array("h")
        for frequency, duration in notes:
            count = int(rate * duration)
            for i in range(count):
                fade = min(1.0, i / 220, (count - 1 - i) / 440)
                samples.append(int(7000 * fade * math.sin(2 * math.pi * frequency * i / rate)))
        if sys.byteorder != "little":
            samples.byteswap()
        stream = BytesIO()
        with wave.open(stream, "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(rate)
            output.writeframes(samples.tobytes())
        stream.seek(0)
        return stream

    def play(self, effect):
        if self.available and not self.muted:
            self.effects[effect].play()

    def toggle_mute(self):
        self.muted = not self.muted
        if self.available and self.muted:
            for effect in self.effects.values():
                effect.stop()

    def status(self):
        if not self.available:
            return "No audio device"
        return "Muted" if self.muted else "Sound on"
