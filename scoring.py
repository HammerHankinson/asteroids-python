import os
import pygame
from constants import HS_FILE, NEON_GREEN, NEON_YELLOW

class ScoreManager:
    HS_FILE       = "highscore.txt"
    NEON_GREEN    = ( 57, 255,  20)
    NEON_YELLOW   = (255, 255,   0)

    def __init__(self, font_name="Arial", font_size=36, file_path=None):
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)
        self.file_path = file_path or self.HS_FILE
        self.high_score = self._load()
        self.current   = 0

    def _load(self):
        try:
            with open(self.file_path, "r") as f:
                return int(f.read().strip())
        except (IOError, ValueError):
            return 0

    def _save(self):
        with open(self.file_path, "w") as f:
            f.write(str(self.high_score))

    def add_points(self, pts):
        self.current += pts
        if self.current > self.high_score:
            self.high_score = self.current
            self._save()

    def reset(self):
        self.current = 0

    def render(self, screen):
        score_surf = self.font.render(f"Score: {self.current}", True, self.NEON_GREEN)
        hs_surf    = self.font.render(f"High Score: {self.high_score}", True, self.NEON_YELLOW)
        screen.blit(score_surf, (10, 10))
        screen.blit(hs_surf,    (10, 50))
