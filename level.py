from __future__ import annotations
from command import Command, MoveCommand, RotateCommand
from game_state import GameState
from layer import Layer, MeshBlockLayer, TetronimoLayer
from typing import List, Tuple

import pygame
import sys


class Game:
    def __init__(self, window_resolution: Tuple[int, int], field_size: Tuple[int, int],
                 tile_size: int, tile_margin: int, initial_tetronimo_down_interval: int, fps: int):
        pygame.init()
        pygame.display.set_caption("Py-Tetris")

        self.screen = pygame.display.set_mode(window_resolution)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.pause = False

        self.transition_to(
            BaseLevel(self, field_size, tile_size, tile_margin, initial_tetronimo_down_interval))

    def transition_to(self, level: Level):
        self._level = level

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause

            self._level.handle_event(event)

    def _update(self):
        self._level.update()

    def _render(self):
        self._level.render()

    def run(self):
        while True:
            self._handle_events()
            if not self.pause:
                self._update()
                self._render()
            self.clock.tick(self.fps)


class Level:
    @property
    def game(self) -> Game:
        return self._game

    @game.setter
    def game(self, value: Game):
        self._game = value

    def handle_event(self, event: pygame.event.Event) -> None:
        raise NotImplementedError()

    def update(self) -> None:
        raise NotImplementedError()

    def render(self) -> None:
        raise NotImplementedError()


class BaseLevel(Level):
    def __init__(
            self, game: Game, field_size: Tuple[int, int], tile_size: int, tile_margin: int,
            initial_tetronimo_down_interval: int,
        ):
        self.game = game

        self._timers(initial_tetronimo_down_interval)

        self.game_state = GameState(field_size, tile_size, tile_margin)
        self.layers: List[Layer] = [
            MeshBlockLayer(self.game_state),
            TetronimoLayer(self.game_state)
        ]
        self.commands: List[Command] = []

    def _timers(self, initial_tetronimo_down_interval):
        # Tetronimo down timer
        self.tetronimo_down_event = pygame.USEREVENT + 0
        self.tetronimo_down_trigger = False
        pygame.time.set_timer(self.tetronimo_down_event, initial_tetronimo_down_interval)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.commands.append(
                    MoveCommand(self.game_state, self.game_state.tetronimo, pygame.Vector2(-1, 0)))
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.commands.append(
                    MoveCommand(self.game_state, self.game_state.tetronimo, pygame.Vector2(1, 0)))
            elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                self.commands.append(
                    RotateCommand(self.game_state, self.game_state.tetronimo))

        elif event.type == self.tetronimo_down_event:
            self.tetronimo_down_trigger = True

    def update(self):
        if self.tetronimo_down_trigger:
            self.commands.append(
                MoveCommand(self.game_state, self.game_state.tetronimo, pygame.Vector2(0, 1)),
            )
            self.tetronimo_down_trigger = False

        for command in self.commands:
            command.run()
        self.commands.clear()

    def render(self):
        for layer in self.layers:
            layer.render(self.game.screen)

        pygame.display.flip()
