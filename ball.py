import pygame
import constants as c

class Ball:
    def __init__(self, pos):
        self.pos = pos
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self, dt):
        self.apply_friction(dt)
        self.pos += self.velocity * dt

    def apply_friction(self, dt):
        speed = self.velocity.length()

        if speed == 0:
            return
        
        deceleration = c.BALL_FRICTION_ACCEL * dt

        if speed < deceleration:
            self.velocity = pygame.math.Vector2(0, 0)
        else:
            self.velocity = self.velocity.normalize() * (speed - deceleration)
        
    def draw(self, screen):
        pygame.draw.circle(screen, c.WHITE, (self.pos.x, self.pos.y), c.BALL_RADIUS)