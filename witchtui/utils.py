import kalong
from witchtui.state import get_color, screen, selected_id


def create_token_list(content):
    strings = []

    if isinstance(content, tuple):
        strings.append(content)
    elif not isinstance(content, list):
        strings.append((content, "default"))
    else:
        for token in content:
            if isinstance(token, tuple):
                strings.append(token)
            else:
                strings.append((token, "default"))

    for i, token in enumerate(strings):
        if not isinstance(token[0], str):
            strings[i] = (str(token[0]), token[1])

    return strings


def get_item_color(stack_id, panel_data, items_len, name, selectable):
    if panel_data["selected_index"] == items_len and selected_id() == stack_id and selectable:
        return get_color(f"{name}_hovered")
    else:
        return get_color(f"{name}")


def print_token_list(tokens, content_len, printable_size, panel_data, items_len, selectable, stack_id, x, y):
    color_mod = panel_data["color_mod"]

    for token in tokens:
        text, color_id = token
        if content_len + len(text) > printable_size:
            text = text[: printable_size - content_len]

        color = get_item_color(stack_id, panel_data, items_len - 1, color_id, selectable)

        screen().addstr(
            y,
            x,
            text,
            color | color_mod,
        )
        x += len(text)

        content_len += len(text)

    screen().addstr(
        y,  # + 1 because we're in menu coordinates and 0 is the title line
        x,
        " " * (printable_size - content_len),
        color | color_mod,
    )
    x += printable_size - content_len

    return x, y, content_len


def split_text_with_wrap(lines, sizex):
    result = []
    for line in lines:
        while len(line) > sizex:
            result.append(line[:sizex])
            line = line[sizex:]
    return result


def get_size_value(size, base) -> int:
    if isinstance(size, Percentage):
        return round(size.amount / 100 * base) + size.offset
    else:
        return size


class Percentage:
    def __init__(self, amount):
        self.amount = amount
        self.offset = 0

    def __add__(self, other) -> "Percentage":
        if isinstance(other, int):
            self.offset = other
            return self
        raise Exception("Percentage can only be added to int")

    def __radd__(self, other) -> "Percentage":
        return self.__add__(other)

    def __sub__(self, other) -> "Percentage":
        return self + (-other)

    def __rsub__(self, other) -> "Percentage":
        return self + (-other)
