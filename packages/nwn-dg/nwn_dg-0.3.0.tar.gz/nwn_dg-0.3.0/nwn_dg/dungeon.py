from .classes import Cell, Dimensions
from .idungeon import IDungeon
from .map_layouts import MapLayout
from .maze import Maze
from .outputs import MapPNG, TileJson, Tileset, Tree
from .room_layouts import RoomLayout


class Dungeon(Dimensions, IDungeon):
    def __init__(self, args):
        def index(x, y):
            return (self.height - y - 1) * self.width + x

        IDungeon.__init__(self, self)
        Dimensions.__init__(self, args["map_width"], args["map_height"])

        # Keep a copy of arguments
        self._args = args

        # Have a minimum of global variables: cells and rooms
        #
        # Create the map cells
        self._cells = [[Cell(x, y, index(x, y)) for y in range(self.height)] for x in range(self.width)]

        # List of rooms
        self._rooms = []

    def generate(self):
        self.generate_map_layout()
        self.generate_rooms()
        self.generate_maze()

    def save(self):
        MapPNG(self).save()
        Tree(self).save()

        tileset = Tileset(self)
        tileset.save()
        TileJson(self, tileset.data).save()

    def generate_map_layout(self):
        layout = MapLayout(self)
        layout.generate()

    def generate_rooms(self):
        layout = RoomLayout(self)
        layout.generate()

    def generate_maze(self):
        Maze(self).generate()
