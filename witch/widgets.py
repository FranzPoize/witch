from witch.state import get_current_id, get_current_view, get_id, screen, get_cursor, get_layout
from witch.utils import Percentage, split_text_with_wrap

BASIC_BORDER = ['─', '│', '┐', '└', '┘', '┌']

def text_buffer(title, x, y, sizex, sizey, text, status='', border_style=BASIC_BORDER, wrap_lines=False):
    id = get_id(title)
    base_layout = get_layout(get_current_id())
    base_x, base_y = get_cursor()
    x += base_x
    y += base_y

    base_size_x, base_size_y = get_current_view()

    if isinstance(sizey, Percentage):
        sizey = sizey.value(base_size_y)

    if isinstance(sizex, Percentage):
        sizex = sizex.value(base_size_x)


    if len(title) > sizex - 2:
        title = title[:sizex - 2]

    if len(status) > sizex - 2:
        status = status[:sizex - 2]

    screen().addstr(y, x, BASIC_BORDER[5] + title + BASIC_BORDER[0] * (sizex - 2 - len(title)) + BASIC_BORDER[2])

    lines = text.splitlines()
    if wrap_lines:
        lines = split_text_with_wrap(lines, sizex - 2)

    startindex = max(0, len(lines) - sizey - 2)

    for i in range(1, sizey - 1):
        line_text = '' if startindex + i - 1 > len(lines) - 1 else lines[startindex + i - 1]
        if len(line_text) > sizex - 2:
            line_text = line_text[:sizex - 2]
        screen().addstr(y + i, x, BASIC_BORDER[1] + line_text + " " * (sizex - 2 - len(line_text)) + BASIC_BORDER[1])

    try:
        screen().addstr(y + sizey - 1, x, BASIC_BORDER[3] + BASIC_BORDER[0] * (sizex - 2 - len(status)) + status + BASIC_BORDER[4])
    except:
        pass
