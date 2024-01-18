from objects.block import block_pos_inside_field
from objects.mesh_block import MeshBlock, block_pos_hit_mesh_block
from objects.tetronimo import Tetronimo


def move_tetronimo(
    field_size: tuple[int, int],
    mesh_block: MeshBlock,
    tetronimo: Tetronimo,
    direction: tuple[int, int],
) -> None:
    new_pos = []
    for block in tetronimo:
        new_block_pos = (block.pos[0] + direction[0], block.pos[1] + direction[1])
        if not block_pos_inside_field(field_size, new_block_pos):
            return
        if block_pos_hit_mesh_block(mesh_block, new_block_pos):
            return
        new_pos.append(new_block_pos)

    for block, pos in zip(tetronimo, new_pos):
        block.pos = pos


def rotate_tetronimo(
    field_size: tuple[int, int], mesh_block: MeshBlock, tetronimo: Tetronimo
) -> None:
    pivot = tetronimo[0].pos
    new_pos = []
    for block in tetronimo:
        translated = (block.pos[0] - pivot[0], block.pos[1] - pivot[1])
        rotated = (-translated[1], translated[0])
        new_block_pos = rotated[0] + pivot[0], rotated[1] + pivot[1]
        if not block_pos_inside_field(field_size, new_block_pos):
            return
        if block_pos_hit_mesh_block(mesh_block, new_block_pos):
            return
        new_pos.append(new_block_pos)

    for block, pos in zip(tetronimo, new_pos):
        block.pos = pos
