import pygame
import sys

class GameController:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        
        self.screen_size = (1000, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Minimal Soccer")

    def display(self):
        
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