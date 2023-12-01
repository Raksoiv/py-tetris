from pygame import Surface

from .layer import Layer


class BackgroundLayer(Layer):
    background_color = (0, 0, 0)

    def render(self, window: Surface):
        window.fill(self.background_color)
