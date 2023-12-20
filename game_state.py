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
        self.tetronimo: Tetronimo = choice(TETRONIMOS)(self.spawn_pos)  # Starting tetronimo

    def _pos_inside_field(self, pos: Vector2) -> bool:
        return 0 <= pos.x < self.field_size.x and pos.y < self.field_size.y

    def _pos_not_hit_mesh(self, pos: Vector2) -> bool:
        return self.block_mesh.mesh[int(pos.y)][int(pos.x)] is None

    def _instantiate_new_tetronimo(self) -> None:
        self.tetronimo = choice(TETRONIMOS)(self.spawn_pos)

    def _check_lines(self) -> None:
        row_to = total_rows = len(self.block_mesh.mesh) - 1
        empty_found = False

        for row_from in range(total_rows, -1, -1):
            if empty_found:
                return

            if all(block is None for block in self.block_mesh.mesh[row_to]):
                empty_found = True

            # Copy row from row_from to row_to
            for col_i, upper_block in enumerate(self.block_mesh.mesh[row_from]):
                    self.block_mesh.mesh[row_to][col_i] = upper_block

                    if upper_block is not None:
                        upper_block.pos = Vector2(col_i, row_to)

            # move row_from up if row_to is not full
            if any(block is None for block in self.block_mesh.mesh[row_from]):
                row_to -= 1

    def check_blocks_collide(self, blocks: List[Vector2]) -> bool:
        return not all(self._pos_inside_field(block) and self._pos_not_hit_mesh(block) for block in blocks)

    def solidify_tetronimo(self, tetronimo: Tetronimo) -> None:
        for block in tetronimo.blocks:
            self.block_mesh.mesh[int(block.pos.y)][int(block.pos.x)] = block

        self._check_lines()

        for observer in self.observers:
            observer.on_tetronimo_solidify()

        self._instantiate_new_tetronimo()
