from pygame import Surface

from .layer import Layer

BACKGROUND_COLOR = (102, 102, 112)


class BackgroundLayer(Layer):
    def render(self, screen: Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
