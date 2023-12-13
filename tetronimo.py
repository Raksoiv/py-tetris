from typing import List, Tuple

from pygame import Vector2, Color
from random import random


class Block:
    def __init__(self, pos: Vector2):
        self.pos = pos


class BlockMesh:
    def __init__(self, field_size: Vector2):
        self.mesh = [[None for _ in range(field_size.x)] for _ in range(field_size.y)]


class Tetronimo:
    block_positions: List[Tuple[int, int]] = []
    base_color: Color = Color(0, 0, 0)

    def __init__(self, spawn_pos: Vector2):
        self.blocks = [Block(spawn_pos + Vector2(*block_pos)) for block_pos in self.block_positions]
        self.color = Color(
            self._random_color_element(self.base_color.r),
            self._random_color_element(self.base_color.g),
            self._random_color_element(self.base_color.b),
        )

    def _random_color_element(self, color_element: int) -> int:
        variation = 50
        color_variation = color_element + random() * variation
        color_variation = max(0, min(255, color_variation))
        return int(color_variation)

    def move(self, direction: Vector2) -> None:
        for block in self.blocks:
            block.pos += direction


class TTetronimo(Tetronimo):
    block_positions = [(0, 0), (-1, 0), (1, 0), (0, -1)]
    base_color = Color(130, 2, 99)


class LTetronimo(Tetronimo):
    block_positions = [(0, 0), (-1, 0), (1, 0), (1, -1)]
    base_color = Color(247, 92, 3)


class OTetronimo(Tetronimo):
    block_positions = [(0, 0), (0, -1), (1, 0), (1, -1)]
    base_color = Color(255, 255, 156)


class ITetronimo(Tetronimo):
    block_positions = [(0, 0), (-1, 0), (1, 0), (2, 0)]
    base_color = Color(41, 115, 115)


class ZTetronimo(Tetronimo):
    block_positions = [(0, 0), (-1, 0), (0, -1), (1, -1)]
    base_color = Color(6, 81, 67)


class STetronimo(Tetronimo):
    block_positions = [(0, 0), (1, 0), (0, -1), (-1, -1)]
    base_color = Color(253, 21, 27)


class JTetronimo(Tetronimo):
    block_positions = [(0, 0), (-1, 0), (1, 0), (-1, -1)]
    base_color = Color(255, 202, 212)


TETRONIMOS = [
    TTetronimo,
    LTetronimo,
    OTetronimo,
    ITetronimo,
    ZTetronimo,
    STetronimo,
    JTetronimo,
]
