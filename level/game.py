from functools import partial

import pygame.constants
from pygame import Surface
from pygame.event import Event
from pygame.time import set_timer

from command import Command
from command.tetronimo import move_tetronimo, rotate_tetronimo
from layer import BackgroundLayer, HUDLayer, Layer, MeshBlockLayer, TetronimoLayer
from objects import Tetronimo
from objects.events import GAME_EXIT_EVENT, GAME_RESTART_EVENT, TETRONIMO_DOWN_EVENT
from objects.mesh_block import (
    add_tetronimo_to_mesh_block,
    new_mesh_block,
    remove_completed_lines,
)
from objects.tetronimo import (
    get_random_tetronimo,
    tetronimo_bottom_hit_mesh_block,
    tetronimo_hit_bottom,
    tetronimo_hit_top,
)

from .level import Level, LevelManager
from .menu.game_over import GameOverMenu

ACCELERATED_TETRONIMO_DOWN_INTERVAL = 25
DEFAULT_TETRONIMO_DOWN_INTERVAL = 500
FIELD_SIZE = (10, 20)
SPAWN_POS = (4, 0)


def set_tetro_down_timer(interval: int) -> None:
    set_timer(TETRONIMO_DOWN_EVENT, interval)


def calculate_score(completed_lines: int) -> int:
    if completed_lines == 1:
        return 40
    elif completed_lines == 2:
        return 100
    elif completed_lines == 3:
        return 300
    elif completed_lines == 4:
        return 1200
    return 0


class GameLevel(Level):
    def __init__(self, game: LevelManager):
        super().__init__(game)

        # constants

        # variables
        self.actual_tetronimo: Tetronimo = get_random_tetronimo(SPAWN_POS)
        self.next_tetronimo: Tetronimo = get_random_tetronimo(SPAWN_POS)
        self.mesh_block = new_mesh_block(*FIELD_SIZE)
        self.score = 0
        self.stop_update = False

        # events
        set_tetro_down_timer(DEFAULT_TETRONIMO_DOWN_INTERVAL)

        # layers
        self.layers: list[Layer] = [
            BackgroundLayer(),
            MeshBlockLayer(self, FIELD_SIZE),
            TetronimoLayer(self),
            HUDLayer(self),
        ]

        # commands
        self.commands: list[Command] = []

        # menus
        self.menus = {
            "game_over": GameOverMenu(self),
        }

    def handle_event(self, event: Event) -> None:
        if event.type == TETRONIMO_DOWN_EVENT:
            self.commands.append(
                partial(
                    move_tetronimo,
                    FIELD_SIZE,
                    self.mesh_block,
                    self.actual_tetronimo,
                    (0, 1),
                )
            )
        elif event.type == GAME_RESTART_EVENT:
            self.game.transition_to("game")
        elif event.type == GAME_EXIT_EVENT:
            self.game.transition_to("main_menu")
        elif event.type == pygame.constants.KEYDOWN:
            if (
                event.key == pygame.constants.K_LEFT
                or event.key == pygame.constants.K_a
            ):
                self.commands.append(
                    partial(
                        move_tetronimo,
                        FIELD_SIZE,
                        self.mesh_block,
                        self.actual_tetronimo,
                        (-1, 0),
                    )
                )
            elif (
                event.key == pygame.constants.K_RIGHT
                or event.key == pygame.constants.K_d
            ):
                self.commands.append(
                    partial(
                        move_tetronimo,
                        FIELD_SIZE,
                        self.mesh_block,
                        self.actual_tetronimo,
                        (1, 0),
                    )
                )
            elif (
                event.key == pygame.constants.K_UP
                or event.key == pygame.constants.K_SPACE
            ):
                self.commands.append(
                    partial(
                        rotate_tetronimo,
                        FIELD_SIZE,
                        self.mesh_block,
                        self.actual_tetronimo,
                    )
                )
                pass
            elif (
                event.key == pygame.constants.K_DOWN
                or event.key == pygame.constants.K_s
            ):
                self.commands.append(
                    partial(set_tetro_down_timer, ACCELERATED_TETRONIMO_DOWN_INTERVAL)
                )
        elif event.type == pygame.constants.KEYUP:
            if (
                event.key == pygame.constants.K_DOWN
                or event.key == pygame.constants.K_s
            ):
                self.commands.append(
                    partial(set_tetro_down_timer, DEFAULT_TETRONIMO_DOWN_INTERVAL)
                )

        for menu in self.menus.values():
            menu.handle_event(event)

    def _should_add_tetronimo_to_mesh_block(self) -> bool:
        return tetronimo_hit_bottom(
            FIELD_SIZE, self.actual_tetronimo
        ) or tetronimo_bottom_hit_mesh_block(self.mesh_block, self.actual_tetronimo)

    def update(self, dt: float) -> None:
        for menu in self.menus.values():
            menu.update(dt)

        if self.stop_update:
            return

        if self._should_add_tetronimo_to_mesh_block():
            if tetronimo_hit_top(self.actual_tetronimo):
                self.commands.clear()
                self.stop_update = True
                self.menus["game_over"].active = True
                return

            add_tetronimo_to_mesh_block(self.mesh_block, self.actual_tetronimo)
            completed_lines = remove_completed_lines(self.mesh_block)
            self.score += calculate_score(completed_lines)

            self.actual_tetronimo = self.next_tetronimo
            self.next_tetronimo = get_random_tetronimo(SPAWN_POS)

        for command in self.commands:
            command()
        self.commands.clear()

    def render(self, screen: Surface) -> None:
        for layer in self.layers:
            layer.render(screen)

        for menu in self.menus.values():
            menu.render(screen)
