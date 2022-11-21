
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
