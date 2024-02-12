from typing import Protocol

from .. import Command


class Level(Protocol):
    @property
    def stop_update(self) -> bool:
        ...

    @stop_update.setter
    def stop_update(self, value: bool) -> None:
        ...


class Menu(Protocol):
    @property
    def active(self) -> bool:
        ...

    @active.setter
    def active(self, value: bool) -> None:
        ...


def active_menu(level: Level, menu: Menu) -> Command:
    def _active_menu() -> None:
        level.stop_update = True
        menu.active = True

    return _active_menu


def deactivate_menu(level: Level, menu: Menu) -> Command:
    def _deactivate_menu() -> None:
        level.stop_update = False
        menu.active = False

    return _deactivate_menu
