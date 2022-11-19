state_screen = None
state_data = dict()
state_ids_stack = ["root"]
state_layout = dict()
state_cursor = (0, 0)

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

def get_current_view():
    base_y, base_x = screen().getmaxyx()
    x, y = get_cursor()

    return base_x - x, base_y - y
