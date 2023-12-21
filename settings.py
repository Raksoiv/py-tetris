TILE_SIZE = 40
TILE_MARGIN = 2
FPS = 60

# Field dimensions
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 10, 20
FIELD_RESOLUTION = FIELD_WIDTH * TILE_SIZE, FIELD_HEIGHT * TILE_SIZE

# Windows dimensions
WINDOW_RATIO_WIDTH, WINDOW_RATIO_HEIGHT = 1, 1
WINDOW_RESOLUTION = WINDOW_WIDTH, WINDOW_HEIGHT = int(FIELD_RESOLUTION[0] * WINDOW_RATIO_WIDTH), \
                                                  int(FIELD_RESOLUTION[1] * WINDOW_RATIO_HEIGHT)

# Timers (in milliseconds)
INITIAL_TETRONIMO_DOWN_INTERVAL = 400

# Assets
FONT_PATH = "assets/fonts/Borel-Regular.ttf"
