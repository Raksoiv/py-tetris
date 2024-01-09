from .level import Level
from pygame import Surface
from pygame.event import Event


class Game(Level):
    def __init__(self, game):
        super().__init__(game)

    def handle_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def render(self, screen: Surface) -> None:
        pass
