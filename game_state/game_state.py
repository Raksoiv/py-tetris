from random import choice
from typing import List

from pygame import Vector2

from piece.piece import Piece
from piece.t_piece import TPiece


class GameState:
    def __init__(self, tile_size: int, cube_size: int) -> None:
        # Constants
        self.available_pieces = [TPiece]
        self.start_position = Vector2(10, 0)
        self.epochs_to_move = 20
        self.tile_size = tile_size
        self.cube_size = cube_size
        self.background_color = (0, 0, 0)

        # Variables
        self.pieces: List[Piece] = []
        self.next_piece: Piece = choice(self.available_pieces)
        self.active_piece: Piece = None

    def create_piece(self) -> None:
        next_piece = self.next_piece
        self.active_piece = next_piece(self.start_position)
        self.next_piece = choice(self.available_pieces)
