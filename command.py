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
        new_blocks_position = [block.pos + self.direction for block in self.target.blocks]
        if self.game_state.check_blocks_collide(new_blocks_position):
            if self.direction.y > 0:
                self.game_state.solidify_tetronimo(self.target)
            return

        for block in self.target.blocks:
            block.pos += self.direction
