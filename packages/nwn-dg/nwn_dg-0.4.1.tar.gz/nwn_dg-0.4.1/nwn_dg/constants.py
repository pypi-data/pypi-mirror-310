from enum import Enum, Flag, IntEnum, auto, unique

DEFAULT_OUTPUT_SEED = False
DEFAULT_OUTPUT_ARE = False
DEFAULT_OUTPUT_ARE_JSON = True
DEFAULT_OUTPUT_PNG = True
DEFAULT_OUTPUT_TILE_JSON = False
DEFAULT_OUTPUT_TREE = False

DEFAULT_MAP_BEND_PCT = 50
DEFAULT_MAP_DEADENDS_PCT = 50
DEFAULT_MAP_HEIGHT = 17
DEFAULT_MAP_LAYOUT = "none"
DEFAULT_MAP_LAYOUT_PCT = 40
DEFAULT_MAP_MAX_ROOMS = None
DEFAULT_MAP_MIN_ROOMS = 1
DEFAULT_MAP_RESHAPE_PCT = 70
DEFAULT_MAP_ROOM_RATIO = 100
DEFAULT_MAP_WIDTH = DEFAULT_MAP_HEIGHT

DEFAULT_PNG_AXES_IDS = False
DEFAULT_PNG_AXES_BASE = 1
DEFAULT_PNG_DEBUG = False
DEFAULT_PNG_GRID_SIZE = 25
DEFAULT_PNG_ROOM_IDS = True
DEFAULT_PNG_TILESET_IDX = False

MAX_MAP_HEIGHT = 31
MAX_MAP_WIDTH = 31

MIN_MAP_HEIGHT = 5
MIN_MAP_WIDTH = 5


@unique
class FloorType(Enum):
    EMPTY = 0
    ROOM = 1
    CORRIDOR = 2
    RESERVED = 3
    TRANSITION = 4


@unique
class TransitionType(Enum):
    NONE = 0
    FLAT = 1
    STAIRS_UP = 2
    STAIRS_DOWN = 3


@unique
class Directions(IntEnum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4


class WalkAction(Flag):
    RETURN = auto()
    CONTINUE = auto()
    #
    OPEN_CELL = auto()
    CLOSE_CELL = auto()


ORIENTATION = {Directions.NORTH: 0, Directions.WEST: 1, Directions.SOUTH: 2, Directions.EAST: 3}
OPPOSITE_DIRECTION = {
    Directions.NORTH: Directions.SOUTH,
    Directions.SOUTH: Directions.NORTH,
    Directions.EAST: Directions.WEST,
    Directions.WEST: Directions.EAST,
}
DIRECTIONS_X = {Directions.NORTH: 0, Directions.SOUTH: 0, Directions.EAST: 1, Directions.WEST: -1}
DIRECTIONS_Y = {Directions.NORTH: -1, Directions.SOUTH: 1, Directions.EAST: 0, Directions.WEST: 0}
DIRECTIONS = (Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST)
