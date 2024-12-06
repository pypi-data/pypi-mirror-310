import tempfile

# pylint: disable=no-name-in-module
import cairo
from cairo import FONT_SLANT_NORMAL, FONT_WEIGHT_BOLD, FONT_WEIGHT_NORMAL, Context, SVGSurface

from .. import constants as C
from ..idungeon import IDungeon

OFFSET = 1


class MapPNG(IDungeon):
    def __init__(self, dungeon):
        IDungeon.__init__(self, dungeon)

        self._context = None
        self._grid_size = self.args.get("png_grid_size", C.DEFAULT_PNG_GRID_SIZE)

        self._output_png = self.args.get("output_png", C.DEFAULT_OUTPUT_PNG)

    def save(self):
        if not self._output_png:
            return

        filename = self.args["filepath"] + ".png"
        with tempfile.NamedTemporaryFile(suffix=".svg") as tmpfile:
            surface = SVGSurface(
                tmpfile.name,
                (self.width + OFFSET * 2) * self._grid_size,
                (self.height + OFFSET * 2) * self._grid_size,
            )
            self._context = Context(surface)
            self._context.set_antialias(cairo.Antialias.GRAY)
            self._set_line_width(1)
            self._generate()

            self._context.save()

            surface.write_to_png(filename)
            surface.finish()

    def _generate(self):
        self._draw_background()
        self._draw_foreground()
        self._draw_grid()
        self._draw_floor()
        self._draw_transitions()

        self._draw_room_ids()
        self._draw_axes_ids()
        self._draw_tileset_idx()
        self._draw_debug()

    def _draw_background(self):
        # Draw a full black background
        self._context.set_source_rgb(0, 0, 0)
        self._context.paint()

    def _draw_foreground(self):
        # Draw a full black background
        self._context.set_source_rgb(1, 1, 1)
        self._rectangle(0, 0, self.width, self.height)
        self._context.fill()
        self._context.stroke()

    def _draw_grid(self):
        # Draw gray grid lines, by skipping first and last lines
        self._context.set_line_width(1.0)
        self._context.set_source_rgb(0.5, 0.5, 0.5)
        for x in range(self.width + 1):
            if x in [0, self.width]:
                continue
            self._line(x, 0, 0, self.height)
            self._context.stroke()
        for y in range(self.height + 1):
            if y in [0, self.height]:
                continue
            self._line(0, y, self.width, 0)
            self._context.stroke()

    def _draw_floor(self):
        # Blacken every empty cell
        self._context.set_source_rgb(0, 0, 0)

        for x, y in self.loop_xy():
            cell = self.cells[x][y]
            if cell.is_floor():
                continue
            self._rectangle(x, y, 1, 1)
            self._context.fill()
            self._context.stroke()

    def _draw_stairs_up(self, cell):
        ctx = self._context

        ctx.set_source_rgb(0.7, 0.7, 0.7)
        self._rectangle(cell.x, cell.y, 1, 1)
        ctx.fill()

        ctx.set_source_rgb(0, 0, 0)
        ctx.set_antialias(cairo.Antialias.NONE)
        self._set_line_width(2)

        self._line(*self._rotate(cell, 0.1, 0.7, 0.8, 0.0))
        self._line(*self._rotate(cell, 0.2, 0.5, 0.6, 0.0))
        self._line(*self._rotate(cell, 0.3, 0.3, 0.4, 0.0))
        self._line(*self._rotate(cell, 0.4, 0.1, 0.2, 0.0))
        ctx.stroke()

        self._set_line_width(2.5)
        self._line(*self._rotate(cell, 0.0, 1.0, 1.0, 0.0))
        ctx.stroke()

        self._draw_door(cell)

    def _draw_door(self, cell):
        ctx = self._context

        ctx.set_antialias(cairo.Antialias.NONE)
        self._set_line_width(2)

        height = 0.3
        if cell.direction in [C.Directions.SOUTH, C.Directions.EAST]:
            height *= -1

        ctx.set_source_rgb(1, 1, 1)
        self._rectangle(*self._rotate(cell, 0.3, 0.85, 0.4, height))
        ctx.fill()
        ctx.set_source_rgb(0, 0, 0)
        self._rectangle(*self._rotate(cell, 0.3, 0.85, 0.4, height))
        ctx.stroke()

        # Restore settings
        ctx.set_antialias(cairo.Antialias.GRAY)
        self._set_line_width(1)

    def _draw_transition(self, cell):
        if cell.transition_type == C.TransitionType.STAIRS_UP:
            self._draw_stairs_up(cell)

    def _draw_transitions(self):
        cells = self.transitions

        for cell in cells:
            self._draw_transition(cell)

    def _draw_room_ids(self):
        result = self.args.get("png_room_ids", C.DEFAULT_PNG_ROOM_IDS)
        if not result:
            return

        ctx = self._context
        gs = self._grid_size

        ctx.set_source_rgb(0, 0, 1)
        self._set_font(16, FONT_WEIGHT_BOLD)
        for room in self.rooms:
            identifier = str(room.identifier)
            x = room.center.x + 0.3 + OFFSET
            if len(str(identifier)) >= 2:
                x -= 0.2
            y = room.center.y + 0.8 + OFFSET
            self._context.move_to(x * gs, y * gs)
            self._context.show_text(identifier)
            self._context.stroke()

    def _draw_axes_ids(self):
        # Print axes horizontal and vertical headers
        result = self.args.get("png_axes_ids", C.DEFAULT_PNG_AXES_IDS)
        if not result:
            return

        index = self.args.get("png_axes_base", C.DEFAULT_PNG_AXES_BASE)

        ctx = self._context
        gs = self._grid_size

        ctx.set_source_rgb(1, 0, 0)
        self._set_font(10, FONT_WEIGHT_NORMAL)
        for x in range(self.width):
            ctx.move_to((x + 0.3 + OFFSET) * gs, 0.7 * gs)
            ctx.show_text(str(x + index))
        for y in range(self.width):
            ctx.move_to(0.2 * gs, (y + 0.5 + OFFSET) * gs)
            ctx.show_text(str(y + index))

    def _draw_tileset_idx(self):
        # Print nwn tile index
        result = self.args.get("png_tileset_idx", C.DEFAULT_PNG_TILESET_IDX)
        if not result:
            return

        ctx = self._context
        gs = self._grid_size

        ctx.set_source_rgb(1, 0, 1)
        self._set_font(12, FONT_WEIGHT_NORMAL)

        for y in range(self.height, 0, -1):
            y -= 1
            for x in range(self.width):
                cell = self.cells[x][y]
                if cell.is_floor():
                    ctx.move_to((x + 0.1 + OFFSET) * gs, (y + 0.6 + OFFSET) * gs)
                    ctx.show_text(str(cell.index))

    def _draw_debug(self):
        # Print axes horizontal and vertical headers
        result = self.args.get("png_debug", C.DEFAULT_PNG_DEBUG)
        if not result:
            return

        ctx = self._context
        gs = self._grid_size

        ctx.set_source_rgb(0.25, 0.25, 1)
        self._set_font(10, FONT_WEIGHT_BOLD)
        for cell in self.deadends:
            identifiers = cell.room_identifiers
            if not identifiers:
                continue
            msg = str(identifiers)
            ctx.move_to((cell.x + 0.08 + OFFSET) * gs, (cell.y + 0.4 + OFFSET) * gs)
            ctx.show_text(msg)

    def _rectangle(self, x, y, width, height):
        gs = self._grid_size

        x += OFFSET
        y += OFFSET
        self._context.rectangle(x * gs, y * gs, width * gs, height * gs)

    def _line(self, x1, y1, width, height):
        self._move_to(x1, y1)
        self._line_to(x1 + width, y1 + height)

    def _move_to(self, x, y):
        gs = self._grid_size

        x += OFFSET
        y += OFFSET
        self._context.move_to(x * gs, y * gs)

    def _line_to(self, x, y):
        gs = self._grid_size

        x += OFFSET
        y += OFFSET
        self._context.line_to(x * gs, y * gs)

    def _set_font(self, size, style):
        gs = self._grid_size

        self._context.set_font_size(gs * size / C.DEFAULT_PNG_GRID_SIZE)
        self._context.select_font_face("Arial", FONT_SLANT_NORMAL, style)

    def _set_line_width(self, size):
        gs = self._grid_size
        self._context.set_line_width(size * gs / C.DEFAULT_PNG_GRID_SIZE)

    def _rotate(self, cell, x, y, w, h):
        if cell.direction == C.Directions.NORTH:
            return cell.x + x, cell.y + y, w, h
        if cell.direction == C.Directions.EAST:
            return cell.x + (1 - y), cell.y + x, h, w
        if cell.direction == C.Directions.SOUTH:
            return cell.x + x, cell.y + (1 - y), w, h
        if cell.direction == C.Directions.WEST:
            return cell.x + y, cell.y + x, h, w
        return None  # pragma: no cover
