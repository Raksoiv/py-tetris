from pygame import Vector2

from game_state import GameState


class Layer:
    def __init__(self, game_state: GameState) -> None:
        self.tile_size = game_state.tile_size
        self.cube_size = game_state.cube_size

    def render(self) -> None:
        raise NotImplementedError
