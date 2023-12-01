from command.command import Command
from piece.piece import Piece


class RotatePieceCommand(Command):
    def __init__(self, piece: Piece) -> None:
        self.piece = piece

    def run(self) -> None:
        self.piece.rotate()
