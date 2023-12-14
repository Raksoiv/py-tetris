from pygame import Surface, Color
from typing import Optional
from pygame.draw import rect

from game_state import GameState, GameStateObserver
from tetronimo import Block


class Layer:
    def __init__(self, game_state: GameState) -> None:
        self.tile_size = game_state.tile_size
        self.tile_margin = game_state.tile_margin
        self.game_state = game_state

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
        raise NotImplementedError()


class TetronimoLayer(Layer):
    def render(self, surface: Surface) -> None:
        color = self.game_state.tetronimo.blocks[0].color
        for block in self.game_state.tetronimo.blocks:
            self._render_block(surface, block, color)


class MeshBlockLayer(Layer, GameStateObserver):
    def __init__(self, game_state: GameState) -> None:
        super().__init__(game_state)
        self.surface: Optional[Surface] = None
        self.updated = False

        game_state.add_observer(self)

    # signal
    def on_tetronimo_solidify(self) -> None:
        if self.surface is None:
            return

        self.surface.fill((36, 36, 36))

        for row in self.game_state.block_mesh.mesh:
            for block in row:
                if block is not None:
                    self._render_block(self.surface, block, block.color)

        self.updated = True

    def render(self, surface: Surface) -> None:
        if self.surface is None:
            self.surface = Surface(surface.get_size(), flags=surface.get_flags())
            self.surface.fill(Color(0, 0, 0, 0))

        if self.updated:
            surface.blit(self.surface, (0, 0))
