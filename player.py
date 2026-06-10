import pygame
import constants as c

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.velocity = pygame.math.Vector2(0, 0)

    def think(self, ball_pos: pygame.math.Vector2):
        to_ball = ball_pos - self.pos

        if to_ball.length() > 0:
            self.velocity = to_ball.normalize() * c.PLAYER_SPEED

    def update(self, dt):
        self.pos += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, c.RED, (self.pos.x, self.pos.y), c.PLAYER_SIZE)