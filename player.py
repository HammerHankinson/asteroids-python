import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Decrease timer
        if self.timer > 0:
            self.timer -= dt
            if self.timer < 0:
                self.timer = 0  # clamp to zero

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer > 0:
            return  # Don't shoot if still in cooldown
        
        # Compute the direction the player is facing
        direction = pygame.Vector2(0, 1).rotate(self.rotation)

        # Scale direction vector to shooting speed
        velocity = direction * PLAYER_SHOOT_SPEED

        self.timer = PLAYER_SHOOT_COOLDOWN

        # Create a new Shot at the player's position with this velocity
        shot = Shot(self.position.x, self.position.y, velocity)

        if hasattr(self, "containers"):
            for group in self.containers:
                group.add(shot)
