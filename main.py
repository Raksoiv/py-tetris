import sys
from typing import List

import pygame

from command import Command, MovePieceCommand, RotatePieceCommand
from game_state import GameState
from layer import ActivePieceLayer, BackgroundLayer, Layer

#
# Setting
#

SCREEN_WIDTH = 630
SCREEN_HEIGHT = 900

TILE_SIZE = 30
CUBE_SIZE = 28

WORLD_WIDTH = SCREEN_WIDTH // TILE_SIZE
WORLD_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

#
# Code
#

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Tetris")

        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.epoch = 0
        self.running = True

        self.game_state = GameState(TILE_SIZE, CUBE_SIZE)

        self.commands: List[Command] = []
        self.layers: List[Layer] = [
            BackgroundLayer(self.game_state),
            ActivePieceLayer(self.game_state),
        ]

    def _process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.commands.append(RotatePieceCommand(self.game_state.active_piece))

        if (
            self.game_state.active_piece
            and self.epoch % self.game_state.epochs_to_move == 0
        ):
            self.commands.append(
                MovePieceCommand(
                    self.game_state.active_piece,
                    pygame.Vector2(0, 1),
                ),
            )

        # If there is no active piece, create one
        if not self.game_state.active_piece:
            self.game_state.create_piece()

    def _update(self) -> None:
        for command in self.commands:
            command.run()
        self.commands.clear()

        self.epoch += 1

    def _render(self) -> None:
        for layer in self.layers:
            layer.render(self.window)

        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self._process_input()
            self._update()
            self._render()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
