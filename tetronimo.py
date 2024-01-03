from typing import List, Tuple, Optional
from dataclasses import dataclass, field

from random import random
from pygame import Vector2, Color


@dataclass
class Block:
    pos: Vector2
    color: Color


class BlockMesh:
    def __init__(self, field_size: Vector2):
        self.mesh: List[List[Optional[Block]]] = [
            [None for _ in range(int(field_size.x))] for _ in range(int(field_size.y))
        ]


@dataclass
class Tetronimo:
    block_positions: List[Tuple[int, int]] = field(default_factory=list)
    base_color: Color = field(default_factory=lambda: Color(0, 0, 0))

    def __init__(self, spawn_pos: Vector2):
        self.blocks: List[Block] = []
        color = Color(*(self._random_color_element(color_element) for color_element in self.base_color))

        for block_pos in self.block_positions:
            self.blocks.append(Block(
                spawn_pos + Vector2(*block_pos),
                color,
            ))

    def __str__(self) -> str:
        block_pos = [block.pos for block in self.blocks]
        return f"{self.__class__.__name__}: {block_pos}"

    def _random_color_element(self, color_element: int) -> int:
        variation = 50
        color_variation = color_element + random() * variation
        color_variation = max(0, min(255, color_variation))
        return int(color_variation)


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
