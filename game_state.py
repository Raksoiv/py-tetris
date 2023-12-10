from typing import Tuple

from pygame import Vector2

from tetronimo import TTetronimo
from random import choice


class GameState:
    def __init__(self, field_size: Tuple[int, int], tile_size: int, tile_margin: int):
        # Constants
        self.field_size = field_size
        self.tile_size = tile_size
        self.tile_margin = tile_margin
        self.spawn_pos = Vector2(field_size[0] // 2 - 1, 0)  # Spawn position is the top middle of the field
        self.tetronimos = [TTetronimo]

        # Variables
        self.tetronimo = choice(self.tetronimos)(self.spawn_pos)
