from curses import wrapper, A_REVERSE, is_term_resized
from time import perf_counter

from witch.state import (
    add_layout,
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
from witch.widgets import menu_item, text_buffer, start_menu, end_menu, menu_item
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
            start_frame()

            start_layout("leftbar", VERTICAL, Percentage(50))
            text_buffer(
                "Hello", 0, 0, Percentage(100), Percentage(50), text, status="0/3"
            )
            end_layout()

            start_menu("Menu2", 0, 0, Percentage(50), Percentage(20))
            menu_item("allo")
            menu_item("baba1")
            menu_item("baba2")
            menu_item("baba3")
            menu_item("baba4")
            menu_item("baba5")
            menu_item("baba6")
            menu_item("baba7")
            menu_item("baba8")
            menu_item("baba9")
            menu_item("baba10")
            menu_item("baba11")
            end_menu()

            start_menu("Menu", 0, 0, Percentage(50), Percentage(20))
            menu_item("allo")
            menu_item("baba1")
            menu_item("baba2")
            menu_item("baba3")
            menu_item("baba4")
            menu_item("baba5")
            menu_item("baba6")
            menu_item("baba7")
            menu_item("baba8")
            menu_item("baba9")
            menu_item("baba10")
            menu_item("baba11")
            end_menu()


            end_frame()
            end = perf_counter()
    except (KeyboardInterrupt, SystemExit):
        pass


def run():
    wrapper(do_curses)
