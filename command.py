from pygame import Vector2
from tetronimo import Tetronimo
from game_state import GameState


class Command:
    def __init__(self, game_state: GameState) -> None:
        self.game_state = game_state

    def run(self):
        raise NotImplementedError()


class MoveCommand(Command):
    def __init__(self, game_state: GameState, tetronimo: Tetronimo, direction: Vector2) -> None:
        super().__init__(game_state)
        self.target = tetronimo
        self.direction = direction

    def run(self) -> None:
        if not self.game_state.tetronimo_inside_field(self.target):
            return

        self.target.move(self.direction)
