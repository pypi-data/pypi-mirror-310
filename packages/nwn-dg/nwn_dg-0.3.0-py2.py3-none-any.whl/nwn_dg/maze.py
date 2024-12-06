"""
A sparse dungeon generates the rooms and corridors only on odd cells (on even numbers when 0-based)

Other online dungeon generators that use this method: https://donjon.bin.sh/d20/dungeon/ or https://www.d20srd.org/d20/dungeon/index.cgi

It's fine for most usage, but has the inconvenient of more "wasted" space in Neverwinter Nights.
"""

from . import constants as C
from .idungeon import IDungeon
from .mixins import DeadendMixin, ReshapeMixin, TransitionMixin, TunnelMixin


class Maze(IDungeon, TunnelMixin, DeadendMixin, ReshapeMixin, TransitionMixin):
    def __init__(self, dungeon):
        IDungeon.__init__(self, dungeon)
        TunnelMixin.__init__(self)
        DeadendMixin.__init__(self)
        ReshapeMixin.__init__(self)
        TransitionMixin.__init__(self)

        if not (self.width & 1 and self.height & 1):
            raise SystemExit("error: dungeon width and height must be odd numbers")
        if self.width < C.MIN_MAP_WIDTH or self.height < C.MIN_MAP_HEIGHT:
            raise RuntimeError(f"error: dungeon width and height must be at least {C.MIN_MAP_WIDTH}x{C.MIN_MAP_HEIGHT}")
        if len(self.rooms) < C.DEFAULT_MAP_MIN_ROOMS:
            raise RuntimeError("error: not enough rooms have been generated")

        # TODO: find a way to detect if this was already run: if everything is connected and room.count > 1?
        # if a corridor exists, it's already generated, unless there's a single room, which shouldn't be possible

    def generate(self):
        # Cells that need to be tunneled.
        self._tunnel_sills()

        # Deadends list are possible deadends, not necessarily deadends
        self._tunnel_cells()

        # Some rooms might not be reachable, open new tunnels
        self._tunnel_connect()

        # Remove deadends
        self._remove_deadends()

        # Update deadends to add room numbers
        self._update_deadends()

        # Reshape some rooms
        self._reshape_rooms()

        # Reshape some rooms
        self._generate_transitions()
