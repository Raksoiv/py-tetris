from random import shuffle

from . import Tetronimo
from .block import Block, block_pos_hit_bottom, block_pos_hit_top
from .mesh_block import MeshBlock

TETRONIMOS: dict[str, tuple[tuple[int, int, int], list[tuple[int, int]]]] = {
    "T": (
        (130, 2, 99),
        [(0, 0), (-1, 0), (1, 0), (0, -1)],
    ),
    "L": (
        (247, 92, 3),
        [(0, 0), (-1, 0), (1, 0), (1, -1)],
    ),
    "O": (
        (255, 255, 156),
        [(0, 0), (0, -1), (1, 0), (1, -1)],
    ),
    "I": (
        (0, 255, 255),
        [(0, 0), (-1, 0), (1, 0), (2, 0)],
    ),
    "S": (
        (0, 255, 0),
        [(0, 0), (1, 0), (0, -1), (-1, -1)],
    ),
    "Z": (
        (255, 0, 0),
        [(0, 0), (-1, 0), (0, -1), (1, -1)],
    ),
    "J": (
        (0, 0, 255),
        [(0, 0), (-1, 0), (1, 0), (-1, -1)],
    ),
}


def get_random_tetronimo_bag(spawn_pos: tuple[int, int]) -> list[Tetronimo]:
    tetronimo_bag = list(TETRONIMOS.keys())
    shuffle(tetronimo_bag)

    return [
        [
            Block(
                (pos[0] + spawn_pos[0], pos[1] + spawn_pos[1]),
                TETRONIMOS[tetronimo_key][0],
            )
            for pos in TETRONIMOS[tetronimo_key][1]
        ]
        for tetronimo_key in tetronimo_bag
    ]


def tetronimo_hit_bottom(field_size: tuple[int, int], tetronimo: Tetronimo) -> bool:
    return any(block_pos_hit_bottom(field_size, block.pos) for block in tetronimo)


def tetronimo_hit_top(tetronimo: Tetronimo) -> bool:
    return any(block_pos_hit_top(block.pos) for block in tetronimo)


def tetronimo_bottom_hit_mesh_block(
    mesh_block: MeshBlock, tetronimo: Tetronimo
) -> bool:
    # Ensure fresh spawn tetromino don't hit the mesh block
    if any(block.pos[1] < 0 for block in tetronimo):
        return False
    return any(
        mesh_block[block.pos[1]][block.pos[0]] is not None for block in tetronimo
    )


def tetromino_move(tetromino: Tetronimo, direction: tuple[int, int]) -> None:
    for block in tetromino:
        block.pos = (block.pos[0] + direction[0], block.pos[1] + direction[1])
