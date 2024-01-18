from typing import Protocol

from pygame import Surface
from pygame.draw import rect

from objects.block import Block
from objects.mesh_block import MeshBlock

from .constants import TILE_MARGIN, TILE_SIZE
from .layer import Layer

BACKGROUND_COLOR = (51, 51, 58)


def render_block(surface: Surface, block: Block, color: tuple[int, int, int]) -> None:
    left = (block.pos[0] * TILE_SIZE) + TILE_MARGIN
    top = (block.pos[1] * TILE_SIZE) + TILE_MARGIN
    size = TILE_SIZE - 2 * TILE_MARGIN
    rect(
        surface,
        color,
        (left, top, size, size),
        border_radius=TILE_MARGIN,
    )


class GameLevel(Protocol):
    @property
    def mesh_block(self) -> MeshBlock:
        ...


class MeshBlockLayer(Layer):
    def __init__(self, game: GameLevel, field_size: tuple[int, int]) -> None:
        self.mesh_block = game.mesh_block
        self.surface = Surface((field_size[0] * TILE_SIZE, field_size[1] * TILE_SIZE))

    def render(self, screen: Surface) -> None:
        self.surface.fill(BACKGROUND_COLOR)

        for row in self.mesh_block:
            for block in row:
                if block is not None:
                    render_block(self.surface, block, block.color)

        screen.blit(self.surface, (0, 0))
