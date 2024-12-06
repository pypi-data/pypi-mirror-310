import math

from .. import constants as C
from ..idungeon import IDungeon


class BoxLayout(IDungeon):
    def __init__(self, dungeon):
        IDungeon.__init__(self, dungeon)

    def generate(self):
        pct = self.args.get("map_layout_pct", C.DEFAULT_MAP_LAYOUT_PCT)
        pct = min(max(pct, 0), 100)

        area = (self.area * pct) // 100
        ratio = self.width / self.height

        width = max(int(math.sqrt(area * ratio)), 1)
        height = max(int(math.sqrt(area / ratio)), 1)

        x = (self.width - width) // 2
        y = (self.height - height) // 2
        x = max(min(x, self.width), 0)
        y = max(min(y, self.height), 0)

        for i in range(width + 1):
            for j in range(height + 1):
                cell = self.get_cell(x + i, y + j)
                cell.set_reserved()
