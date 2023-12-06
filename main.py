import sys

import pygame

from settings import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Py-Tetris")

        self.screen = pygame.display.set_mode(WINDOW_RESOLUTION)
        self.clock = pygame.time.Clock()

    def _update(self):
        self.clock.tick(FPS)

    def _draw(self):
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._draw()


if __name__ == "__main__":
    game = Game()
    game.run()
