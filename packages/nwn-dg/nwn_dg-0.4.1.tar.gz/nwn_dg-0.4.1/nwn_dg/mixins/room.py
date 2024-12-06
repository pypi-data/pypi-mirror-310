# pylint: disable=protected-access
class RoomMixin:
    def add_room(self, room):
        """
        Add room to map if it does not overlap with anything
        Return True if added
        """

        def _set_room(room, identifier):
            # For every cell contained by this room, set the identifier
            room.identifier = identifier
            room.set_center_cell(self.cells)
            for x, y in room.loop_xy():
                cell = self.cells[x][y]
                cell.set_room(identifier)

        # Verify placement
        for x, y in room.loop_xy():
            cell = self.cells[x][y]
            if not cell.is_empty():
                return False

        self._dg._rooms += [room]

        # Reorder all rooms
        self._dg._rooms = sorted(self.rooms)
        for index, j in zip(range(len(self.rooms)), self.rooms):
            _set_room(j, index + 1)
        return True
