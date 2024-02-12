from abc import ABC
from typing import Callable

import pygame.mouse
from pygame import Surface
from pygame.event import Event

from command.ui.button import button_hover, button_normal
from objects.ui.button import UIButton


def run_if_active(func: Callable[..., None]) -> Callable[..., None]:
    def _run_if_active(self: "BaseMenu", *args: list, **kwargs: dict) -> None:
        if self.active:
            func(self, *args, **kwargs)

    return _run_if_active


class BaseMenu(ABC):
    active: bool
    buttons: dict[str, UIButton]
    commands: list[Callable[[], None]]
    menu_pos: tuple[int, int]
    menu_size: tuple[int, int]
    surface: Surface

    @run_if_active
    def handle_event(self, event: Event) -> None:
        global_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (
            global_mouse_pos[0] - self.menu_pos[0],
            global_mouse_pos[1] - self.menu_pos[1],
        )
        for button in self.buttons.values():
            if button.collidepoint(mouse_pos):
                self.commands.append(button_hover(button))
            else:
                self.commands.append(button_normal(button))

        self.handle_custom_events(event)

    def handle_custom_events(self, event: Event) -> None:
        pass

    @run_if_active
    def update(self, dt: float) -> None:
        for command in self.commands:
            command()
        self.commands.clear()

        self.custom_update(dt)

    def custom_update(self, dt: float) -> None:
        pass

    @run_if_active
    def render(self, screen: Surface) -> None:
        if self.menu_pos == (0, 0):
            self.menu_pos = (
                (screen.get_width() - self.menu_size[0]) // 2,
                (screen.get_height() - self.menu_size[1]) // 2,
            )

        self.custom_render(screen)

        screen.blit(self.surface, self.menu_pos)

    def custom_render(self, surface: Surface) -> None:
        pass
