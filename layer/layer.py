from abc import ABC, abstractmethod

from pygame import Surface


class Layer(ABC):
    @abstractmethod
    def render(self, screen: Surface) -> None:
        pass
