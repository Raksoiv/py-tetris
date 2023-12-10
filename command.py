from pygame import Vector2
from tetronimo import Tetronimo


class Command:
    def run(self):
        raise NotImplementedError()


class MoveCommand(Command):
    def __init__(self, tetronimo: Tetronimo, direction: Vector2) -> None:
        self.target = tetronimo
        self.direction = direction

    def run(self) -> None:
        self.target.move(self.direction)
