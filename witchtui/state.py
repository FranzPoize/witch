import curses
from typing import Literal, Optional, Union

state_selectable_ids: list[str] = []


def add_as_selectable(stack_id):
    """ Adds the item with id `stack_id` to the set of selectables items """
    state_selectable_ids.append(stack_id)


def get_selectables():
    """ Returns the list of selectable items """
    return state_selectable_ids


state_selected_id = None


def selected_id():
    """ Returns the current selected_id """ 
    return state_selected_id


def set_selected_id(stack_id):
    """ Sets the current selected_id """ 
    global state_selected_id
    state_selected_id = stack_id


def select_next():
    """ Select the next selectables in the list""" 
    global state_selected_id
    try:
        selected_index = next(
            i for i, v in enumerate(state_selectable_ids) if v == state_selected_id
        )
        state_selected_id = state_selectable_ids[
            (selected_index + 1) % len(state_selectable_ids)
        ]
    except StopIteration:
        if len(state_selectable_ids) > 0:
            state_selected_id = state_selectable_ids[0]
        else:
            pass


def select_prev():
    """ Select the previous selectables in the list""" 
    global state_selected_id
    try:
        selected_index = next(
            i for i, v in enumerate(state_selectable_ids) if v == state_selected_id
        )
        state_selected_id = state_selectable_ids[
            (selected_index - 1)
            if selected_index - 1 >= 0
            else len(state_selectable_ids) - 1
        ]
    except StopIteration:
        if len(state_selectable_ids) > 0:
            state_selected_id = state_selectable_ids[0]
        else:
            pass


state_data = {}


def add_data(stack_id, data):
    state_data[stack_id] = data
    state_data[stack_id]["touch"] = True


def get_data(id) -> Union[dict, Literal[False]]:
    if id in state_data:
        return state_data[id]

    return False


def reset_data_touch():
    global state_data
    for data in state_data:
        state_data[data]["touch"] = False


def delete_untouch_data():
    global state_data

    for data in dict(state_data):
        if not state_data[data]["touch"]:
            del state_data[data]


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
    if ord(key) in state_inputs:
        result = state_inputs[ord(key)]["pressed"]
        state_inputs[ord(key)]["pressed"] = False
    else:
        result = False
    return result


def input_buffer():
    return state_input_buffer


current_color_index = 9
colors_index = dict()
color_mods = dict()
hovered_color = None
not_hovered_color = None


def add_bg_color(not_hovered, hovered):
    global not_hovered_color
    global hovered_color

    not_hovered_color = not_hovered
    hovered_color = hovered


def add_color(name, foreground, background, mods=[]):
    global current_color_index

    curses.init_pair(current_color_index, foreground, background)
    colors_index[name] = current_color_index
    color_mods[name] = mods
    current_color_index += 1


def add_text_color(name, foreground, mods=[]):
    global current_color_index

    if not_hovered_color is None:
        raise Exception("Not hovered color is not set")

    if hovered_color is None:
        raise Exception("Hovered color is not set")

    curses.init_pair(current_color_index, foreground, not_hovered_color)
    curses.init_pair(current_color_index + 1, foreground, hovered_color)
    colors_index[name] = current_color_index
    colors_index[name + "_hovered"] = current_color_index + 1
    color_mods[name] = mods
    color_mods[name + "_hovered"] = mods + [curses.A_BOLD]
    current_color_index += 2


def get_color(name):
    mods = 0
    for mod in color_mods[name]:
        mods |= mod
    return curses.color_pair(colors_index[name]) | mods
