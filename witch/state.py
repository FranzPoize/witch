state_screen = None
state_data = dict()
state_ids_stack = ["root"]
state_layout = dict()
state_cursor = (0, 0)
state_screen_size = (0, 0)

def add_data(id, data):
    global state_data
    state_data[id] = data

def get_data(id):
    return state_data[id]

def screen_size():
    return state_screen_size

def set_screen_size(size):
    global state_screen_size
    state_screen_size = size

def get_current_id():
    return state_ids_stack[-1]

def get_id(label, seed=""):
    return seed + label

def push_id(id):
    state_ids_stack.append(id)

def get_cursor():
    return state_cursor

def set_cursor(pos):
    global state_cursor
    state_cursor = pos;

def poop_id():
    id = state_ids_stack[-1]
    state_ids_stack.pop()
    return id

def add_layout(id, direction, size, pos):
    state_layout[id] = {"direction" : direction, "size": size, "pos": pos}

def get_layout(id):
    return state_layout[id]

def load_screen(a_screen):
    global state_screen
    state_screen = a_screen

def screen():
    return state_screen

