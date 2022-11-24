from math import ceil
from curses import (
    A_DIM,
    KEY_UP,
    KEY_DOWN,
)
from witch.layout_state import (
    add_layout,
    get_layout,
)
from witch.state import (
    add_as_selectable,
    get_color,
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
    set_selected_id,
)
from witch.utils import (
    split_text_with_wrap,
    get_size_value,
)
from witch.layout import HORIZONTAL, VERTICAL

BASIC_BORDER = ["─", "│", "┐", "└", "┘", "┌", "╴", "╶", "▲", "▼", "█"]

POSITION_CENTER = "pos_center"
POSITION_CENTER_HORIZ = "pos_center_horiz"
POSITION_CENTER_VERTICAL = "pos_center_vert"


def text_buffer(
    title,
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
    x, y = get_cursor()

    base_size_x, base_size_y = base_layout.size

    sizey = get_size_value(sizey, base_size_y)
    sizex = get_size_value(sizex, base_size_x)

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


def get_scrolling_border(index, max_index, size, position, border_style):
    id = get_current_id()
    panel_data = get_data(id)
    scroll_offset_index = index - position
    scroll_oversize = max_index - size
    scroller_size = max(1, (size - 2) - scroll_oversize)
    scroll_ratio = scroll_oversize / -(scroller_size - (size - 2))

    if not panel_data:
        raise Exception("Can't scroll outside panel")

    if panel_data["needs_scrolling"]:
        if scroll_offset_index == 0:
            return border_style[8]
        elif scroll_offset_index == size - 1:
            return border_style[9]
        elif (
            scroll_offset_index > ceil(position / scroll_ratio)
            and scroll_offset_index - 1 < ceil(position / scroll_ratio) + scroller_size
        ):
            return border_style[10]

    return border_style[1]


def get_border_color(id):
    if selected_id() == id:
        return get_color("panel_selected")
    else:
        return A_DIM


def get_item_color(id, panel_data, items_len, name="default"):
    if panel_data["selected_index"] == items_len and selected_id() == id:
        return get_color(f"{name}_hovered")
    else:
        return get_color(f"{name}")


def print_first_elem():
    pass


def print_last_elem():
    pass


def start_same_line(border_style=BASIC_BORDER):
    id = get_current_id()
    panel_data = get_data(id)
    base_layout = get_layout(id)
    base_layout.size = (base_layout.size[0] - 2, base_layout.size[1])
    _, sizey = base_layout.size
    x, y = get_cursor()

    if not panel_data:
        raise Exception("Same line not in panel")

    if panel_data["same_line_mode"]:
        raise Exception("Can't nest same line")

    panel_data["items_len"] += 1
    panel_data["same_line_mode"] = True
    panel_data["same_line_size"] = 0

    if (
        panel_data["items_len"] - 1 < panel_data["scroll_position"]
        or panel_data["items_len"] > panel_data["scroll_position"] + sizey - 2
    ):
        return

    border_color = get_border_color(id)

    screen().addstr(
        y,  # + 1 because we're in menu coordinates and 0 is the title line
        x,
        border_style[1],
        border_color,
    )

    set_cursor((x + 1, y))


def end_same_line(border_style=BASIC_BORDER):
    id = get_current_id()
    panel_data = get_data(id)
    base_layout = get_layout(id)
    base_layout.size = (base_layout.size[0] + 2, base_layout.size[1])
    x, y = get_cursor()
    sizex, sizey = base_layout.size

    if not panel_data:
        raise Exception("Same line not in panel")

    panel_data["same_line_mode"] = False
    same_line_size = panel_data["same_line_size"]
    panel_data["same_line_size"] = 0

    if (
        panel_data["items_len"] - 1 < panel_data["scroll_position"]
        or panel_data["items_len"] > panel_data["scroll_position"] + sizey - 2
    ):
        return

    border_color = get_border_color(id)
    end_border = get_scrolling_border(
        panel_data["items_len"] - 1,
        panel_data["max_items"],
        sizey - 2,
        panel_data["scroll_position"],
        border_style,
    )

    try:
        screen().addstr(
            y,
            x + sizex - 2 - same_line_size,
            end_border,
            border_color,
        )
    except Exception:
        pass

    set_cursor((x - same_line_size - 1, y + 1))


def start_panel(title, sizex, sizey, start_selected=False, border_style=BASIC_BORDER):
    id = get_id(title, get_current_id())
    add_as_selectable(id)
    base_layout = get_layout(get_current_id())
    x, y = get_cursor()
    push_id(id)

    base_size_x, base_size_y = base_layout.size

    sizey = get_size_value(sizey, base_size_y)
    sizex = get_size_value(sizex, base_size_x)

    if len(title) > sizex - 4:
        title = title[: sizex - 4]

    panel_data = get_data(id)
    if not panel_data:
        if start_selected:
            set_selected_id(id)
        panel_data = {
            "border_style": border_style,
            "selected_index": 0,
            "scroll_position": 0,
            "needs_scrolling": False,
            "max_items": 1,
            "same_line_mode": False,
            "items_len": 0,
        }

        add_data(id, panel_data)
    else:
        panel_data["touch"] = True

    panel_data["max_items"] = (
        panel_data["items_len"] if panel_data["items_len"] > 0 else 1
    )

    # Find out if we need scrolling
    if panel_data["items_len"] > sizey - 2:
        panel_data["needs_scrolling"] = True

    # Scrolling items
    if selected_id() == id:
        selected_index = panel_data["selected_index"]
        if is_key_pressed(chr(KEY_UP)):
            panel_data["selected_index"] = (
                selected_index - 1
                if selected_index != 0
                else panel_data["items_len"] - 1
            )
        if is_key_pressed(chr(KEY_DOWN)):
            panel_data["selected_index"] = (selected_index + 1) % panel_data[
                "items_len"
            ]

    if panel_data["selected_index"] + 1 > panel_data["scroll_position"] + sizey - 2:
        panel_data["scroll_position"] += 1

    if panel_data["selected_index"] < panel_data["scroll_position"]:
        panel_data["scroll_position"] -= 1

    # Remove items
    panel_data["items_len"] = 0

    add_layout(id, HORIZONTAL, (sizex, sizey), (x, y))

    color = get_border_color(id)

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

    set_cursor((x, y + 1))

    return id

def text_item(content, line_sizex=None):
    id = get_current_id()
    base_layout = get_layout(id)
    x, y = get_cursor()
    sizex, sizey = base_layout.size
    panel_data = get_data(id)

    if not panel_data:
        raise Exception("No panel data in menu_item. Probably missing encircling panel")

    border_style = panel_data["border_style"]
    scroll_position = panel_data["scroll_position"]
    same_line_mode = panel_data["same_line_mode"]

    if same_line_mode:
        if line_sizex is not None:
            sizex = get_size_value(line_sizex, sizex)
        else:
            sizex = sizex - panel_data["same_line_size"]

    if not same_line_mode:
        panel_data["items_len"] += 1

    items_len = panel_data["items_len"]

    if items_len - 1 < scroll_position or items_len > scroll_position + sizey - 2:
        return (False, False)

    printable_size = sizex - 2

    if same_line_mode:
        printable_size = sizex

    strings = []

    if isinstance(content, tuple):
        strings.append(content)
    elif not isinstance(content, list):
        strings.append((content, "default"))
    else:
        for c in content:
            if isinstance(c, tuple):
                strings.append(c)
            else:
                strings.append((c, "default"))


    border_color = get_border_color(id)

    end_border = get_scrolling_border(
        items_len - 1,
        panel_data["max_items"],
        sizey - 2,
        scroll_position,
        border_style,
    )

    if not same_line_mode:
        screen().addstr(
            y,  # + 1 because we're in menu coordinates and 0 is the title line
            x,
            border_style[1],
            border_color,
        )
        x += 1

    content_len = 0

    for string in strings:
        text = string[0]
        if content_len + len(text) > printable_size:
            text = text[:printable_size - content_len]

        color = get_item_color(id, panel_data, items_len - 1, string[1])

        screen().addstr(
            y,  # + 1 because we're in menu coordinates and 0 is the title line
            x + content_len,
            text,
            color,
        )

        content_len += len(text)

    screen().addstr(
        y,  # + 1 because we're in menu coordinates and 0 is the title line
        x + content_len,
        " " * (printable_size - content_len),
        color,
    )

    if not same_line_mode:
        x -= 1
        screen().addstr(
            y,  # + 1 because we're in menu coordinates and 0 is the title line
            x + sizex - 1,
            end_border,
            border_color,
        )

    # TODO: size is not correct because - 2 is shared between all element in a same line layout

    if same_line_mode:
        set_cursor((x + printable_size, y))
        panel_data["same_line_size"] += printable_size
    else:
        set_cursor((x, y + 1))

    hovered = False
    pressed = False

    if (
        selected_id() == id
        and panel_data["selected_index"] == items_len - 1
    ):
        hovered = True
        if is_key_pressed("\n"):
            pressed = True

    return (hovered, pressed)


def end_panel():
    id = get_current_id()
    base_layout = get_layout(id)
    sizex, sizey = base_layout.size
    base_x, base_y = base_layout.pos
    x, y = get_cursor()
    panel_data = get_data(id)

    if not panel_data:
        raise Exception("No panel data in menu_item. Probably missing encircling panel")

    border_style = panel_data["border_style"]
    poop_id()

    color = get_border_color(id)

    for i in range(0, sizey - ((panel_data["items_len"] + 2))):
        try:
            screen().addstr(
                y + i,
                x,
                border_style[1] + " " * (sizex - 2) + border_style[1],
                color,
            )
        except Exception:
            pass

    try:
        screen().addstr(
            y + sizey - (panel_data["items_len"] + 2),
            x,
            border_style[3] + border_style[0] * (sizex - 2) + border_style[4],
            color,
        )
    except Exception:
        pass

    if base_layout.direction == VERTICAL:
        next_pos = (base_x, base_y + sizey)
    else:
        next_pos = (base_x + sizex, base_y)

    set_cursor(next_pos)


def start_floating_panel(title, position, sizex, sizey):

    maxy, maxx = screen().getmaxyx()
    sizex = get_size_value(sizex, maxx)
    sizey = get_size_value(sizey, maxy)

    if isinstance(position, tuple):
        x, y = position
        if not isinstance(x, int) and x == POSITION_CENTER_HORIZ:
            x = (maxx - sizex) / 2
        if not isinstance(y, int):
            y = (maxy - sizey) / 2
    elif position == POSITION_CENTER:
        y = (maxy - sizey) / 2
        x = (maxx - sizex) / 2
    else:
        x, y = (0, 0)

    x = round(x)
    y = round(y)

    set_cursor((x, y))

    id = get_id(f"{title}_modal_wrapper")
    add_layout(id, HORIZONTAL, (sizex, sizey), (x,y))
    push_id(id)
    return start_panel(title, sizex, sizey)

def end_floating_panel():
    end_panel()
    id = poop_id()
    layout = get_layout(id)

    if layout.direction == HORIZONTAL:
        next_pos = (layout.pos[0], layout.pos[1] + layout.size[1])
    else:
        next_pos = (layout.pos[0] + layout.size[0], layout.pos[1])

    set_cursor(next_pos)

