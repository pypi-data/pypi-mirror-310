from .dimensions import Dimensions
from .position import Position


class Room(Dimensions, Position):
    def __init__(self, width, height):
        Dimensions.__init__(self, width, height)
        Position.__init__(self)

        # Room identifier is set according to it's x,y position
        self._identifier = None

        # One cell, the middle, identifying the room
        self._cell = None

    def __repr__(self):
        retval = {
            "identifier": self.identifier,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }
        return str(retval)

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, rhs):
        self._identifier = rhs

    def loop_xy(self):
        """
        Return a tuples of (x,y) tuples with the coordinates of
        the room.
        Equivalent to:
        for x in range(0, self.width):
          for y in range(0, self.height):
            x = x + room.x
            y = y + room.y
        """
        yield from ((self.x + x, self.y + y) for x in range(0, self.width) for y in range(0, self.height))

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def set_center_cell(self, cells):
        x = self.x + self.width // 2
        y = self.y + self.height // 2
        self._cell = cells[x][y]

    @property
    def center(self):
        return self._cell

    @property
    def north(self):
        return self.y

    @property
    def east(self):
        return self.x + self.width - 1

    @property
    def west(self):
        return self.x

    @property
    def south(self):
        return self.y + self.height - 1
