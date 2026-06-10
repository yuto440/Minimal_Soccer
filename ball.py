import pygame
import constants as c

class Ball:
    def __init__(self, pos):
        self.pos = pos
        self.velocity = pygame.math.Vector2(100, 100)

    def update(self, dt):
        self.pos += self.velocity * dt
        
    def draw(self, screen):
        pygame.draw.circle(screen, c.WHITE, (self.pos.x, self.pos.y), c.BALL_SIZE)