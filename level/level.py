from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from pygame import Surface
from pygame.event import Event


class LevelManager(Protocol):
    def transition_to(self, level: str):
        ...


class Level(ABC):
    def __init__(self, game: LevelManager):
        self.game: LevelManager = game

    @abstractmethod
    def handle_event(self, event: Event) -> None:
        """Handle pygame events"""

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update game state"""

    @abstractmethod
    def render(self, screen: Surface) -> None:
        """Render layers"""
