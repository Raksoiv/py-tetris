from settings import *
from level import Game


if __name__ == "__main__":
    game = Game(WINDOW_RESOLUTION, FIELD_SIZE, TILE_SIZE,
                TILE_MARGIN, INITIAL_TETRONIMO_DOWN_INTERVAL, FPS)
    game.run()
