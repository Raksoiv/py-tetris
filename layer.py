from pygame import Surface, Color
from typing import Tuple
from pygame.draw import rect
from pygame.font import Font

from game_state import GameState, GameStateObserver
from tetronimo import Block


class Layer:
    def __init__(self, game_state: GameState) -> None:
        self.tile_size = game_state.tile_size
        self.tile_margin = game_state.tile_margin
        self.game_state = game_state

    def _render_block(self, surface: Surface, block: Block, color: Color) -> None:
        left = (block.pos.x * self.tile_size) + self.tile_margin
        top = (block.pos.y * self.tile_size) + self.tile_margin
        size = self.tile_size - 2 * self.tile_margin
        rect(
            surface,
            color,
            (left, top, size, size),
            border_radius=self.tile_margin,
        )

    def render(self, surface: Surface) -> None:
        raise NotImplementedError()


class TetronimoLayer(Layer):
    def render(self, surface: Surface) -> None:
        for block in self.game_state.tetronimo.blocks:
            self._render_block(surface, block, block.color)


class MeshBlockLayer(Layer, GameStateObserver):
    def __init__(self, game_state: GameState, background_color: Tuple[int, int, int],
                 field_resolution: Tuple[int, int]) -> None:
        super().__init__(game_state)
        self.updated = False
        self.background_color = background_color

        self.surface = Surface(field_resolution)
        self.surface.fill(self.background_color)

        game_state.add_observer(self)

    # signal
    def on_tetronimo_solidify(self) -> None:
        self.surface.fill(self.background_color)

        for row in self.game_state.block_mesh.mesh:
            for block in row:
                if block is not None:
                    self._render_block(self.surface, block, block.color)

        self.updated = True

    def render(self, surface: Surface) -> None:
        surface.blit(self.surface, (0, 0))


class UILayer(Layer):
    def __init__(
            self, game_state: GameState, ui_resolution: Tuple[int, int], ui_x_margin: int,
            background_color: Tuple[int, int, int], font_path: str,
            font_color: Tuple[int, int, int],
            ) -> None:
        super().__init__(game_state)

        self.background_color = background_color

        font = Font(font_path, 30)
        self.next_piece_text_surface = font.render("Next piece:", True, font_color)
        self.next_piece_text_pos = (
            ui_x_margin + (ui_resolution[0] - self.next_piece_text_surface.get_width()) // 2,
            ui_resolution[1] * .05,
        )

        self.next_piece_top = ui_resolution[1] * .2
        self.next_piece_center_x = ui_resolution[0] // 2
        self.piece_margin_x = ui_x_margin

    def _render_next_piece(self, surface: Surface) -> None:
        tile_size = self.tile_size // 1.5
        center_x = self.next_piece_center_x - tile_size // 2
        piece_center_x = self.game_state.field_size.x // 2 - 1

        size = tile_size - 2 * self.tile_margin
        for block in self.game_state.next_tetronimo.blocks:
            x = block.pos.x - piece_center_x
            left = center_x + x * tile_size + self.piece_margin_x

            y = block.pos.y
            top = self.next_piece_top + y * tile_size

            rect(surface, block.color, (left, top, size, size))

    def render(self, surface: Surface) -> None:
        surface.fill(self.background_color)
        surface.blit(self.next_piece_text_surface, self.next_piece_text_pos)
        self._render_next_piece(surface)
