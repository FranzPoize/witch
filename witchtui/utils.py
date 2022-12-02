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
