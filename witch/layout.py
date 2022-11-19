from witch.state import add_layout, get_current_view, get_id, get_layout, push_id, poop_id, get_cursor, set_cursor, get_current_id
from witch.utils import Percentage

HORIZONTAL = "horizontal"
VERTICAL = "vertical"

def start_layout(label, direction, size):
    parent_id = get_current_id()
    id = get_id(label, parent_id)
    push_id(id)

    if isinstance(size, Percentage):
        layout = get_layout(parent_id)
        x, y = get_current_view()

        if layout["direction"] == HORIZONTAL:
            size = size.value(y)
        else:
            size = size.value(x)

    add_layout(id, direction, size, get_cursor())
    pass

def end_layout():
    id = poop_id()
    layout = get_layout(id)

    if layout["direction"] == HORIZONTAL:
        next_pos = (layout["pos"][0], layout["pos"][1] + layout["size"])
    else:
        next_pos = (layout["pos"][0] + layout["size"], layout["pos"][1])

    set_cursor(next_pos)


