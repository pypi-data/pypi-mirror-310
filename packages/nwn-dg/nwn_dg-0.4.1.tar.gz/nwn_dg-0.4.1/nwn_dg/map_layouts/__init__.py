from .. import constants as C
from ..idungeon import IDungeon
from .box import BoxLayout


class MapLayout(IDungeon):
    def __init__(self, dungeon):
        IDungeon.__init__(self, dungeon)

        if len(self.reserved):
            raise RuntimeError("error: map layout has already been generated")

        self._layout = None
        layout = self.args.get("map_layout", C.DEFAULT_MAP_LAYOUT)
        if layout == "none":
            return
        if layout == "box":
            self._layout = BoxLayout(dungeon)
            return
        raise SystemExit(f'error: unsupported layout "{layout}"') from None

    def generate(self):
        if not self._layout:
            return
        self._layout.generate()
