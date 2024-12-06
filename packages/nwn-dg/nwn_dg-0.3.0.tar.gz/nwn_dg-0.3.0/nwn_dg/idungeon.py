import itertools

from boltons import iterutils

from . import constants as C


# pylint: disable=protected-access
class IDungeon:
    def __init__(self, dungeon):
        self._dg = dungeon

    @property
    def area(self):
        return self.height * self.width

    @property
    def args(self):
        return self._dg._args

    @property
    def cells(self):
        return self._dg._cells

    @property
    def deadends(self):
        def is_deadend(cell):
            return len(self.get_adjacent_cells(cell, lambda x: x and x.is_floor())) == 1

        cells = [cell for cell in self.loop_cells() if cell.is_primary()]
        cells = [cell for cell in cells if cell.is_corridor() or cell.is_transition()]
        cells = [cell for cell in cells if is_deadend(cell)]
        return sorted(cells)

    def get_adjacent_cell(self, cell, direction):
        x = cell.x + C.DIRECTIONS_X[direction]
        y = cell.y + C.DIRECTIONS_Y[direction]
        return self.get_cell(x, y)

    def get_adjacent_cells(self, cell, action=lambda x: x, *, with_direction=False):
        """
        If direction is True, return a tuple of (cell, direction)
        """
        retval = []
        for direction in C.DIRECTIONS:
            adj_cell = self.get_adjacent_cell(cell, direction)
            if action(adj_cell):
                if with_direction:
                    retval += [(adj_cell, direction)]
                else:
                    retval += [adj_cell]
        return retval

    def get_cell(self, x, y):
        if x < 0 or y < 0:
            return None
        if x >= self.width or y >= self.height:
            return None
        return self._dg._cells[x][y]

    def get_direction_of_adjacent(self, src, dst):
        """
        Return the direction needed for get_adjacent_cell to get
        from src to dst.
        src must be a direct neighbour
        """
        cells = self.get_adjacent_cells(src, with_direction=True)
        directions = [x[1] for x in cells if x[0] == dst]
        if len(directions) == 1:
            return directions[0]
        return None

    def get_room_cells(self, room):
        retval = []
        identifier = room.identifier
        for x, y in itertools.product(range(room.west, room.east + 1), range(room.north, room.south + 1)):
            cell = self.cells[x][y]
            if cell.is_room() and cell.room_identifier == identifier:
                retval += [cell]
        return sorted(retval)

    def get_room_sills(self, room):
        """
        Return all adjacent cells of the primary cells of the room.
        Returned as tuple (cell, direction)
        They can be empty or not
        """
        if isinstance(room, list):
            rooms = room
            retval = [self.get_room_sills(x) for x in rooms]
            retval = iterutils.unique(itertools.chain.from_iterable(retval))
            return sorted(retval)

        room_cells = self.get_room_cells(room)
        retval = [x for x in room_cells if x.is_primary()]
        # TODO: self.get_adjacent_cells with input as list
        retval = [self.get_adjacent_cells(x, with_direction=True) for x in retval]
        retval = iterutils.unique(itertools.chain.from_iterable(retval))
        retval = [x for x in retval if x[0] not in room_cells]
        return sorted(retval)

    @property
    def height(self):
        return self._dg.height

    def loop_cells(self):
        yield from (self.cells[x][y] for x, y in self.loop_xy())

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
        yield from ((x, y) for x in range(0, self.width) for y in range(0, self.height))

    @property
    def reserved(self):
        return [cell for cell in self.loop_cells() if cell.is_reserved()]

    @property
    def rooms(self):
        return self._dg._rooms

    @property
    def transitions(self):
        return sorted([cell for cell in self.loop_cells() if cell.is_transition()])

    @property
    def width(self):
        return self._dg.width
