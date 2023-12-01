from typing import List

from pygame import Vector2

from .piece import Piece


class TPiece(Piece):
    color = (100, 5, 45)

    # Returns the position (x, y) of the cubes based on position
    def _get_cubes(self, position: Vector2) -> List[Vector2]:
        cubes = [Vector2(position.x, position.y)] # always add the center cube
        if self.rotation != 0:
            cubes.append(Vector2(position.x, position.y - 1)) # add the top cube
        if self.rotation != 1:
            cubes.append(Vector2(position.x + 1, position.y)) # add the right cube
        if self.rotation != 2:
            cubes.append(Vector2(position.x, position.y + 1)) # add the bottom cube
        if self.rotation != 3:
            cubes.append(Vector2(position.x - 1, position.y)) # add the left cube

        return cubes
