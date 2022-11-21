from curses import start_color, wrapper, A_REVERSE, is_term_resized, initscr
from time import perf_counter

from witch.layout_state import (
    add_layout,
)

from witch.state import (
    get_current_id,
    get_id,
    get_selectables,
    input_buffer,
    is_key_pressed,
    screen,
    load_screen,
    select_next,
    selected_id,
    set_cursor,
    screen_size,
    set_screen_size,
    set_key_state,
    is_key_pressed,
    set_selected_id
)
from witch.widgets import menu_item, text_buffer, start_panel, end_panel, menu_item
from witch.layout import start_layout, end_layout, HORIZONTAL, VERTICAL
from witch.utils import Percentage


def start_frame():
    # setting up root
    id = get_id("root")
    y, x = screen().getmaxyx()
    add_layout(id, VERTICAL, (x, y), (0, 0))

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
    if get_current_id() != "root":
        raise Exception("Stack is not clean probably missing end_layout")
    set_cursor((0, 0))

    if input_buffer() == 9:
        select_next()

    screen().refresh()


def do_curses(astdscr):
    start_color()
    load_screen(astdscr)
    screen().nodelay(True)
    screen().clear()
    i = 0
    fps = 0
    start = 0
    end = 1
    test = ""
    try:
        while True:
            fps = 1.0 / (end - start)
            start = perf_counter()
            if is_key_pressed("q"):
                quit()
            screen().addstr(0, 0, f"Current mode {i} at {fps}", A_REVERSE)
            set_cursor((0,1))
            i += 1
            text = """lmkqjdfklq
qlmkdf
qldlmfjqdfqsdf
qdfqsdfqsdf
qdfqsdf"""

            text += f"\n{test}"

            start_frame()

            start_layout("leftbar", VERTICAL, Percentage(50))
            text_buffer(
                "Hello", 0, 0, Percentage(100), Percentage(100) - 1, text, status="0/3"
            )
            end_layout()

            data = []

            for i in range(100):
                data.append(f"hello {i}")

            start_panel("Menu2", 0, 0, Percentage(50), Percentage(20))
            for item in data:
                if menu_item(item):
                    test = item
            end_panel()

            start_panel("Text panel", 0, 0, Percentage(50), 30)
            end_panel()


            end_frame()
            end = perf_counter()
    except (KeyboardInterrupt, SystemExit):
        pass


def run():
    wrapper(do_curses)
