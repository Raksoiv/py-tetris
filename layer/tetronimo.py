from typing import Protocol

from pygame import Surface

from objects.tetronimo import Tetronimo

from .layer import Layer
from .mesh_block import render_block


class LayerManager(Protocol):
    @property
    def actual_tetronimo(self) -> Tetronimo:
        ...


class TetronimoLayer(Layer):
    def __init__(self, layer_manager: LayerManager) -> None:
        self.layer_manager = layer_manager

    def render(self, surface: Surface) -> None:
        for block in self.layer_manager.actual_tetronimo:
            render_block(surface, block, block.color)
