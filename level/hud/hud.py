from typing import Protocol

import pygame.mouse
from pygame import Surface
from pygame.draw import rect
from pygame.event import Event, post
from pygame.font import Font

from command import Command
from command.ui.button import button_hover, button_normal
from command.ui.menu import active_menu
from layer.background import BACKGROUND_COLOR
from objects import Tetronimo
from objects.events import GAME_OPEN_MENU_EVENT
from objects.ui.button import uibutton_factory

BOREL_FONT_PATH = "assets/fonts/Borel-Regular.ttf"
ROBOTO_FONT_PATH = "assets/fonts/RobotoCondensed-Regular.ttf"
ROBOTO_MONO_PATH = "assets/fonts/RobotoMono-Regular.ttf"

HUD_SIZE = (200, 800)
HUD_START_POS = (400, 0)


def button_open_menu() -> Command:
    def _button_open_menu() -> None:
        post(Event(GAME_OPEN_MENU_EVENT))

    return _button_open_menu


class Game(Protocol):
    @property
    def next_tetronimo(self) -> Tetronimo: ...

    @property
    def score(self) -> int: ...


class HUD:
    def __init__(self, game: Game) -> None:
        # constants
        self.game = game
        self.title_font = Font(BOREL_FONT_PATH, 34)
        self.body_font = Font(ROBOTO_FONT_PATH, 26)
        self.mono_font = Font(ROBOTO_MONO_PATH, 26)
        self.font_color = (238, 255, 255)

        # variables
        self.surface = Surface(HUD_SIZE)
        self.next_tetronimo = None

        # config
        self.surface.set_colorkey((0, 0, 0))

        # buttons
        self.menu_button = uibutton_factory(
            self.body_font,
            self.font_color,
            BACKGROUND_COLOR,
            "Menu",
        )

        # commands
        self.commands = []

    def _title(self) -> None:
        title = self.title_font.render("Py-Tetris", True, self.font_color)
        self.surface.blit(
            title,
            (
                (HUD_SIZE[0] - title.get_width()) // 2,
                HUD_SIZE[1] * 0.025,
            ),
        )

    def _next_tetronimo_text(self) -> None:
        text = self.body_font.render("Next:", True, self.font_color)
        self.surface.blit(
            text,
            (
                (HUD_SIZE[0] - text.get_width()) // 2,
                HUD_SIZE[1] * 0.15,
            ),
        )

    def _next_tetronimo(self) -> None:
        tile_size = 20
        tile_margin = 1
        tetronimo_spawn = (4, -1)
        top_margin = HUD_SIZE[1] * 0.214
        left_margin = (HUD_SIZE[0] - (tile_size * 2)) // 2
        next_tetronimo = self.game.next_tetronimo
        for block in next_tetronimo:
            left = (
                left_margin
                + ((block.pos[0] - tetronimo_spawn[0]) * tile_size)
                + tile_margin
            )
            top = (
                top_margin
                + ((block.pos[1] - tetronimo_spawn[1]) * tile_size)
                + tile_margin
            )
            size = tile_size - 2 * tile_margin
            rect(
                self.surface,
                block.color,
                (left, top, size, size),
                border_radius=tile_margin,
            )

    def _score(self) -> None:
        score_text = self.body_font.render(f"Score:", True, self.font_color)
        self.surface.blit(
            score_text,
            (
                (HUD_SIZE[0] - score_text.get_width()) // 2,
                HUD_SIZE[1] * 0.3,
            ),
        )

        score = self.mono_font.render(f"{self.game.score:0>6}", True, self.font_color)
        self.surface.blit(
            score,
            (
                (HUD_SIZE[0] - score.get_width()) // 2,
                HUD_SIZE[1] * 0.35,
            ),
        )

    def _menu_button(self) -> None:
        button_pos = (
            (HUD_SIZE[0] - self.menu_button.active.get_width()) // 2,
            int(HUD_SIZE[1] * 0.9),
        )
        self.menu_button.pos = button_pos
        self.surface.blit(self.menu_button.active, button_pos)

    def handle_event(self, event: Event) -> None:
        global_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (
            global_mouse_pos[0] - HUD_START_POS[0],
            global_mouse_pos[1] - HUD_START_POS[1],
        )

        if self.menu_button.collidepoint(mouse_pos):
            self.commands.append(button_hover(self.menu_button))
        else:
            self.commands.append(button_normal(self.menu_button))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button.collidepoint(mouse_pos):
                self.commands.append(button_open_menu())

    def update(self, delta_time: float) -> None:
        for command in self.commands:
            command()

        self.commands.clear()

    def render(self, screen: Surface) -> None:
        if self.next_tetronimo != self.game.next_tetronimo:
            self.next_tetronimo = self.game.next_tetronimo
            self.surface.fill((0, 0, 0))
            self._title()
            self._next_tetronimo_text()
            self._next_tetronimo()
            self._score()
        self._menu_button()
        screen.blit(self.surface, HUD_START_POS)
