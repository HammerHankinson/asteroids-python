import pygame

class GameOverScreen:
    def __init__(self, screen, font_path=None):
        self.screen = screen
        self.font_path = font_path
        self.title_font = pygame.font.Font(font_path, 64)
        self.message_font = pygame.font.Font(font_path, 32)
        self.running = True

    def show(self, score, high_score):
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill((0, 0, 0))

            title_surface = self.title_font.render("GAME OVER", True, (255, 0, 0))
            message_surface = self.message_font.render("Press Enter to Play Again", True, (255, 255, 255))
            score_surface = self.message_font.render(f"Score: {score}  High Score: {high_score}", True, (255, 255, 255))

            self.screen.blit(title_surface, self._center_text(title_surface, y_offset=-80))
            self.screen.blit(score_surface, self._center_text(score_surface, y_offset=0))
            self.screen.blit(message_surface, self._center_text(message_surface, y_offset=80))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
            clock.tick(60)

    def _center_text(self, surface, y_offset=0):
        rect = surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + y_offset))
        return rect