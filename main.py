import pygame
from constants import *
from circleshape import CircleShape
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from scoring import ScoreManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Game")

    clock = pygame.time.Clock()
    dt = 0
    score_mgr = ScoreManager(font_name="Consolas", font_size=32)
    state = "playing"
    pause_font = pygame.font.SysFont("Arial", 72, bold=True)


    # Create groups BEFORE instantiating player
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set as containers for Player
    Player.containers = (updatable, drawable, shots)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)

    # Now create the Player (so it adds itself to the groups)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if state == "playing":
                    state = "paused"
                else:
                    state = "playing"

        if state == "playing":
            # Update all update-able sprites
            updatable.update(dt)

            # Check for collisions after update step
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    print("Game over!")
                    pygame.quit()
                    return
            

            # Check for bullet-asteroid collisions
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        # Check size before splitting
                        if asteroid.radius <= ASTEROID_MIN_RADIUS:
                            score_mgr.add_points(30)
                        else:
                            score_mgr.add_points(10)
                        asteroid.split()
                        shot.kill()

        # Draw all drawable sprites
        screen.fill((0, 0, 0))
        for sprite in drawable:
            sprite.draw(screen)

        if state == "paused":
            text = pause_font.render("PAUSED", True, (255,255,255))
            rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text, rect)

        score_mgr.render(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Delta time in seconds

if __name__ == "__main__":
    main()
