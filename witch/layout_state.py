from dataclasses import dataclass
from typing import Union

from witch.utils import Percentage


@dataclass
class Layout:
    direction: str
    size: Union[int, Percentage]
    pos: tuple[int, int]


state_layout: dict[str, Layout] = dict()


def add_layout(id, direction, size, pos):
    state_layout[id] = Layout(direction, size, pos)


def get_layout(id) -> Layout:
    return state_layout[id]
