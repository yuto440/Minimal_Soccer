import pygame
import constants as c

class Player:
    def __init__(self, pos):
        self.pos = pos

    def draw(self, screen):
        pygame.draw.circle(screen, c.RED, (self.pos.x, self.pos.y), c.PLAYER_SIZE)