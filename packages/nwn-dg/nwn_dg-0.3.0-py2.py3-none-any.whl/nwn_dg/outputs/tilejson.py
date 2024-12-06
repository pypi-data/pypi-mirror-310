"""
Generate input valid for SetTileJson

https://nwnlexicon.com/index.php/SetTileJson
"""

import json

from .. import constants as C
from ..idungeon import IDungeon
from ..mixins import PathMixin


class TileJson(IDungeon, PathMixin):
    def __init__(self, dungeon, data):
        IDungeon.__init__(self, dungeon)

        self._source = data
        self._data = None
        self._output_tile_json = self.args.get("output_tile_json", C.DEFAULT_OUTPUT_TILE_JSON)

    @property
    def data(self):
        return self._data

    def save(self):
        if not self._output_tile_json:
            return

        self.generate()

        filename = self.args["filepath"] + ".tile.json"
        with open(filename, "w", encoding="UTF-8") as fd:
            fd.write(json.dumps(self._data, indent=2))

    def generate(self):
        # Avoid too much indentation
        def tile(x):
            return {"index": x[0], "tileid": x[1]["Tile_ID"]["value"], "orientation": x[1]["Tile_Orientation"]["value"]}

        # fmt: off
        self._data = {
            "version": "0.3.0",
            "tileset": self._source["Tileset"]["value"],
            "width": self.width,
            "height": self.height,
            "cells": {
                # TODO: is this too much information?
                # "rooms": [{"x": cell.x, "y": cell.y} for cell in self.loop_cells() if cell.is_room()],
                # "corridors": [{"x": cell.x, "y": cell.y} for cell in self.loop_cells() if cell.is_corridor()],
                "deadends": [{"x": cell.x, "y": cell.y, "rooms": cell.room_identifiers} for cell in self.deadends],
            },
            "transitions": {
                "stairs-up": [{"x": cell.x, "y": cell.y, "room": cell.room_identifier} for cell in self.transitions],
            },
            "rooms": {
                "periphery": self.get_periphery(),
                "rooms": [{"identifier": room.identifier, "cell": {"x": room.center.x, "y": room.center.y}} for room in self.rooms],
            },
            "paths": {
                "longest": self.get_longest_path(),
                "paths": self.get_longest_paths(),
            },
            "tiles": [tile(x) for x in zip(range(self.area), self._source["Tile_List"]["value"])],
        }
        # fmt: on
