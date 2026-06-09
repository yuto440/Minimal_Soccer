import pygame
import sys
import constants as c
from ball import Ball
from player import Player

class GameController:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("Minimal Soccer")

        self.ball = Ball(c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2)#ボールの生成
        
        self.player = Player(c.SCREEN_WIDTH // 4, c.SCREEN_HEIGHT // 2)

    def display(self):
        self.screen.fill(c.GRASS_COLOR)
        pygame.draw.circle(self.screen, c.WHITE, (self.ball.x, self.ball.y), c.BALL_SIZE)#ボールの表示
        pygame.draw.circle(self.screen, c.RED, (self.player.x, self.player.y), c.PLAYER_SIZE)#プレイヤーの表示
        pygame.display.update()

    def play_game(self):
        self.display()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gm = GameController()
    gm.play_game()