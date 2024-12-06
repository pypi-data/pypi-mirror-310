from .. import constants as C
from ..idungeon import IDungeon
from .scattered import ScatteredLayout


class RoomLayout(IDungeon):
    def __init__(self, dungeon):
        IDungeon.__init__(self, dungeon)

        if len(self.rooms):
            raise RuntimeError("error: rooms has already been generated")

        self._layout = ScatteredLayout(dungeon)

    def generate(self):
        if not self._layout:
            return
        self._layout.generate()
