import pygame
import constants as c

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.velocity = pygame.math.Vector2(0, 0)

        self.color = c.BLACK

        self.knockback_timer = 0

    def think(self, ball_pos: pygame.math.Vector2):
        if self.knockback_timer > 0:
            return

        to_ball = ball_pos - self.pos

        if to_ball.length() > 0:
            self.velocity = to_ball.normalize() * c.PLAYER_SPEED

    def trigger_knockback(self, n_player_to_ball: pygame.math.Vector2):
        self.knockback_timer = 0.5#0.5秒間ノックバック
        self.velocity = -n_player_to_ball * c.PLAYER_SPEED

    def update(self, dt):
        if self.knockback_timer > 0:
            self.knockback_timer -= dt

        self.pos += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), c.PLAYER_RADIUS)