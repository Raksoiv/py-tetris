import sys
import pygame
from level import Level, MainMenuLevel
from settings import FPS, WINDOW_RESOLUTION


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Py-Tetris")

        # Constants
        self.fps = FPS

        # Variables
        self.screen = pygame.display.set_mode(WINDOW_RESOLUTION)
        self.clock = pygame.time.Clock()

        self.transition_to(MainMenuLevel(self))

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self._level.handle_event(event)

    def _update(self, delta_time: float) -> None:
        self._level.update(delta_time)

    def _render(self) -> None:
        self._level.render(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            delta_time = self.clock.tick(self.fps) / 1000.0
            self._handle_events()
            self._update(delta_time)
            self._render()

    def transition_to(self, level: Level) -> None:
        self._level = level


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
