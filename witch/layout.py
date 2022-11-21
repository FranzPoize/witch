from witch.layout_state import (
    add_layout,
    get_layout,
)
from witch.state import get_id, push_id, poop_id, get_cursor, set_cursor, get_current_id
from witch.utils import Percentage

HORIZONTAL = "horizontal"
VERTICAL = "vertical"


def start_layout(label, direction, size):
    parent_id = get_current_id()
    parent_layout = get_layout(parent_id)

    id = get_id(label, parent_id)
    push_id(id)

    if isinstance(size, Percentage):
        if parent_layout.direction == HORIZONTAL:
            size = (parent_layout.size[0], size.value(parent_layout.size[1]))
        else:
            size = (size.value(parent_layout.size[0]), parent_layout.size[1])
    else:
        if parent_layout.direction == HORIZONTAL:
            size = (parent_layout.size[0], size)
        else:
            size = (size, parent_layout.size[1])

    add_layout(id, direction, size, get_cursor())


def end_layout():
    id = poop_id()
    layout = get_layout(id)

    if layout.direction == HORIZONTAL:
        next_pos = (layout.pos[0], layout.pos[1] + layout.size[1])
    else:
        next_pos = (layout.pos[0] + layout.size[0], layout.pos[1])

    set_cursor(next_pos)
