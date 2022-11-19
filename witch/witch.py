from curses import wrapper, initscr, A_REVERSE
import os
from time import perf_counter

from witch.state import add_layout, get_current_id, get_id, screen, load_screen, set_cursor
from witch.widgets import text_buffer
from witch.layout import start_layout, end_layout, HORIZONTAL, VERTICAL
from witch.utils import Percentage

def start_frame():
    id = get_id("root")
    add_layout(id, VERTICAL, Percentage(100), (0, 0))

def end_frame():
    if get_current_id() != "root":
        raise Exception("Stack is not clean probably missing end_layout")
    set_cursor((0,0))
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
            i += 1
            text = '''lmkqjdfklq
qlmkdf
qldlmfjqdfqsdf
qdfqsdfqsdf
qdfqsdf'''
            start_frame()

            start_layout("leftbar", VERTICAL, Percentage(50))
            text_buffer("Hello", 0, 0, Percentage(100), Percentage(100), text, status="0/3")
            end_layout()

            text_buffer("Hello2", 0, 0, 10, 20, "haha", status="0/3")

            end_frame()
            end = perf_counter()
    except (KeyboardInterrupt, SystemExit):
        pass

def run():
    wrapper(do_curses)


