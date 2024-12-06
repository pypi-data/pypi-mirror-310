import math
import random

from boltons import iterutils

from .. import constants as C


class TunnelMixin:
    def __init__(self):
        # How often to bend a corridor?
        self.__map_bend_pct = self.args.get("map_bend_pct", C.DEFAULT_MAP_BEND_PCT)

        # List of cells to tunnel
        self.__open_cells = []

        # We keep a list of identifiers that have been explored,
        # and that will tend to 1
        self.__cell_id = [[self.get_cell(x, y).room_identifier for y in range(self.height)] for x in range(self.width)]

    def __add_open_cell(self, cell):
        """
        Add a cell to be tunneled
        """
        self.__open_cells += [cell]

    def __get_open_cell(self):
        # Sorting enables keeping the random generation the same after
        # making list unique
        self.__open_cells = sorted(iterutils.unique(self.__open_cells))
        random.shuffle(self.__open_cells)
        return self.__open_cells.pop(0)

    def __get_cell_id(self, cell):
        return self.__cell_id[cell.x][cell.y]

    def __set_cell_id(self, dst, src):
        if not isinstance(src, int):
            src = self.__cell_id[src.x][src.y]
        self.__cell_id[dst.x][dst.y] = src

    def __get_cells_by_id(self, needle):
        return [self.get_cell(x, y) for x, y in self.loop_xy() if self.__cell_id[x][y] in needle]

    def _tunnel_sills(self):
        """
        Sills are corridors that open from a room into the dungeon.
        They're placed on every other cell, and have
        one or two possible directions (ie: corners)

        Opened sills are added to open_cells for tunneling
        """

        def get_openings_count(room):
            room_h = int((room.height // 2) + 1)
            room_w = int((room.width // 2) + 1)
            return max(int(math.sqrt(room_h * room_w)), 1)

        # ---
        # For every room, build a list of sills
        # Open a random amount of sills per room, never opening or considering
        # a sill from another room (even if not opened)
        # By randomizing the rooms, that are already in order, we reduce some
        # possible friction between sills
        sills = []
        rooms = random.sample(self.rooms, len(self.rooms))
        for room in rooms:
            room_sills = [x for x in self.get_room_sills(room) if x[0] not in sills]
            sills += [x[0] for x in room_sills]

            # n_opens can be 0 because len(sills) is 0, which means room will probably end up
            # unaccessible. room will be opened later when fixing unaccessible rooms
            n_opens = get_openings_count(room)
            n_opens = min(n_opens, len(room_sills))

            cells = random.sample(room_sills, n_opens)
            for item in cells:
                cell2 = item[0]
                cell2.direction = item[1]

                cell1 = self.get_adjacent_cell(cell2, C.OPPOSITE_DIRECTION[cell2.direction])
                self.__tunnel_cell(cell1, cell2.direction, True)

    def __tunnel_cell(self, cell1, direction, open_room=False):
        def set_corridors(direction, cell1, cell2, cell3=None):
            self.__add_open_cell(cell1)
            self.__set_cell_id(cell2, cell1)
            cell2.set_corridor()
            if cell3:
                self.__set_cell_id(cell3, cell1)
                cell3.set_corridor(direction)
                self.__add_open_cell(cell3)

        cell2 = self.get_adjacent_cell(cell1, direction)
        if cell2 is None or not cell2.is_empty():
            return C.WalkAction.CONTINUE

        cell3 = self.get_adjacent_cell(cell2, direction)
        if cell3 is None:
            return C.WalkAction.CONTINUE
        # If we land on an empty space, then it's OK
        if cell3.is_empty():
            set_corridors(direction, cell1, cell2, cell3)
            return C.WalkAction.RETURN
        if cell3.is_corridor() or (open_room and cell3.is_room()):
            id1 = self.__get_cell_id(cell1)
            id3 = self.__get_cell_id(cell3)
            if id1 == id3:
                return C.WalkAction.CONTINUE

            if cell3.is_corridor():
                set_corridors(direction, cell1, cell2, cell3)
            else:
                set_corridors(direction, cell1, cell2)
            self.__minimize_identifiers([id1, id3])
            return C.WalkAction.RETURN
        return C.WalkAction.CONTINUE

    def __tunnel_random_cell(self, cell, open_room=False):
        """
        If open_room is True, then we can tunnel into a room and open
        a new sill
        """

        def get_random_directions(last_dir=None):
            """
            Return all four directions, with a priority on the last
            direction the cell was
            """
            retval = list(C.DIRECTIONS)
            random.shuffle(retval)
            if not (random.randint(1, 100) <= self.__map_bend_pct) and last_dir:
                retval.insert(0, last_dir)
            return retval

        # ---
        directions = get_random_directions(cell.direction)
        for direction in directions:
            action = self.__tunnel_cell(cell, direction, open_room)
            if action == C.WalkAction.CONTINUE:
                continue
            if action == C.WalkAction.RETURN:
                return

    def _tunnel_cells(self):
        while self.__open_cells:
            cell = self.__get_open_cell()
            self.__tunnel_random_cell(cell)

    def _tunnel_connect(self):
        # def get_cells(cells):
        room_ids = list(range(2, len(self.rooms) + 1))

        cells = self.__get_cells_by_id(room_ids)
        if not cells:
            return

        # Reduce to every other cell to keep corridors aligned
        cells = [cell for cell in cells if cell.is_primary()]

        # Until all cells have an identifier of None or 1,
        # randomly open the cells one by one, especially into other
        # corridors and other rooms
        while cells:
            cell = random.sample(cells, 1)[0]
            self.__tunnel_random_cell(cell, True)
            cells = [cell for cell in cells if self.__get_cell_id(cell) not in [None, 1]]

    def __minimize_identifiers(self, identifiers):
        """
        Loop through all the cells.
        If the identifier is in the param "identifier" list,
        then set the identifier to the smallest value from that list

        When all cell identifiers are None or 1, then the map is all
        connected.
        """
        min_id = min(identifiers)

        cells = self.__get_cells_by_id(identifiers)
        for cell in cells:
            self.__set_cell_id(cell, min_id)
