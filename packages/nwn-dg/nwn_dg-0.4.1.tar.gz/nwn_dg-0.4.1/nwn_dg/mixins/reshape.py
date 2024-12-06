import random

from .. import constants as C


class ReshapeMixin:
    def _reshape_rooms(self):
        """
        For every room, check every adjacent cell on every border.
        If the sills are clear, we can remove a full border of a room
        """
        map_reshape_pct = self.args.get("map_reshape_pct", C.DEFAULT_MAP_RESHAPE_PCT)
        if not map_reshape_pct:
            return

        rooms = random.sample(self.rooms, len(self.rooms))
        for room in rooms:
            # To remove a row or column from a room we need
            # to have as many sills as half the length, plus the two corners
            h_req_free = 2 + (room.width + 1) // 2
            v_req_free = 2 + (room.height + 1) // 2

            # Get the sills, then sort into the ones on the north,
            # the east, the south and the west
            sills = [x[0] for x in self.get_room_sills(room) if x[0].is_empty()]
            n_sills = [sill for sill in sills if sill.y <= room.north]
            e_sills = [sill for sill in sills if sill.x >= room.east]
            s_sills = [sill for sill in sills if sill.y >= room.south]
            w_sills = [sill for sill in sills if sill.x <= room.west]

            directions = []
            if len(n_sills) >= h_req_free:
                directions += [C.Directions.NORTH]
            if len(e_sills) >= v_req_free:
                directions += [C.Directions.EAST]
            if len(s_sills) >= h_req_free:
                directions += [C.Directions.SOUTH]
            if len(w_sills) >= v_req_free:
                directions += [C.Directions.WEST]
            if not directions:
                continue

            # We don't change the size of the room object as it's
            # no longer used.
            random.shuffle(directions)
            for direction in directions:
                # pylint: disable=superfluous-parens
                if not (random.randint(1, 100) <= map_reshape_pct):
                    continue
                if direction == C.Directions.NORTH:
                    for x in range(room.west, room.east + 1):
                        self.cells[x][room.north].clear()
                if direction == C.Directions.EAST:
                    for y in range(room.north, room.south + 1):
                        self.cells[room.east][y].clear()
                if direction == C.Directions.SOUTH:
                    for x in range(room.west, room.east + 1):
                        self.cells[x][room.south].clear()
                if direction == C.Directions.WEST:
                    for y in range(room.north, room.south + 1):
                        self.cells[room.west][y].clear()
