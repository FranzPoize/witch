import curses
from curses import A_DIM, A_REVERSE, KEY_DOWN, KEY_UP
from math import ceil

from witchtui.errors import LayoutException
from witchtui.layout import HORIZONTAL, VERTICAL
from witchtui.layout_state import add_layout, get_layout
from witchtui.state import (
    add_as_selectable,
    add_data,
    get_color,
    get_current_id,
    get_cursor,
    get_data,
    get_id,
    is_key_pressed,
    poop_id,
    push_id,
    screen,
    selected_id,
    set_cursor,
    set_selected_id,
)
from witchtui.utils import (
    create_token_list,
    get_size_value,
    print_token_list,
    split_text_with_wrap,
)

BASIC_BORDER = ["─", "│", "┐", "└", "┘", "┌", "╴", "╶", "▲", "▼", "█"]

POSITION_CENTER = "pos_center"
POSITION_CENTER_HORIZ = "pos_center_horiz"
POSITION_CENTER_VERTICAL = "pos_center_vert"

SELECTION_DIRECTION_DOWN = 1
SELECTION_DIRECTION_UP = 2

# TODO: make a proper Error when we use more than the layout size


def text_buffer(
    title,
    sizex,
    sizey,
    text,
    status="",
    border_style=BASIC_BORDER,
    wrap_lines=False,
):
    stack_id = get_id(title, get_current_id())
    add_as_selectable(stack_id)
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
    except curses.error:
        pass

    layout = get_layout(get_current_id())

    if layout.direction == VERTICAL:
        next_pos = (x, y + sizey)
    else:
        next_pos = (x + sizex, y)

    set_cursor(next_pos)


def get_scrolling_border(index, max_index, size, position, border_style):
    stack_id = get_current_id()
    panel_data = get_data(stack_id)
    scroll_offset_index = index - position
    scroll_oversize = max_index - size
    scroller_size = max(1, (size - 2) - scroll_oversize)
    if scroll_oversize != 0:
        scroll_ratio = scroll_oversize / -(scroller_size - (size - 2))
    else:
        scroll_ratio = 1

    if not panel_data:
        raise LayoutException("Can't scroll outside panel")

    if panel_data["needs_scrolling"]:
        if scroll_offset_index == 0:
            return border_style[8]
        if scroll_offset_index == size - 1:
            return border_style[9]
        if (
            scroll_offset_index > ceil(position / scroll_ratio)
            and scroll_offset_index - 1 < ceil(position / scroll_ratio) + scroller_size
        ):
            return border_style[10]

    return border_style[1]


def get_border_color(stack_id):
    if selected_id() == stack_id:
        return get_color("panel_selected")
    else:
        return A_DIM

def start_same_line(border_style=BASIC_BORDER):
    stack_id = get_current_id()
    panel_data = get_data(stack_id)
    base_layout = get_layout(stack_id)
    base_layout.size = (base_layout.size[0] - 2, base_layout.size[1])
    _, sizey = base_layout.size
    x, y = get_cursor()

    if not panel_data:
        raise LayoutException("Same line not in panel")

    if panel_data["same_line_mode"]:
        raise LayoutException("Can't nest same line")

    panel_data["items_len"] += 1
    panel_data["same_line_mode"] = True
    panel_data["same_line_size"] = 0

    if (
        panel_data["items_len"] - 1 < panel_data["scroll_position"]
        or panel_data["items_len"] > panel_data["scroll_position"] + sizey - 2
    ):
        return

    border_color = get_border_color(stack_id)

    screen().addstr(
        y,  # + 1 because we're in menu coordinates and 0 is the title line
        x,
        border_style[1],
        border_color,
    )

    set_cursor((x + 1, y))


def end_same_line(border_style=BASIC_BORDER):
    stack_id = get_current_id()
    panel_data = get_data(stack_id)
    base_layout = get_layout(stack_id)
    base_layout.size = (base_layout.size[0] + 2, base_layout.size[1])
    basex, _ = base_layout.pos
    x, y = get_cursor()
    sizex, sizey = base_layout.size

    if not panel_data:
        raise LayoutException("Same line not in panel")

    panel_data["same_line_mode"] = False
    panel_data["same_line_size"] = 0

    if (
        panel_data["items_len"] - 1 < panel_data["scroll_position"]
        or panel_data["items_len"] > panel_data["scroll_position"] + sizey - 2
    ):
        return

    border_color = get_border_color(stack_id)
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
            x,
            end_border,
            border_color,
        )
    except curses.error:
        pass

    set_cursor((basex, y + 1))


def start_panel(title, sizex, sizey, start_selected=False, border_style=BASIC_BORDER):
    stack_id = get_id(title, get_current_id())
    add_as_selectable(stack_id)
    base_layout = get_layout(get_current_id())
    x, y = get_cursor()
    push_id(stack_id)

    base_size_x, base_size_y = base_layout.size

    sizey = get_size_value(sizey, base_size_y)
    sizex = get_size_value(sizex, base_size_x)

    if len(title) > sizex - 4:
        title = title[: sizex - 4]

    panel_data = get_data(stack_id)
    if not panel_data:
        if start_selected:
            set_selected_id(stack_id)
        panel_data = {
            "border_style": border_style,
            "selected_index": 0,
            "selection_direction": 0,
            "scroll_position": 0,
            "needs_scrolling": False,
            "max_items": 1,
            "same_line_mode": False,
            "items_len": 0,
            "color_mod": 0,
        }

        add_data(stack_id, panel_data)
    else:
        panel_data["touch"] = True

    panel_data["max_items"] = (
        panel_data["items_len"] if panel_data["items_len"] > 0 else 1
    )

    # Find out if we need scrolling
    if panel_data["items_len"] > sizey - 2:
        panel_data["needs_scrolling"] = True

    # Scrolling items
    if selected_id() == stack_id:
        selected_index = panel_data["selected_index"]
        if is_key_pressed(chr(KEY_UP)) or is_key_pressed("k"):
            panel_data["selection_direction"] = SELECTION_DIRECTION_UP
            panel_data["selected_index"] = selected_index - 1
        if is_key_pressed(chr(KEY_DOWN)) or is_key_pressed("j"):
            panel_data["selection_direction"] = SELECTION_DIRECTION_DOWN
            panel_data["selected_index"] = selected_index + 1

    if panel_data["selected_index"] == panel_data["items_len"]:
        panel_data["selected_index"] = 0
    if panel_data["selected_index"] == -1:
        panel_data["selected_index"] = panel_data["items_len"] - 1

    if panel_data["selected_index"] + 1 > panel_data["scroll_position"] + sizey - 2:
        panel_data["scroll_position"] += 1

    if panel_data["selected_index"] < panel_data["scroll_position"]:
        panel_data["scroll_position"] -= 1

    # Remove items
    panel_data["items_len"] = 0

    add_layout(stack_id, HORIZONTAL, (sizex, sizey), (x, y))

    color = get_border_color(stack_id)

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

    return stack_id


def text_item(content, line_sizex=None, selectable=True):
    stack_id = get_current_id()
    base_layout = get_layout(stack_id)
    basex, basey = base_layout.pos
    sizex, sizey = base_layout.size
    x, y = get_cursor()

    panel_data = get_data(stack_id)
    if not panel_data:
        raise LayoutException("Text item is not in a panel")

    # Split content for color formatting
    strings = create_token_list(content)

    border_style = panel_data["border_style"]
    scroll_position = panel_data["scroll_position"]
    same_line_mode = panel_data["same_line_mode"]
    color_mod = panel_data["color_mod"]

    if same_line_mode:
        if line_sizex is not None:
            sizex = get_size_value(line_sizex, sizex)
        else:
            sizex = sizex - panel_data["same_line_size"]
    else:
        panel_data["items_len"] += 1

    items_len = panel_data["items_len"]

    if items_len - 1 < scroll_position or items_len > scroll_position + sizey - 2:
        return False

    printable_size = sizex - 2

    if same_line_mode:
        printable_size = sizex

    border_color = get_border_color(stack_id)

    if not same_line_mode:
        screen().addstr(
            y,
            x,
            border_style[1],
            border_color,
        )
        x += 1

    content_len = 0

    x, y, content_len = print_token_list(strings, content_len, printable_size, panel_data, items_len, selectable, stack_id, x, y)

    if not same_line_mode:
        end_border = get_scrolling_border(
            items_len - 1,
            panel_data["max_items"],
            sizey - 2,
            scroll_position,
            border_style,
        )
        screen().addstr(
            y,  # + 1 because we're in menu coordinates and 0 is the title line
            x,
            end_border,
            border_color,
        )
        x += 1

    # TODO: size is not correct because - 2 is shared between all element in a same line layout

    if same_line_mode:
        set_cursor((x, y))
        panel_data["same_line_size"] += printable_size
    else:
        set_cursor((basex, y + 1))

    pressed = False

    if selected_id() == stack_id and panel_data["selected_index"] == items_len - 1:
        if selectable:
            if is_key_pressed("\n"):
                pressed = True
        # TODO: To avoid taking X frame (X is the number of unselectable item before
        # this one) we could store the number of unselectable previous item
        # and go up that much
        elif panel_data["selection_direction"] == SELECTION_DIRECTION_UP:
            panel_data["selected_index"] -= 1
        else:
            panel_data["selected_index"] += 1

    return pressed

def tree_node(title):
    layout_id = get_current_id()
    panel_data = get_data(layout_id)
    stack_id = get_id(str(title), layout_id)
    base_layout = get_layout(layout_id)
    basex, basey = base_layout.pos
    sizex, sizey = base_layout.size
    x, y = get_cursor()

    if not panel_data:
        raise LayoutException("tree_node must be in a layout")

    if panel_data["same_line_mode"]:
        raise LayoutException("Can't place tree node in same line mode")
    

    if "tree_node_opened" not in panel_data:
        panel_data["tree_node_opened"] = set()

    tree_node_opened = panel_data["tree_node_opened"]

    opened = stack_id in tree_node_opened

    if text_item(title):
        if stack_id in tree_node_opened:
            tree_node_opened.remove(stack_id)
        else:
            tree_node_opened.add(stack_id)

    return opened

def is_item_hovered():
    id = get_current_id()
    panel_data = get_data(id)

    if not panel_data:
        raise LayoutException("text_item is not in a panel")

    selected_id_value = selected_id()

    if selected_id_value is None:
        raise LayoutException("is_item_hovered needs to be placed in a panel with a least one text_item")

    if (
         selected_id_value == id
        and panel_data["selected_index"] == panel_data["items_len"] - 1
    ):
        return True


def end_panel():
    id = poop_id()
    panel_data = get_data(id)
    panel_layout = get_layout(id)
    layout_id = get_current_id()
    base_layout = get_layout(layout_id)
    sizex, sizey = panel_layout.size
    base_x, base_y = panel_layout.pos
    x, y = get_cursor()

    if not panel_data:
        raise LayoutException("No panel data in menu_item. Probably missing encircling panel")

    border_style = panel_data["border_style"]

    color = get_border_color(id)

    for i in range(0, sizey - ((panel_data["items_len"] + 2))):
        try:
            screen().addstr(
                y,
                x,
                border_style[1] + " " * (sizex - 2) + border_style[1],
                color,
            )
        except curses.error:
            pass

        y += 1

    try:
        screen().addstr(
            y,
            x,
            border_style[3] + border_style[0] * (sizex - 2) + border_style[4],
            color,
        )
    except curses.error:
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
    add_layout(id, HORIZONTAL, (sizex, sizey), (x, y))
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


def start_status_bar(id):
    id = get_id(id)
    parent_id = get_current_id()
    parent_layout = get_layout(parent_id)
    push_id(id)
    sizex, _ = parent_layout.size
    sizey = 3
    add_layout(id, HORIZONTAL, (sizex, sizey), parent_layout.pos)

    panel_data = get_data(id)
    if not panel_data:
        panel_data = {
            "border_style": [],
            "selected_index": 0,
            "selection_direction": 0,
            "scroll_position": 0,
            "needs_scrolling": False,
            "max_items": 1,
            "same_line_mode": False,
            "items_len": 1,
            "color_mod": A_REVERSE,
            "same_line_mode": True,
            "same_line_size": 0,
        }

        add_data(id, panel_data)
    else:
        panel_data["touch"] = True


def end_status_bar():
    id = poop_id()
    panel_data = get_data(id)
    layout = get_layout(id)
    basex, _ = layout.pos
    sizex, _ = layout.size
    x, y = get_cursor()
    try:
        screen().addstr(y, x, " " * (x - basex + sizex), panel_data["color_mod"])
    except curses.error:
        pass

    set_cursor((x, y + 1))
