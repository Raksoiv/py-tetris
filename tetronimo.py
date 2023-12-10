from typing import Tuple

from pygame import Vector2


class Block:
    def __init__(self, pos: Vector2):
        self.pos = pos


class Tetronimo:
    block_positions: Tuple[int, int] = []

    def __init__(self, spawn_pos: Vector2):
        self.blocks = [Block(spawn_pos + Vector2(*block_pos)) for block_pos in self.block_positions]

    def move(self, direction: Vector2) -> None:
        for block in self.blocks:
            block.pos += direction


class TTetronimo(Tetronimo):
    block_positions = [(0, 0), (-1, 0), (1, 0), (0, -1)]
