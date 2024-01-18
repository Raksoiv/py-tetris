from typing import Protocol

from pygame import Surface
from pygame.draw import rect
from pygame.font import Font

from objects import Tetronimo

from ..layer import Layer

BOREL_FONT_PATH = "assets/fonts/Borel-Regular.ttf"
ROBOTO_FONT_PATH = "assets/fonts/RobotoCondensed-Regular.ttf"
ROBOTO_MONO_PATH = "assets/fonts/RobotoMono-Regular.ttf"

HUD_SIZE = (200, 800)
HUD_START_POS = (400, 0)


class LayerManager(Protocol):
    @property
    def next_tetronimo(self) -> Tetronimo:
        ...

    @property
    def score(self) -> int:
        ...


class HUDLayer(Layer):
    def __init__(self, layer_manager: LayerManager) -> None:
        # constants
        self.layer_manager = layer_manager
        self.title_font = Font(BOREL_FONT_PATH, 34)
        self.body_font = Font(ROBOTO_FONT_PATH, 26)
        self.mono_font = Font(ROBOTO_MONO_PATH, 26)
        self.font_color = (238, 255, 255)

        # variables
        self.surface = Surface(HUD_SIZE)
        self.next_tetronimo = None

        # config
        self.surface.set_colorkey((0, 0, 0))

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
        next_tetronimo = self.layer_manager.next_tetronimo
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

        score = self.mono_font.render(
            f"{self.layer_manager.score:0>6}", True, self.font_color
        )
        self.surface.blit(
            score,
            (
                (HUD_SIZE[0] - score.get_width()) // 2,
                HUD_SIZE[1] * 0.35,
            ),
        )

    def render(self, screen: Surface) -> None:
        if self.next_tetronimo != self.layer_manager.next_tetronimo:
            self.next_tetronimo = self.layer_manager.next_tetronimo
            self.surface.fill((0, 0, 0))
            self._title()
            self._next_tetronimo_text()
            self._next_tetronimo()
            self._score()
        screen.blit(self.surface, HUD_START_POS)
