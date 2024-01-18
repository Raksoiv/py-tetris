from . import MeshBlock, Tetronimo


def new_mesh_block(width: int, height: int) -> MeshBlock:
    return [[None for _ in range(width)] for _ in range(height)]


def add_tetronimo_to_mesh_block(mesh_block: MeshBlock, tetronimo: Tetronimo) -> None:
    for block in tetronimo:
        mesh_block[block.pos[1]][block.pos[0]] = block


def block_pos_hit_mesh_block(mesh_block: MeshBlock, block_pos: tuple[int, int]) -> bool:
    return mesh_block[block_pos[1]][block_pos[0]] is not None


def block_bottom_hit_mesh_block(
    mesh_block: MeshBlock, block_pos: tuple[int, int]
) -> bool:
    return mesh_block[block_pos[1] + 1][block_pos[0]] is not None


def remove_completed_lines(mesh_block: MeshBlock) -> int:
    completed_lines = 0
    for y in range(len(mesh_block) - 1, -1, -1):
        for x in range(len(mesh_block[y])):
            new_y = y + completed_lines
            mesh_block[new_y][x] = mesh_block[y][x]

            block = mesh_block[new_y][x]
            if block is not None:
                block.pos = (x, new_y)
        if all(block is not None for block in mesh_block[y]):
            completed_lines += 1

    return completed_lines
