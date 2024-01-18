from functools import partial
from typing import Callable, Protocol

import pygame.mouse
from pygame import Surface
from pygame.draw import rect
from pygame.event import Event, post
from pygame.font import Font

from command import Command
from command.ui.button import button_hover, button_normal
from objects.events import GAME_EXIT_EVENT, GAME_RESTART_EVENT
from objects.ui.button import uibutton_factory

# BOREL_FONT_PATH = "assets/fonts/Borel-Regular.ttf"
ROBOTO_FONT_PATH = "assets/fonts/RobotoCondensed-Regular.ttf"
ROBOTO_MONO_PATH = "assets/fonts/RobotoMono-Regular.ttf"

GAME_OVER_SIZE = (400, 400)


def run_if_active(func: Callable[..., None]) -> Callable[..., None]:
    def _run_if_active(self: "GameOverMenu", *args: list, **kwargs: dict) -> None:
        if self.active:
            func(self, *args, **kwargs)

    return _run_if_active


def button_restart() -> Command:
    def _button_restart() -> None:
        post(Event(GAME_RESTART_EVENT))

    return _button_restart


def button_exit() -> Command:
    def _button_exit() -> None:
        post(Event(GAME_EXIT_EVENT))

    return _button_exit


class MenuManager(Protocol):
    @property
    def score(self) -> int:
        ...


class GameOverMenu:
    def __init__(self, menu_manager: MenuManager) -> None:
        self.menu_manager = menu_manager

        # constants
        self.title_font = Font(ROBOTO_FONT_PATH, 34)
        self.body_font = Font(ROBOTO_FONT_PATH, 26)
        self.mono_font = Font(ROBOTO_MONO_PATH, 26)
        self.font_color = (238, 255, 255)

        self.background_color = (58, 51, 51)
        self.background_border_color = (255, 238, 238)

        factory = partial(
            uibutton_factory,
            self.body_font,
            self.font_color,
            self.background_color,
        )

        self.buttons = {
            "restart": factory("Restart"),
            "exit": factory("Exit"),
        }

        self.restart_button = uibutton_factory(
            self.body_font,
            self.font_color,
            self.background_color,
            "Restart",
        )
        self.button_pos = (
            (GAME_OVER_SIZE[0] - self.restart_button.active.get_width()) // 2,
            GAME_OVER_SIZE[1] * 0.65,
        )

        # variables
        self.active = False
        self.surface = Surface(GAME_OVER_SIZE)
        self.menu_pos = (0, 0)

        # config
        self.surface.set_colorkey((0, 0, 0))

        # commands
        self.commands = []

    def _background(self) -> None:
        rect(
            self.surface,
            self.background_color,
            (0, 0, *self.surface.get_size()),
            border_radius=10,
        )

    def _border(self) -> None:
        rect(
            self.surface,
            self.background_border_color,
            (0, 0, *self.surface.get_size()),
            width=5,
            border_radius=10,
        )

    def _title(self) -> None:
        title = self.title_font.render("Game Over", True, self.font_color)
        self.surface.blit(
            title,
            (
                (GAME_OVER_SIZE[0] - title.get_width()) // 2,
                GAME_OVER_SIZE[1] * 0.1,
            ),
        )

    def _score(self) -> None:
        score_text = self.body_font.render(f"Score:", True, self.font_color)
        self.surface.blit(
            score_text,
            (
                (GAME_OVER_SIZE[0] - score_text.get_width()) // 2,
                GAME_OVER_SIZE[1] * 0.3,
            ),
        )

        score = self.mono_font.render(
            f"{self.menu_manager.score}", True, self.font_color
        )
        self.surface.blit(
            score,
            (
                (GAME_OVER_SIZE[0] - score.get_width()) // 2,
                GAME_OVER_SIZE[1] * 0.4,
            ),
        )

    def _buttons(self) -> None:
        for i, button in enumerate(self.buttons.values()):
            button_pos = (
                (GAME_OVER_SIZE[0] - button.active.get_width()) // 2,
                int(GAME_OVER_SIZE[1] * (0.6 + 0.2 * i)),
            )
            button.pos = button_pos
            self.surface.blit(button.active, button_pos)

    @run_if_active
    def handle_event(self, event: Event) -> None:
        global_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (
            global_mouse_pos[0] - self.menu_pos[0],
            global_mouse_pos[1] - self.menu_pos[1],
        )
        for button in self.buttons.values():
            if button.collidepoint(mouse_pos):
                self.commands.append(button_hover(button))
            else:
                self.commands.append(button_normal(button))

        if event.type == pygame.MOUSEBUTTONUP:
            if self.buttons["restart"].collidepoint(mouse_pos):
                self.commands.append(button_restart())
            elif self.buttons["exit"].collidepoint(mouse_pos):
                self.commands.append(button_exit())

    @run_if_active
    def update(self, dt: float) -> None:
        for command in self.commands:
            command()

    @run_if_active
    def render(self, screen: Surface) -> None:
        if self.menu_pos == (0, 0):
            self.menu_pos = (
                (screen.get_width() - GAME_OVER_SIZE[0]) // 2,
                (screen.get_height() - GAME_OVER_SIZE[1]) // 2,
            )

        self._background()
        self._border()
        self._title()
        self._score()
        self._buttons()
        screen.blit(self.surface, self.menu_pos)
