from curses import (
    A_BOLD,
    A_DIM,
    A_REVERSE,
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_MAGENTA,
    COLOR_WHITE,
    start_color,
    wrapper,
)
from itertools import accumulate
from time import perf_counter

from witchtui.errors import LayoutException, WitchException, WrappingCurseException
from witchtui.layout import HORIZONTAL, VERTICAL, end_layout, start_layout
from witchtui.layout_state import add_layout
from witchtui.state import (
    add_bg_color,
    add_color,
    add_text_color,
    delete_untouch_data,
    get_current_id,
    get_id,
    get_selectables,
    input_buffer,
    is_key_pressed,
    load_screen,
    reset_data_touch,
    screen,
    screen_size,
    select_next,
    selected_id,
    set_selected_id,
    select_prev,
    set_cursor,
    set_key_state,
    set_screen_size,
)
from witchtui.utils import Percentage
from witchtui.widgets import (
    is_item_hovered,
    tree_node,
    end_panel,
    end_same_line,
    start_panel,
    start_same_line,
    text_buffer,
    text_item,
    start_floating_panel,
    end_floating_panel,
    start_status_bar,
    end_status_bar,
)


def witch_init(init_screen):
    """Init a curses window for witchtui

    Parameters
    ----------
    init_screen: a curses window object
    """
    start_color()
    init_screen.nodelay(True)
    init_screen.clear()
    load_screen(init_screen)
    add_color("panel_selected", COLOR_GREEN, COLOR_BLACK, [A_BOLD])
    add_bg_color(COLOR_BLACK, COLOR_BLUE)
    add_text_color("default", COLOR_WHITE, [A_DIM])


def start_frame():
    """Starts a witchtui frame

    Example
    -------
    while(True):
        start_frame()
        text_item()
        end_frame()
    """
    # setting up root
    id = get_id("root")
    y, x = screen().getmaxyx()
    add_layout(id, VERTICAL, (x, y), (0, 0))

    # reset data touch status
    reset_data_touch()

    # handle screen resize
    old_x, old_y = screen_size()
    y, x = screen().getmaxyx()
    if old_x != x or old_y != y:
        set_screen_size((x, y))
        screen().clear()

    # capture input
    set_key_state(screen().getch())

    # clear selectables pre frame
    get_selectables().clear()


def end_frame():
    """Ends a witchtui frame

    Example
    -------
    while(True):
        start_frame()
        text_item()
        end_frame()
    """
    if get_current_id() != "root":
        raise Exception("Stack is not clean probably missing end_layout")
    set_cursor((0, 0))

    delete_untouch_data()

    if input_buffer() == 9:
        select_next()

    if input_buffer() == 353:
        select_prev()

    screen().refresh()
