from functools import partial
from typing import Callable

import pygame.event
import pygame.mouse
from pygame import Surface
from pygame.font import Font

from objects.ui import UIButton, uibutton_factory

from .game import Game
from .level import Level, LevelManager

BOREL_FONT_PATH = "assets/fonts/Borel-Regular.ttf"
ROBOTO_FONT_PATH = "assets/fonts/RobotoCondensed-Regular.ttf"

Command = Callable[[], None]


def button_hover(button: UIButton) -> Command:
    def _button_hover() -> None:
        button.set_hover_active()

    return _button_hover


def button_normal(button: UIButton) -> Command:
    def _button_normal() -> None:
        button.set_normal_active()

    return _button_normal


def button_play(level_manager: LevelManager) -> Command:
    def _button_play() -> None:
        level_manager.transition_to(Game(level_manager))

    return _button_play


def button_settings() -> Command:
    def _button_settings() -> None:
        print("Settings")

    return _button_settings


def button_exit() -> Command:
    def _button_exit() -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    return _button_exit


class MainMenuLevel(Level):
    def __init__(self, game):
        super().__init__(game)

        # constants
        self.background_color = (51, 51, 51)
        self.font_color = (204, 204, 204)
        self.title_font = Font(BOREL_FONT_PATH, 64)
        self.body_font = Font(ROBOTO_FONT_PATH, 32)
        self._create_buttons()

        # variables
        self.commands: list[Command] = []

    def _create_buttons(self) -> None:
        factory = partial(
            uibutton_factory, self.body_font, self.font_color, self.background_color
        )
        self.buttons = {
            "play": factory("Play"),
            "settings": factory("Settings"),
            "exit": factory("Exit"),
        }

    def _render_title(self, screen: Surface) -> None:
        title_surface = self.title_font.render("Py-Tetris", True, self.font_color)
        screen_size = screen.get_size()
        title_pos = (screen_size[0] - title_surface.get_width()) // 2, screen_size[
            1
        ] * 0.1
        screen.blit(title_surface, title_pos)

    def _render_buttons(self, screen: Surface) -> None:
        for i, button in enumerate(self.buttons.values()):
            button_pos = (
                (screen.get_width() - button.active.get_width()) // 2,
                int(screen.get_height() * (0.25 + (i + 1) * 0.15)),
            )
            button.pos = button_pos
            screen.blit(button.active, button_pos)

    def handle_event(self, event: pygame.event.Event) -> None:
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            if button.collidepoint(mouse_pos):
                self.commands.append(button_hover(button))
            else:
                self.commands.append(button_normal(button))

        if event.type == pygame.MOUSEBUTTONUP:
            if self.buttons["play"].collidepoint(mouse_pos):
                self.commands.append(button_play(self.game))
            elif self.buttons["settings"].collidepoint(mouse_pos):
                self.commands.append(button_settings())
            elif self.buttons["exit"].collidepoint(mouse_pos):
                self.commands.append(button_exit())

    def update(self, delta_time: float) -> None:
        for command in self.commands:
            command()
        self.commands.clear()

    def render(self, screen: Surface) -> None:
        screen.fill(self.background_color)
        self._render_title(screen)
        self._render_buttons(screen)
