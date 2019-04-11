__author__ = 'Omar Verduga'

class Lugar:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, l):
        if l.x == self.x and l.y == self.y:
            return 1
        else:
            return 0

