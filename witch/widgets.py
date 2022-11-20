from curses import A_BOLD, A_DIM
from witch.state import (
    add_as_selectable,
    add_layout,
    get_current_id,
    get_id,
    poop_id,
    push_id,
    screen,
    get_cursor,
    get_layout,
    add_data,
    get_data,
    selected_id,
    set_cursor,
)
from witch.utils import Percentage, split_text_with_wrap
from witch.layout import HORIZONTAL, VERTICAL

BASIC_BORDER = ["─", "│", "┐", "└", "┘", "┌", "╴", "╶"]


def text_buffer(
    title,
    x,
    y,
    sizex,
    sizey,
    text,
    status="",
    border_style=BASIC_BORDER,
    wrap_lines=False,
):
    id = get_id(title, get_current_id())
    base_layout = get_layout(get_current_id())
    base_x, base_y = get_cursor()
    x += base_x
    y += base_y

    base_size_x, base_size_y = base_layout["size"]

    if isinstance(sizey, Percentage):
        sizey = sizey.value(base_size_y)

    if isinstance(sizex, Percentage):
        sizex = sizex.value(base_size_x)

    if len(title) > sizex - 4:
        title = title[: sizex - 4]

    if len(status) > sizex - 2:
        status = status[: sizex - 2]

    # TODO: this should take into account the title length
    # and remove the half dash (border_style 6 and 7 if the title length
    # is sizex - 2)
    screen().addstr(
        y,
        x,
        border_style[5]
        + border_style[6]
        + title
        + border_style[7]
        + border_style[0] * (sizex - 4 - len(title))
        + border_style[2],
    )

    lines = text.splitlines()
    if wrap_lines:
        lines = split_text_with_wrap(lines, sizex - 2)

    startindex = max(0, len(lines) - sizey - 2)

    for i in range(1, sizey - 1):
        line_text = (
            "" if startindex + i - 1 > len(lines) - 1 else lines[startindex + i - 1]
        )
        if len(line_text) > sizex - 2:
            line_text = line_text[: sizex - 2]
        screen().addstr(
            y + i,
            x,
            border_style[1]
            + line_text
            + " " * (sizex - 2 - len(line_text))
            + border_style[1],
        )

    # TODO: this should take into account the title length
    # and remove the half dash (border_style 6 and 7 if the title length
    # is sizex - 2)
    try:
        screen().addstr(
            y + sizey - 1,
            x,
            border_style[3]
            + border_style[0] * (sizex - 4 - len(status))
            + border_style[6]
            + status
            + border_style[7]
            + border_style[4],
        )
    except Exception:
        pass

    layout = get_layout(get_current_id())

    if layout["direction"] == VERTICAL:
        next_pos = (x, y + sizey)
    else:
        next_pos = (x + sizex, y)

    set_cursor(next_pos)


def start_menu(title, x, y, sizex, sizey, border_style=BASIC_BORDER):
    id = get_id(title, get_current_id())
    add_as_selectable(id)
    base_layout = get_layout(get_current_id())
    base_x, base_y = get_cursor()
    x += base_x
    y += base_y
    push_id(id)

    base_size_x, base_size_y = base_layout["size"]

    if isinstance(sizey, Percentage):
        sizey = sizey.value(base_size_y)

    if isinstance(sizex, Percentage):
        sizex = sizex.value(base_size_x)

    if len(title) > sizex - 4:
        title = title[: sizex - 4]

    add_layout(id, HORIZONTAL, (sizex, sizey), (x, y))
    add_data(id, {"border_style": border_style, "items": []})

    screen().addstr(
        y,
        x,
        border_style[5]
        + border_style[6]
        + title
        + border_style[7]
        + border_style[0] * (sizex - 4 - len(title))
        + border_style[2],
        A_BOLD if selected_id() == id else A_DIM,
    )


def menu_item(name):
    id = get_current_id()
    base_layout = get_layout(id)
    sizex, sizey = base_layout["size"]
    x, y = base_layout["pos"]
    menu_data = get_data(id)
    border_style = menu_data["border_style"]

    menu_data["items"].append(name)

    if len(name) > sizex - 2:
        name = name[: sizex - 2]

    screen().addstr(
        y + len(menu_data["items"]),
        x,
        border_style[1] + name + " " * (sizex - 2 - len(name)) + border_style[1],
        A_BOLD if selected_id() == id else A_DIM,
    )


def end_menu():
    id = get_current_id()
    base_layout = get_layout(id)
    sizex, sizey = base_layout["size"]
    x, y = base_layout["pos"]
    menu_data = get_data(id)
    border_style = menu_data["border_style"]
    poop_id()

    for i in range(len(menu_data["items"]) + 1, sizey - 1):
        screen().addstr(
            y + i,
            x,
            border_style[1] + " " * (sizex - 2) + border_style[1],
            A_BOLD if selected_id() == id else A_DIM,
        )

    try:
        screen().addstr(
            y + sizey - 1,
            x,
            border_style[3] + border_style[0] * (sizex - 2) + border_style[4],
            A_BOLD if selected_id() == id else A_DIM,
        )
    except Exception:
        pass

    next_pos = (base_layout["pos"][0], base_layout["pos"][1] + base_layout["size"][1])
    set_cursor(next_pos)
