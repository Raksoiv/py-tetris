from random import choice
from typing import Tuple

from pygame import Vector2

from tetronimo import Tetronimo, TETRONIMOS


class GameState:
    def __init__(self, field_size: Tuple[int, int], tile_size: int, tile_margin: int) -> None:
        # Constants
        self.field_size = Vector2(field_size)
        self.tile_size = tile_size
        self.tile_margin = tile_margin
        self.spawn_pos = Vector2(self.field_size.x // 2 - 1, 0)  # Spawn position is the top middle of the field
        self.tetronimos = TETRONIMOS

        # Variables
        self.tetronimo = choice(self.tetronimos)(self.spawn_pos)

    def tetronimo_inside_field(self, tetronimo: Tetronimo) -> bool:
        return all(
            self.inside_field(block.pos)
            for block in tetronimo.blocks
        )

    def inside_field(self, pos: Vector2) -> bool:
        return 0 <= pos.x < self.field_size.x - 1 and pos.y < self.field_size.y - 1
