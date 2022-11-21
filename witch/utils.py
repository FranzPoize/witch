
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

    def __radd__(self, other):
        if isinstance(other, int):
            self.offset = other
            return self

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return self + (-other)

def get_scrolling_info(index, max_index, size, position):
    start = False
    in_bar = False
    end = False

    scroll_offset_index = index - position
    scroll_oversize = (max_index - size)
    scroller_size = max(1, (size - 2) - scroll_oversize)
    scroll_ratio = scroll_oversize / - (scroller_size - (size - 2))

    if scroll_offset_index == 0:
        start = True
    elif scroll_offset_index == size - 1: 
        end = True
    elif scroll_offset_index > position / scroll_ratio and scroll_offset_index - 1 < position / scroll_ratio + scroller_size:
        in_bar = True

    return (start, in_bar, end)
