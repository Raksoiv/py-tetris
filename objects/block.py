from dataclasses import dataclass


@dataclass
class Block:
    pos: tuple[int, int]
    color: tuple[int, int, int]


def block_pos_inside_field(
    field_size: tuple[int, int], block_pos: tuple[int, int]
) -> bool:
    return 0 <= block_pos[0] < field_size[0] and 0 <= block_pos[1] < field_size[1]


def block_pos_hit_bottom(
    field_size: tuple[int, int], block_pos: tuple[int, int]
) -> bool:
    return block_pos[1] >= field_size[1] - 1


def block_pos_hit_top(block_pos: tuple[int, int]) -> bool:
    return block_pos[1] <= 0
