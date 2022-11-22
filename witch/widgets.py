from curses import A_BOLD, A_DIM, COLOR_BLACK, COLOR_BLUE, COLOR_GREEN, COLOR_WHITE, KEY_UP, KEY_DOWN, A_REVERSE, init_pair, color_pair
from witch.layout_state import (
    add_layout,
    get_layout,
)
from witch.state import (
    add_as_selectable,
    get_current_id,
    get_id,
    is_key_pressed,
    poop_id,
    push_id,
    screen,
    get_cursor,
    add_data,
    get_data,
    selected_id,
    set_cursor,
)
from witch.utils import Percentage, split_text_with_wrap, get_scrolling_info
from witch.layout import HORIZONTAL, VERTICAL

BASIC_BORDER = ["─", "│", "┐", "└", "┘", "┌", "╴", "╶", "▲", "▼", "█"]

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
    add_as_selectable(id)
    base_layout = get_layout(get_current_id())
    base_x, base_y = get_cursor()
    x += base_x
    y += base_y

    base_size_x, base_size_y = base_layout.size

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

    if layout.direction == VERTICAL:
        next_pos = (x, y + sizey)
    else:
        next_pos = (x + sizex, y)

    set_cursor(next_pos)


def start_panel(title, x, y, sizex, sizey, border_style=BASIC_BORDER):
    id = get_id(title, get_current_id())
    add_as_selectable(id)
    base_layout = get_layout(get_current_id())
    base_x, base_y = get_cursor()
    x += base_x
    y += base_y
    push_id(id)
    init_pair(10, COLOR_GREEN, COLOR_BLACK)

    base_size_x, base_size_y = base_layout.size

    if isinstance(sizey, Percentage):
        sizey = sizey.value(base_size_y)

    if isinstance(sizex, Percentage):
        sizex = sizex.value(base_size_x)

    if len(title) > sizex - 4:
        title = title[: sizex - 4]

    panel_data = get_data(id)
    if not panel_data:
        panel_data = {
            "border_style": border_style,
            "selected_index": 0,
            "scroll_position": 0,
            "needs_scrolling": False,
            "max_items" : 1,
            "items": [],
        }

    panel_data["max_items"] = len(panel_data["items"]) if len(panel_data["items"]) > 0 else 1

    # Find out if we need scrolling
    if len(panel_data["items"]) > sizey - 2:
        panel_data["needs_scrolling"] = True

    color = A_DIM
    # Scrolling items
    if selected_id() == id:
        color = A_BOLD | color_pair(10)
        selected_index = panel_data["selected_index"]
        if is_key_pressed(chr(KEY_UP)):
            panel_data["selected_index"] = (
                selected_index - 1
                if selected_index != 0
                else len(panel_data["items"]) - 1
            )
        if is_key_pressed(chr(KEY_DOWN)):
            panel_data["selected_index"] = (selected_index + 1) % len(panel_data["items"])

    if panel_data["selected_index"] + 1 > panel_data["scroll_position"] + sizey - 2:
        panel_data["scroll_position"] += 1

    if panel_data["selected_index"] < panel_data["scroll_position"]:
        panel_data["scroll_position"] -= 1

    # Remove items 
    panel_data["items"] = []

    add_data(id, panel_data)

    add_layout(id, HORIZONTAL, (sizex, sizey), (x, y))

    screen().addstr(
        y,
        x,
        border_style[5]
        + border_style[6]
        + title
        + border_style[7]
        + border_style[0] * (sizex - 4 - len(title))
        + border_style[2],
        color,
    )


def menu_item(name):
    id = get_current_id()
    base_layout = get_layout(id)
    sizex, sizey = base_layout.size
    x, y = base_layout.pos
    panel_data = get_data(id)

    if not panel_data:
        raise Exception("No panel data in menu_item. Probably missing encircling panel")

    border_style = panel_data["border_style"]
    items = panel_data["items"]
    scroll_position = panel_data["scroll_position"]


    init_pair(9, COLOR_WHITE, COLOR_BLUE)

    color = A_DIM
    border_color = A_DIM

    if selected_id() == id:
        border_color = A_BOLD | color_pair(10)

    if panel_data["selected_index"] == len(items) and selected_id() == id:
        color |= color_pair(9) | A_BOLD 

    items.append(name)

    if (
        len(items) - 1 < scroll_position
        or len(items) > scroll_position + sizey - 2
    ):
        return

    if len(name) > sizex - 2:
        name = name[: sizex - 2]

    end_border = border_style[1]
    if panel_data["needs_scrolling"]:
        end_border = get_scrolling_info(len(items) - 1,
                                                    panel_data["max_items"],
                                                    sizey - 2,
                                                    scroll_position,
                                                border_style)

    screen().addstr(
        y + len(items) - scroll_position, # + 1 because we're in menu coordinates and 0 is the title line
        x,
        border_style[1],
        border_color,
    )
    screen().addstr(
        y + len(items) - scroll_position, # + 1 because we're in menu coordinates and 0 is the title line
        x + 1,
        name + " " * (sizex - 2 - len(name)),
        color,
    )
    screen().addstr(
        y + len(items) - scroll_position, # + 1 because we're in menu coordinates and 0 is the title line
        x + sizex - 1,
        end_border,
        border_color,
    )

    if (
        selected_id() == id
        and panel_data["selected_index"] == len(items) - 1
        and is_key_pressed("\n")
    ):
        return True


def end_panel():
    id = get_current_id()
    base_layout = get_layout(id)
    sizex, sizey = base_layout.size
    x, y = base_layout.pos
    panel_data = get_data(id)

    if not panel_data:
        raise Exception("No panel data in menu_item. Probably missing encircling panel")

    border_style = panel_data["border_style"]
    poop_id()

    color = A_DIM
    if selected_id() == id:
        color = A_BOLD | color_pair(10)

    for i in range(len(panel_data["items"]) + 1, sizey - 1):
        screen().addstr(
            y + i,
            x,
            border_style[1] + " " * (sizex - 2) + border_style[1],
            color,
        )

    try:
        screen().addstr(
            y + sizey - 1,
            x,
            border_style[3] + border_style[0] * (sizex - 2) + border_style[4],
            color,
        )
    except Exception:
        pass

    next_pos = (base_layout.pos[0], base_layout.pos[1] + base_layout.size[1])
    set_cursor(next_pos)
