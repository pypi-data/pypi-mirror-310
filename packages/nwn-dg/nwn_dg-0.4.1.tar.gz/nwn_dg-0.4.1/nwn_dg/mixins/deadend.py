import random

from .. import constants as C


class DeadendMixin:
    def _remove_deadends(self):
        deadends = self.deadends
        if not self.deadends:
            return

        map_deadends_pct = self.args.get("map_deadends_pct", C.DEFAULT_MAP_DEADENDS_PCT)
        pct = map_deadends_pct / 100
        k = int(len(self.deadends) * (1.0 - min(max(float(pct), 0.0), 1.0)))
        k = min(max(0, k), len(self.deadends))
        deadends = random.sample(self.deadends, k)

        while deadends:
            cell = deadends.pop(0)
            exits = [i for i in self.get_adjacent_cells(cell) if i.is_floor()]
            if len(exits) == 1:
                cell.clear()
                deadends += exits

    def _update_deadends(self):
        for deadend in self.deadends:
            deadend.room_identifiers = self.get_connected_rooms(deadend)
