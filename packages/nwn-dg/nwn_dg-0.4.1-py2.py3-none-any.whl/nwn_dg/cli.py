"""
Main command-line interface
"""

import argparse
import sys

from torxtools import argtools

from . import constants as C
from .dungeon import Dungeon
from .seed import Seed


def options(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="nwn-dg",
        description="Neverwinter Nights (nwn) dungeon generator",
        allow_abbrev=False,
        exit_on_error=False,
    )

    parser.add_argument("--version", action="version", version="%(prog)s 0.4.1")

    # fmt: off
    parser.add_argument("--seed", metavar="SEED", help="Initialization seed for random.seed(). If a file is passed, it's content will be used to restore state.")
    parser.add_argument("--output-seed", action=argparse.BooleanOptionalAction, default=C.DEFAULT_OUTPUT_SEED, help=f"Output the seed to a file. (default: {str(C.DEFAULT_OUTPUT_SEED).lower()})")
    parser.add_argument("--output-seed-early", action=argparse.BooleanOptionalAction, default=C.DEFAULT_OUTPUT_SEED, help=argparse.SUPPRESS)

    # map
    group = parser.add_argument_group("map")
    group.add_argument("--map-bend-pct", metavar="PCT", type=int, default=C.DEFAULT_MAP_BEND_PCT, action=argtools.is_int_between(0,100), help=f"Corridors bend this percentage of the time (0-100, default: {C.DEFAULT_MAP_BEND_PCT})")
    group.add_argument("--map-deadends-pct", metavar="PCT", type=int, default=C.DEFAULT_MAP_DEADENDS_PCT, action=argtools.is_int_between(0,100), help=f"Deadends to keep, as a percentage (0-100, default: {C.DEFAULT_MAP_DEADENDS_PCT})")
    group.add_argument("--map-height", metavar="HEIGHT", type=int, default=C.DEFAULT_MAP_HEIGHT, action=argtools.is_int_between(C.MIN_MAP_HEIGHT,C.MAX_MAP_HEIGHT), help=f"Map height (default: {C.DEFAULT_MAP_HEIGHT})")
    group.add_argument("--map-layout", metavar="LAYOUT", choices=["none", "box"], default=C.DEFAULT_MAP_LAYOUT, help='Map layout (choices: "none", "box")')
    group.add_argument("--map-layout-pct", metavar="PCT", type=int, default=C.DEFAULT_MAP_LAYOUT_PCT, action=argtools.is_int_between(10,50), help="Percentage of reserved cells. May cause generation failure. (default: {C.DEFAULT_MAP_LAYOUT_PCT})")
    group.add_argument("--map-max-rooms", metavar="NUMBER", type=int, default=C.DEFAULT_MAP_MAX_ROOMS, action=argtools.is_int_positive, help="Maximum number of rooms")
    group.add_argument("--map-min-rooms", metavar="NUMBER", type=int, default=C.DEFAULT_MAP_MIN_ROOMS, action=argtools.is_int_positive, help="Minimum number of rooms. May cause generation failure.")
    group.add_argument("--map-reshape-pct", metavar="PCT", type=int, default=C.DEFAULT_MAP_RESHAPE_PCT, action=argtools.is_int_between(0,100), help=f"Percentage of rooms to reshape (default: {C.DEFAULT_MAP_RESHAPE_PCT})")
    group.add_argument("--map-room-ratio", metavar="PCT", type=int, default=C.DEFAULT_MAP_ROOM_RATIO, action=argtools.is_int_between(1,100), help=f"Percentage of rooms to create proportionally to dimensions of map (default: {C.DEFAULT_MAP_ROOM_RATIO})")
    group.add_argument("--map-width", metavar="WIDTH", type=int, default=C.DEFAULT_MAP_WIDTH, action=argtools.is_int_between(C.MIN_MAP_WIDTH,C.MAX_MAP_WIDTH), help=f"Map width (default: {C.DEFAULT_MAP_WIDTH})")

    # png
    group = parser.add_argument_group("png")
    group.add_argument("--output-png", action=argparse.BooleanOptionalAction, default=C.DEFAULT_OUTPUT_PNG, help=f"Output a png map. (default: {str(C.DEFAULT_OUTPUT_PNG).lower()})")
    group.add_argument("--png-axes-ids", action=argparse.BooleanOptionalAction, default=C.DEFAULT_PNG_AXES_IDS, help=f"Output axes identifiers (default: {str(C.DEFAULT_PNG_AXES_IDS).lower()})")
    group.add_argument("--png-axes-base", metavar="INT", action=argtools.is_int_positive_or_zero, default=C.DEFAULT_PNG_AXES_BASE, help=f"Output axes index base (default: {C.DEFAULT_PNG_AXES_BASE})")
    group.add_argument("--png-debug", action=argparse.BooleanOptionalAction, default=C.DEFAULT_PNG_DEBUG, help=argparse.SUPPRESS)
    group.add_argument("--png-grid-size", action=argtools.is_int_positive, metavar="SIZE", type=int, default=C.DEFAULT_PNG_GRID_SIZE, help=f"Grid size, in pixels, of png map (default: {C.DEFAULT_PNG_GRID_SIZE})")
    group.add_argument("--png-room-ids", action=argparse.BooleanOptionalAction, default=C.DEFAULT_PNG_ROOM_IDS, help=f"Output room identifiers (default: {str(C.DEFAULT_PNG_ROOM_IDS).lower()})")
    group.add_argument("--png-tileset-idx", action=argparse.BooleanOptionalAction, default=C.DEFAULT_PNG_TILESET_IDX, help=f"Output NWN tileset tile indexes (default: {str(C.DEFAULT_PNG_TILESET_IDX).lower()})")

    # are
    group = parser.add_argument_group("are")
    group.add_argument("--output-are-json", action=argparse.BooleanOptionalAction, default=C.DEFAULT_OUTPUT_ARE_JSON, help=f'Output a nwn "are" json file. (default: {str(C.DEFAULT_OUTPUT_ARE_JSON).lower()})')
    group.add_argument("--output-are", action=argparse.BooleanOptionalAction, default=C.DEFAULT_OUTPUT_ARE, help=f'Output a nwn "are" file converted with `nwn_gff`. (default: {str(C.DEFAULT_OUTPUT_ARE).lower()}))')

    # json
    group = parser.add_argument_group("tile json")
    group.add_argument("--output-tile-json", action=argparse.BooleanOptionalAction, default=C.DEFAULT_OUTPUT_TILE_JSON, help=f"Output a json file suitable for SetTileJson(). (default: {str(C.DEFAULT_OUTPUT_TILE_JSON).lower()})")

    # graph tree
    group = parser.add_argument_group("graph tree")
    group.add_argument("--output-tree", action=argparse.BooleanOptionalAction, default=C.DEFAULT_OUTPUT_TREE, help=f"Output a graph of connected rooms. (default: {str(C.DEFAULT_OUTPUT_TREE).lower()})")

    # Outputs: tileset are, tile json, png, graph png
    parser.add_argument("filepath", help="Output base filepath. Extensions will be added according to output file type")
    # fmt: on

    try:
        return vars(parser.parse_args(argv))
    except argparse.ArgumentTypeError as err:
        raise SystemExit(f"error: {err}") from None


def main(argv=None):
    args = options(argv)

    seed = Seed(args)

    dg = Dungeon(args)
    dg.generate()

    seed.save()
    dg.save()
