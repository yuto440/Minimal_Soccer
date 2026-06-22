import pygame
import constants as c
from typing import Any

class Player:
    def __init__(self, pos: pygame.math.Vector2) -> None:
        self.pos: pygame.math.Vector2 = pos
        self.initial_pos: pygame.math.Vector2 = pygame.math.Vector2(pos)

        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(0, 0)

        self.color: tuple[int, int, int] = c.BLACK

        self.knockback_timer: float = 0.0

    def reset(self) -> None:
        self.pos = pygame.math.Vector2(self.initial_pos)
        self.velocity = pygame.math.Vector2(0, 0)

    def think(self, ball_pos: pygame.math.Vector2) -> None:
        if self.knockback_timer > 0.0:
            return

        to_ball = ball_pos - self.pos

        if to_ball.length_squared() > 0:
            self.velocity = to_ball.normalize() * c.PLAYER_SPEED

    def trigger_knockback(self, n_player_to_ball: pygame.math.Vector2) -> None:
        self.knockback_timer = 0.5  # 0.5秒間ノックバック
        self.velocity = -n_player_to_ball * c.PLAYER_SPEED

    def update(self, dt: float) -> None:
        if self.knockback_timer > 0.0:
            self.knockback_timer = max(0.0, self.knockback_timer - dt)

        self.pos += self.velocity * dt

    def draw(self, screen: Any) -> None:
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), c.PLAYER_RADIUS)