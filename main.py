import sys

import pygame

from level import GameLevel, Level, MainMenuLevel

FPS = 60
WINDOW_RESOLUTION = (600, 800)


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Py-Tetris")

        # Constants
        self.fps = FPS
        self.levels: dict[str, type[Level]] = {
            "game": GameLevel,
            "main_menu": MainMenuLevel,
        }

        # Variables
        self.screen = pygame.display.set_mode(WINDOW_RESOLUTION)
        self.clock = pygame.time.Clock()

        self.transition_to("main_menu")

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

    def transition_to(self, level: str) -> None:
        self._level = self.levels[level](self)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
