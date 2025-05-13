import pygame
from constants import *
from circleshape import CircleShape
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from scoring import ScoreManager
from gameover import GameOverScreen

def reset_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable, shots)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    field = AsteroidField()

    return updatable, drawable, asteroids, shots, player, field

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    dt = 0

    score_mgr = ScoreManager(font_name="Consolas", font_size=32)
    pause_font = pygame.font.SysFont("Arial", 72, bold=True)
    game_over_screen = GameOverScreen(screen)

    running = True
    while running:
        state = "playing"
        updatable, drawable, asteroids, shots, player, field = reset_game()

        while state != "game_over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    state = "game_over"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    state = "paused" if state == "playing" else "playing"

            if state == "playing":
                updatable.update(dt)

                for asteroid in asteroids:
                    if player.collides_with(asteroid):
                        player.kill()
                        play_again = game_over_screen.show(score_mgr.current, score_mgr.high_score)
                        if play_again:
                            state = "game_over"
                        else:
                            running = False
                            state = "game_over"
                        break

                for asteroid in asteroids:
                    for shot in shots:
                        if asteroid.collides_with(shot):
                            if asteroid.radius <= ASTEROID_MIN_RADIUS:
                                score_mgr.add_points(30)
                            else:
                                score_mgr.add_points(10)
                            asteroid.split()
                            shot.kill()

            screen.fill((0, 0, 0))
            for sprite in drawable:
                sprite.draw(screen)

            if state == "paused":
                text = pause_font.render("PAUSED", True, (255,255,255))
                rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                screen.blit(text, rect)

            score_mgr.render(screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()
