from objects.ui import UIButton

from .. import Command


def button_hover(button: UIButton) -> Command:
    def _button_hover() -> None:
        button.set_hover_active()

    return _button_hover


def button_normal(button: UIButton) -> Command:
    def _button_normal() -> None:
        button.set_normal_active()

    return _button_normal
