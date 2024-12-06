from .. import constants as C
from .position import Position

K_KEYS = {
    C.FloorType.CORRIDOR: "C",
    C.FloorType.ROOM: "R",
    C.FloorType.TRANSITION: "C",
}


class Cell(Position):
    def __init__(self, x, y, index=None):
        Position.__init__(self, x, y)

        # The NWN tile index
        self._index = index

        # Cell favored direction, used when tunneling
        self._direction = None

        # All cells start as empty, and are then filled
        self._floor_type = C.FloorType.EMPTY

        # Room identifier is set once for rooms,
        # For deadends, it holds a list of room identifiers
        self._room_identifier = None
        self._room_identifiers = None

        self._transition_type = C.TransitionType.NONE

    def __repr__(self):
        retval = {
            "x": self.x,
            "y": self.y,
            "index": self.index,
            "direction": self.direction,
            "type": self._floor_type,
        }
        return str(retval)

    def clear(self):
        self._room_identifier = None
        self._room_identifiers = None
        self._floor_type = C.FloorType.EMPTY
        self._transition_type = C.TransitionType.NONE
        self._direction = None

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, rhs):
        self._direction = rhs

    @property
    def index(self):
        return self._index

    def is_corridor(self):
        return self._floor_type == C.FloorType.CORRIDOR

    def is_empty(self):
        return self._floor_type not in [
            C.FloorType.ROOM,
            C.FloorType.CORRIDOR,
            C.FloorType.RESERVED,
            C.FloorType.TRANSITION,
        ]

    def is_floor(self):
        return self._floor_type in [C.FloorType.CORRIDOR, C.FloorType.ROOM, C.FloorType.TRANSITION]

    def is_primary(self):
        return (self.x & 1 == 0) and (self.y & 1 == 0)

    def is_reserved(self):
        return self._floor_type == C.FloorType.RESERVED

    def is_room(self):
        return self._floor_type == C.FloorType.ROOM

    def is_transition(self):
        return self._floor_type == C.FloorType.TRANSITION

    @property
    def key(self):
        return K_KEYS.get(self._floor_type, "W")

    @property
    def room_identifier(self):
        return self._room_identifier

    @room_identifier.setter
    def room_identifier(self, rhs):
        self._room_identifier = rhs

    @property
    def room_identifiers(self):
        return self._room_identifiers

    @room_identifiers.setter
    def room_identifiers(self, rhs):
        self._room_identifiers = rhs

    def set_corridor(self, direction=None):
        self._floor_type = C.FloorType.CORRIDOR
        self._direction = direction

    def set_room(self, identifier):
        self._room_identifier = identifier
        self._floor_type = C.FloorType.ROOM

    def set_reserved(self):
        self._floor_type = C.FloorType.RESERVED
        self._direction = None

    def set_transition(self, transition, direction):
        self._floor_type = C.FloorType.TRANSITION
        self._transition_type = transition
        self._direction = direction

    @property
    def transition_type(self):
        return self._transition_type
