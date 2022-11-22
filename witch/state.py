import curses
from typing import Literal, Optional, Union

state_selectable_ids: list[str] = [] 

def add_as_selectable(id):
    global state_selectable_ids
    state_selectable_ids.append(id)

def get_selectables():
    return state_selectable_ids

state_selected_id = None

def selected_id():
    return state_selected_id

def set_selected_id(id):
    global state_selected_id
    state_selected_id = id

def select_next():
    global state_selected_id
    try:
        selected_index = next(i for i, v in enumerate(state_selectable_ids) if v == state_selected_id)
        state_selected_id = state_selectable_ids[(selected_index + 1) % len(state_selectable_ids)]
    except StopIteration:
        if len(state_selectable_ids) > 0:
            state_selected_id = state_selectable_ids[0]
        else:
            pass

state_data = dict()

def add_data(id, data):
    global state_data
    state_data[id] = data


def get_data(id) -> Union[dict, Literal[False]]:
    if id in state_data:
        return state_data[id]
    else:
        return False

state_screen_size = (0, 0)

def screen_size():
    return state_screen_size


def set_screen_size(size):
    global state_screen_size
    state_screen_size = size

state_ids_stack = ["root"]

def get_current_id():
    return state_ids_stack[-1]


def get_id(label, seed=""):
    return seed + label


def push_id(id):
    state_ids_stack.append(id)

state_cursor = (0, 0)

def get_cursor():
    return state_cursor


def set_cursor(pos):
    global state_cursor
    state_cursor = pos


def poop_id():
    id = state_ids_stack[-1]
    state_ids_stack.pop()
    return id

state_screen: Optional["curses._CursesWindow"] = None

def load_screen(a_screen):
    global state_screen
    state_screen = a_screen


def screen() -> "curses._CursesWindow":
    if state_screen is None:
        raise Exception("Curse window has not been loaded")
    return state_screen


state_inputs = dict()
state_input_buffer = ""


def set_key_state(key):
    global state_inputs
    global state_input_buffer
    state_inputs = dict()
    state_inputs[key] = {
        "pressed": True,
    }
    state_input_buffer = key

def get_key_state(key):
    return False if key not in state_inputs else state_inputs[ord(key)]

def is_key_pressed(key):
    return False if ord(key) not in state_inputs else state_inputs[ord(key)]["pressed"]

def input_buffer():
    return state_input_buffer
