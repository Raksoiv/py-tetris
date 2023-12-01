from typing import List

from pygame import Vector2


class Piece:
    def __init__(self, position: Vector2) -> None:
        self.active = True
        self.rotation = 0
        self.last_position = None
        self.position = Vector2(position.x, position.y)

    def _get_cubes(self, position: Vector2) -> List[Vector2]:
        raise NotImplementedError

    def rotate(self) -> None:
        self.rotation = (self.rotation + 1) % 4

    # Returns the position (x, y) of the cubes of the piece
    def get_cubes(self) -> List[Vector2]:
        return self._get_cubes(self.position)

    # Returns the position (x, y) of the last cubes of the piece
    def get_last_cubes(self) -> List[Vector2]:
        if not self.last_position:
            return []
        return self._get_cubes(self.last_position)
