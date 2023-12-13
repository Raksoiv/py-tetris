from pygame import Surface, Color
from pygame.draw import rect

from game_state import GameState
from tetronimo import Block


class Layer:
    def __init__(self, game_state: GameState) -> None:
        self.tile_size = game_state.tile_size
        self.tile_margin = game_state.tile_margin

    def render(self, surface: Surface) -> None:
        raise NotImplementedError()


class TetronimoLayer(Layer):
    def __init__(self, game_state: GameState) -> None:
        super().__init__(game_state)
        self.tetronimo = game_state.tetronimo

    def _render_block(self, surface: Surface, block: Block, color: Color) -> None:
        top = (block.pos.x * self.tile_size) + self.tile_margin
        left = (block.pos.y * self.tile_size) + self.tile_margin
        size = self.tile_size - 2 * self.tile_margin
        rect(
            surface,
            color,
            (top, left, size, size),
            border_radius=self.tile_margin,
        )

    def render(self, surface: Surface) -> None:
        for block in self.tetronimo.blocks:
            self._render_block(surface, block, self.tetronimo.color)
