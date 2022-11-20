from curses import wrapper, A_REVERSE, is_term_resized
from time import perf_counter

from witch.state import (
    add_layout,
    get_current_id,
    get_id,
    screen,
    load_screen,
    set_cursor,
    screen_size,
    set_screen_size,
)
from witch.widgets import text_buffer, start_menu, end_menu
from witch.layout import start_layout, end_layout, HORIZONTAL, VERTICAL
from witch.utils import Percentage


def start_frame():
    id = get_id("root")
    y, x = screen().getmaxyx()
    add_layout(id, VERTICAL, (x, y), (0, 0))
    old_x, old_y = screen_size()
    y, x = screen().getmaxyx()
    if old_x != x or old_y != y:
        set_screen_size((x, y))
        screen().clear()


def end_frame():
    if get_current_id() != "root":
        raise Exception("Stack is not clean probably missing end_layout")
    set_cursor((0, 0))
    screen().refresh()


def do_curses(astdscr):
    load_screen(astdscr)
    screen().nodelay(True)
    screen().clear()
    i = 0
    fps = 0
    start = 0
    end = 1
    try:
        while True:
            fps = 1.0 / (end - start)
            start = perf_counter()
            key = screen().getch()
            if key != -1 and chr(key) == "q":
                quit()
            screen().addstr(0, 0, f"Current mode {i} at {fps}", A_REVERSE)
            set_cursor((0,1))
            i += 1
            text = """lmkqjdfklq
qlmkdf
qldlmfjqdfqsdf
qdfqsdfqsdf
qdfqsdf"""
            start_frame()

            start_layout("leftbar", VERTICAL, Percentage(50))
            text_buffer(
                "Hello", 0, 0, Percentage(100), Percentage(100), text, status="0/3"
            )
            end_layout()

            start_menu("Menu", 0, 0, 10, Percentage(50))
            end_menu()

            text_buffer("Hello2", 0, 0, 10, 20, "haha", status="0/3")

            end_frame()
            end = perf_counter()
    except (KeyboardInterrupt, SystemExit):
        pass


def run():
    wrapper(do_curses)
