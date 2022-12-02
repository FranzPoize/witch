from witchtui.layout_state import (
    add_layout,
    get_layout,
)
from witchtui.state import get_id, push_id, poop_id, get_cursor, set_cursor, get_current_id
from witchtui.utils import get_size_value

HORIZONTAL = "horizontal"
VERTICAL = "vertical"


def start_layout(label, direction, size):
    parent_id = get_current_id()
    parent_layout = get_layout(parent_id)

    id = get_id(label, parent_id)
    push_id(id)

    if parent_layout.direction == VERTICAL:
        size = (parent_layout.size[0], get_size_value(size, parent_layout.size[1]))
    else:
        size = (get_size_value(size, parent_layout.size[0]), parent_layout.size[1])

    add_layout(id, direction, size, get_cursor())


def end_layout():
    id = poop_id()
    layout = get_layout(id)

    if layout.direction == HORIZONTAL:
        next_pos = (layout.pos[0], layout.pos[1] + layout.size[1])
    else:
        next_pos = (layout.pos[0] + layout.size[0], layout.pos[1])

    set_cursor(next_pos)
