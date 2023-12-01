from pygame import Vector2

from command.command import Command
from piece.piece import Piece


class MovePieceCommand(Command):
    def __init__(self, piece: Piece, move_vector: Vector2) -> None:
        self.piece = piece
        self.move_vector = move_vector

    def run(self) -> None:
        self.piece.last_position = self.piece.position.copy()
        self.piece.position += self.move_vector
