from pygame import Surface, draw

from game_state import GameState

from .layer import Layer


class ActivePieceLayer(Layer):
    def __init__(self, game_state: GameState) -> None:
        super().__init__(game_state)
        self.game_state = game_state

    def render(self, window: Surface) -> None:
        if self.game_state.active_piece:
            for cube in self.game_state.active_piece.get_cubes():
                draw.rect(
                    window,
                    self.game_state.active_piece.color,
                    (
                        cube[0] * self.tile_size,
                        cube[1] * self.tile_size,
                        self.cube_size,
                        self.cube_size,
                    ),
                )
