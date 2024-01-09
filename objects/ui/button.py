from dataclasses import dataclass

from pygame import Surface
from pygame.draw import rect
from pygame.font import Font


@dataclass
class UIButton:
    normal: Surface
    hover: Surface
    active: Surface
    pos: tuple[int, int] = (0, 0)

    def collidepoint(self, pos: tuple[int, int]) -> bool:
        return self.active.get_rect(topleft=self.pos).collidepoint(pos)

    def set_hover_active(self) -> None:
        self.active = self.hover

    def set_normal_active(self) -> None:
        self.active = self.normal


def uibutton_factory(
    font: Font,
    font_color: tuple[int, int, int],
    background_color: tuple[int, int, int],
    text: str,
) -> UIButton:
    normal_text_surface = font.render(text, True, font_color)
    normal = Surface(
        (normal_text_surface.get_width() + 40, normal_text_surface.get_height() + 20)
    )
    normal.set_colorkey((0, 0, 0))
    rect(
        normal,
        background_color,
        (0, 0, *normal.get_size()),
        border_radius=5,
    )
    normal.blit(normal_text_surface, (20, 10))
    rect(
        normal,
        font_color,
        (0, 0, *normal.get_size()),
        width=2,
        border_radius=5,
    )

    hover_text_surface = font.render(text, True, background_color)
    hover = Surface(
        (hover_text_surface.get_width() + 40, hover_text_surface.get_height() + 20)
    )
    hover.set_colorkey((0, 0, 0))
    rect(
        hover,
        font_color,
        (0, 0, *hover.get_size()),
        border_radius=5,
    )
    hover.blit(hover_text_surface, (20, 10))

    return UIButton(normal, hover, normal)
