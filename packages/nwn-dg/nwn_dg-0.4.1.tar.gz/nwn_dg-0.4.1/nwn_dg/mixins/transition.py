"""
A transition is not a door, even if all transitions have doors.

A transition can be a cell that extends into a room or corridor, but can
also be group tiles.
"""

import itertools
import random

from boltons import iterutils

from .. import constants as C
from .path import PathMixin


class TransitionMixin(PathMixin):
    def __add_transition(self, cell, transition_type):
        # We know that there is a single cell connected to a transition
        neighbour = self.get_adjacent_cells(cell, lambda x: x and x.is_floor())[0]
        direction = self.get_direction_of_adjacent(neighbour, cell)
        cell.set_transition(transition_type, direction)

    def _make_transition_from_deadend(self, room, transition_type):
        # Find deadends that are connected to room_ids
        deadends = [i for i in self.deadends if room.identifier in i.room_identifiers]
        if not deadends:
            return False
        deadend = random.sample(deadends, 1)[0]
        self.__add_transition(deadend, transition_type)
        return True

    def _make_transition_on_room(self, room, transition_type):
        def is_single(cell):
            return len(self.get_adjacent_cells(cell, lambda x: x and x.is_floor())) == 1

        # Get all room sills, and keep only the empty ones
        cells = [x[0] for x in self.get_room_sills(room)]
        cells = [x for x in cells if x.is_empty()]

        # Filter the cells that have more than one neighbor
        cells = [x for x in cells if is_single(x)]
        if not cells:
            return False
        cell = random.sample(cells, 1)[0]
        self.__add_transition(cell, transition_type)
        cell.room_identifier = room.identifier
        return True

    def _generate_transitions(self):
        """
        Try to place the first transition on the longest path,
        and on a deadend if possible, otherwise, on the room itself
        """

        # Prioritize the rooms at the periphery of the paths
        # Then add the longest paths
        rooms = self.get_periphery()
        rooms = random.sample(rooms, len(rooms))
        rooms += itertools.chain.from_iterable(self.get_longest_paths())
        rooms = iterutils.unique(rooms)
        rooms = [x for x in self.rooms if x.identifier in rooms]

        for room in rooms:
            if self._make_transition_from_deadend(room, C.TransitionType.STAIRS_UP):
                return
            if self._make_transition_on_room(room, C.TransitionType.STAIRS_UP):
                return

        # Should statistically happen only in extreme cases
        raise SystemExit("error: failed to add an entrance to the maze")
