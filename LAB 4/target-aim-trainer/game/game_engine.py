import pygame
import random
from .target import Target
from .sound import SoundFeedback

# Game Engine

WHITE = (255, 255, 255)
RED = (220, 60, 60)
DIFFICULTIES = {
    "Easy": {"base_radius": 50, "min_radius": 16, "lifespan_frames": 150},
    "Medium": {"base_radius": 40, "min_radius": 12, "lifespan_frames": 90},
    "Hard": {"base_radius": 26, "min_radius": 8, "lifespan_frames": 45},
}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.margin = 60
        self.hud_height = 60
        self.round_seconds = 30
        self.font = pygame.font.SysFont("Arial", 26)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.quit_requested = False
        self.sound = SoundFeedback()
        self.replay_buttons = {
            name: pygame.Rect(self.width // 2 - 225 + index * 155, 330, 140, 50)
            for index, name in enumerate(DIFFICULTIES)
        }
        self.start_round("Medium")

    def start_round(self, difficulty):
        if difficulty not in DIFFICULTIES:
            raise ValueError(f"Unknown difficulty: {difficulty}")
        self.difficulty = difficulty
        self.time_left_frames = self.round_seconds * 60
        self.hits = self.misses = self.score = 0
        self.game_over = False
        self.target = self._spawn_target()

    def _spawn_target(self):
        radius = DIFFICULTIES[self.difficulty]["base_radius"]
        x = random.randint(self.margin, self.width - self.margin)
        y = random.randint(self.margin + self.hud_height, self.height - max(self.margin, radius + 40))
        return Target(x, y, **DIFFICULTIES[self.difficulty])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.sound.toggle_mute()
            return
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
            self.quit_requested = True
            return
        if self.game_over:
            shortcuts = {pygame.K_1: "Easy", pygame.K_2: "Medium", pygame.K_3: "Hard"}
            if event.type == pygame.KEYDOWN and event.key in shortcuts:
                self.start_round(shortcuts[event.key])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, rect in self.replay_buttons.items():
                    if rect.collidepoint(event.pos):
                        self.start_round(name)
                        break
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        x, y = pos
        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            self.sound.play("hit")
            self.target = self._spawn_target()
        else:
            self.misses += 1
            self.sound.play("miss")

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1
        if self.time_left_frames <= 0:
            self.game_over = True
            self.sound.play("end")
            return

        self.target.update()
        if self.target.expired():
            self.misses += 1  # letting a target time out counts as a miss too
            self.sound.play("miss")
            self.target = self._spawn_target()

    def accuracy(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return round(100 * self.hits / total, 1)

    def render(self, screen):
        if self.game_over:
            self._render_game_over(screen)
            return
        r = self.target.drawn_radius()
        pygame.draw.circle(screen, RED, (self.target.x, self.target.y), r)
        pygame.draw.circle(screen, WHITE, (self.target.x, self.target.y), r, 2)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        seconds_left = max(0, self.time_left_frames // 60)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, WHITE)
        screen.blit(timer_text, (self.width - 140, 10))

        acc_text = self.font.render(f"Accuracy: {self.accuracy()}%", True, WHITE)
        screen.blit(acc_text, (self.width // 2 - 90, 10))
        self._center_text(screen, f"{self.difficulty} | {self.sound.status()} (M) | Q / Esc: quit", self.height - 22)

    def _center_text(self, screen, text, y, font=None, color=WHITE):
        label = (font or self.font).render(text, True, color)
        screen.blit(label, label.get_rect(center=(self.width // 2, y)))

    def _render_game_over(self, screen):
        screen.fill((24, 27, 36))
        self._center_text(screen, "ROUND COMPLETE", 100, self.title_font)
        self._center_text(screen, f"Final score: {self.score}", 190)
        self._center_text(screen, f"Accuracy: {self.accuracy():.1f}%", 235)
        self._center_text(screen, f"Hits: {self.hits}    Misses: {self.misses}", 280)
        for name, rect in self.replay_buttons.items():
            pygame.draw.rect(screen, (44, 94, 130), rect, border_radius=8)
            label = self.font.render(name, True, WHITE)
            screen.blit(label, label.get_rect(center=rect.center))
        self._center_text(screen, "Replay: click a difficulty or press 1 / 2 / 3", 410)
        self._center_text(screen, f"Q / Esc: exit | {self.sound.status()} (M)", 450)
