
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

    def value(self, base):
        return round(self.amount / 100 * base)

