from math import ceil

def split_text_with_wrap(lines, sizex):
    result = []
    for line in lines:
        while len(line) > sizex:
            result.append(line[:sizex])
            line = line[sizex:]
    return result

class Percentage:
    def __init__(self, amount):
        self.amount = amount
        self.offset = 0

    def value(self, base):
        return round(self.amount / 100 * base) + self.offset

    def __add__(self, other):
        if isinstance(other, int):
            self.offset = other
            return self
        raise Exception("Percentage can only be added to int")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return self + (-other)

def get_scrolling_info(index, max_index, size, position, border_style):
    scroll_offset_index = index - position
    scroll_oversize = (max_index - size)
    scroller_size = max(1, (size - 2) - scroll_oversize)
    scroll_ratio = scroll_oversize / - (scroller_size - (size - 2))

    if scroll_offset_index == 0:
        return border_style[8]
    elif scroll_offset_index == size - 1: 
        return border_style[9]
    elif scroll_offset_index > ceil(position / scroll_ratio) and scroll_offset_index - 1 < ceil(position / scroll_ratio) + scroller_size:
        return border_style[10]

    return border_style[1]
