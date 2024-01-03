from random import choice
from typing import List, Tuple

from pygame import Vector2

from tetronimo import TETRONIMOS, Tetronimo, BlockMesh
from observable import Observable


class GameStateObserver:
    def on_tetronimo_solidify(self) -> None:
        raise NotImplementedError()


class GameState(Observable):
    def __init__(self, field_size: Tuple[int, int], tile_size: int, tile_margin: int) -> None:
        super().__init__()

        # Constants
        self.field_size = Vector2(field_size)
        self.tile_size = tile_size
        self.tile_margin = tile_margin
        self.spawn_pos = Vector2(self.field_size.x // 2 - 1, 0)  # Spawn position is the top middle of the field

        # Variables
        self.block_mesh = BlockMesh(self.field_size)
        self.next_tetronimo: Tetronimo = choice(TETRONIMOS)(self.spawn_pos)  # Next tetronimo
        self.tetronimo: Tetronimo = choice(TETRONIMOS)(self.spawn_pos)  # Starting tetronimo
        self.score = 0

    def _pos_inside_field(self, pos: Vector2) -> bool:
        return 0 <= pos.x < self.field_size.x and pos.y < self.field_size.y

    def _pos_not_hit_mesh(self, pos: Vector2) -> bool:
        return self.block_mesh.mesh[int(pos.y)][int(pos.x)] is None

    def _instantiate_new_tetronimo(self) -> None:
        self.tetronimo = self.next_tetronimo
        self.next_tetronimo = choice(TETRONIMOS)(self.spawn_pos)

    def _increase_score(self, completed_lines: int) -> None:
        if completed_lines == 1:
            self.score += 40
        elif completed_lines == 2:
            self.score += 100
        elif completed_lines == 3:
            self.score += 300
        elif completed_lines == 4:
            self.score += 1200

    def _check_lines(self) -> None:
        completed_lines = 0
        for y in range(len(self.block_mesh.mesh) - 1, -1, -1):
            for x in range(len(self.block_mesh.mesh[y])):
                new_y = y + completed_lines
                self.block_mesh.mesh[new_y][x] = self.block_mesh.mesh[y][x]

                block = self.block_mesh.mesh[new_y][x]
                if block is not None:
                    block.pos = Vector2(x, new_y)
            if all(block is not None for block in self.block_mesh.mesh[y]):
                completed_lines += 1

        self._increase_score(completed_lines)

    def check_blocks_collide(self, blocks: List[Vector2]) -> bool:
        return not all(self._pos_inside_field(block) and self._pos_not_hit_mesh(block) for block in blocks)

    def solidify_tetronimo(self, tetronimo: Tetronimo) -> None:
        for block in tetronimo.blocks:
            self.block_mesh.mesh[int(block.pos.y)][int(block.pos.x)] = block

        self._check_lines()

        for observer in self.observers:
            observer.on_tetronimo_solidify()

        self._instantiate_new_tetronimo()
