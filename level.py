from __future__ import annotations
from typing import List
import sys

import pygame

from command import Command, MoveCommand, RotateCommand
from game_state import GameState
from layer import Layer, MeshBlockLayer, TetronimoLayer, UILayer
import settings


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Py-Tetris")

        self.screen = pygame.display.set_mode(settings.WINDOW_RESOLUTION)
        self.clock = pygame.time.Clock()
        self.fps = settings.FPS
        self.pause = False

        # self.transition_to(
        #     BaseLevel(self, field_size, tile_size, tile_margin, initial_tetronimo_down_interval))
        self.transition_to(MainMenu(self))

    def transition_to(self, level: Level):
        self._level = level

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause

            self._level.handle_event(event)

    def _update(self):
        self._level.update()

    def _render(self):
        self._level.render()
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self._handle_events()
            if not self.pause:
                self._update()
                self._render()
            self.clock.tick(self.fps)


class Level:
    def __init__(self, game: Game):
        self.game = game

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
    def __init__(self, game: Game):
        super().__init__(game)

        # Colors
        ui_background_color = (102, 102, 112)
        ui_text_color = (238, 255, 255)
        field_background_color = (51, 51, 58)

        self._init_timers()

        self.game_state = GameState(
            settings.FIELD_SIZE,
            settings.TILE_SIZE,
            settings.TILE_MARGIN,
        )

        ui_resolution = (
            settings.WINDOW_RESOLUTION[0] - settings.FIELD_RESOLUTION[0],
            settings.WINDOW_RESOLUTION[1],
        )
        ui_x_margin = settings.FIELD_RESOLUTION[0]
        self.layers: List[Layer] = [
            UILayer(
                self.game_state,
                ui_resolution,
                ui_x_margin,
                ui_background_color,
                settings.ROBOTO_FONT_PATH,
                ui_text_color,
                settings.ROBOTO_MONO_FONT_PATH,
                ui_text_color,
            ),
            MeshBlockLayer(self.game_state, field_background_color, settings.FIELD_RESOLUTION),
            TetronimoLayer(self.game_state)
        ]

        self.commands: List[Command] = []

    def _init_timers(self):
        # Tetronimo down timer
        self._tetromino_down_timer(settings.DEFAULT_TETRONIMO_DOWN_INTERVAL)

    def _tetromino_down_timer(self, tetronimo_down_interval):
        self.tetronimo_down_event = pygame.USEREVENT + 0
        self.tetronimo_down_trigger = False
        pygame.time.set_timer(self.tetronimo_down_event, tetronimo_down_interval)

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
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self._tetromino_down_timer(settings.ACCELERATED_TETRONIMO_DOWN_INTERVAL)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self._tetromino_down_timer(settings.DEFAULT_TETRONIMO_DOWN_INTERVAL)

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


class MainMenu(Level):
    def __init__(self, game: Game):
        super().__init__(game)

        self.window_resolution = settings.WINDOW_RESOLUTION
        self.title_font = pygame.font.Font(settings.BOREL_FONT_PATH, 64)
        self.body_font = pygame.font.Font(settings.ROBOTO_FONT_PATH, 32)
        self.primary_color = (204, 204, 204)
        self.secondary_color = (51, 51, 51)
        self._create_options()

        self.fonr_surface: pygame.Surface = pygame.Surface((0, 0))

    def _create_options(self):
        self.options = [
            {
                "text": "Play",
                "action": lambda: self.game.transition_to(BaseLevel(self.game)),
                "hover": False,
            },
            {
                "text": "Settings",
                "action": lambda: print("Settings"),
                "hover": False,
            },
            {
                "text": "Exit",
                "action": lambda: self.game.quit(),
                "hover": False,
            },
        ]

        for i, option in enumerate(self.options):
            option["surface"] = self.body_font.render(option["text"], True, self.primary_color)
            option["pos"] = (
                (self.window_resolution[0] - option["surface"].get_width()) // 2,
                self.window_resolution[1] * (.25 + (i + 1) * .15),
            )
            option["border_box"] = pygame.Rect(
                option["pos"][0] - 48,
                option["pos"][1] - 10,
                option["surface"].get_width() + 96,
                option["surface"].get_height() + 20,
            )

    def handle_event(self, event: pygame.event.Event) -> None:
        mouse_pos = pygame.mouse.get_pos()
        for option in self.options:
            if option["border_box"].collidepoint(mouse_pos):
                option["hover"] = True
            else:
                option["hover"] = False

        if event.type == pygame.MOUSEBUTTONUP:
            for option in self.options:
                if option["hover"]:
                    option["action"]()

    def update(self):
        pass

    def render(self):
        self.game.screen.fill(self.secondary_color)

        # Title
        title_surface = self.title_font.render("Py-Tetris", True, self.primary_color)
        title_pos = (self.window_resolution[0] - title_surface.get_width()) // 2, self.window_resolution[1] * .1
        self.game.screen.blit(title_surface, title_pos)

        # Options
        for option in self.options:
            # Text
            self.game.screen.blit(option["surface"], option["pos"])
            # Border box
            if option["hover"]:
                pygame.draw.rect(self.game.screen, self.primary_color, option["border_box"], 5)
