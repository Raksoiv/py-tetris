import sys

import pygame

from game_state import GameState
from layer import TetronimoLayer
from command import MoveCommand
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Py-Tetris")

        self.screen = pygame.display.set_mode(WINDOW_RESOLUTION)
        self.clock = pygame.time.Clock()

        self._timers()

        self.game_state = GameState(FIELD_SIZE, TILE_SIZE, TILE_MARGIN)
        self.layers = [
            TetronimoLayer(self.game_state)
        ]
        self.commands = []

    def _timers(self):
        # Tetronimo down timer
        self.tetronimo_down_event = pygame.USEREVENT + 0
        self.tetronimo_down_trigger = False
        pygame.time.set_timer(self.tetronimo_down_event, INITIAL_TETRONIMO_DOWN_INTERVAL)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == self.tetronimo_down_event:
                self.tetronimo_down_trigger = True

    def _update(self):
        if self.tetronimo_down_trigger:
            self.commands.append(
                MoveCommand(self.game_state, self.game_state.tetronimo, pygame.Vector2(0, 1)),
            )
            self.tetronimo_down_trigger = False

        for command in self.commands:
            command.run()
        self.commands.clear()

    def _render(self):
        self.screen.fill((36, 36, 36))

        for layer in self.layers:
            layer.render(self.screen)

        pygame.display.flip()

    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
