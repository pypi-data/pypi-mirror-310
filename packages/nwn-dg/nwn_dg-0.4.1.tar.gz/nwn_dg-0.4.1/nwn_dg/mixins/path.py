import functools
import itertools

import networkx as nx
from boltons import iterutils

from .. import constants as C


class PathMixin:
    def _get_graph(self):
        edges = self.get_room_edges()
        return nx.from_edgelist(edges)

    def get_longest_path(self):
        return self.get_longest_paths()[0]

    @functools.lru_cache(maxsize=10)
    def get_connected_rooms(self, cell):
        def action(cell, accumulator):
            if cell.room_identifier:
                accumulator += [cell.room_identifier]
                return C.WalkAction.CLOSE_CELL
            return C.WalkAction.OPEN_CELL

        results = []
        self.__walk(cell, lambda i: action(i, results))
        return iterutils.unique(results)

    @functools.lru_cache(maxsize=10)
    def get_longest_paths(self):
        graph = self._get_graph()
        periphery = self.get_periphery()

        # Calculate the paths from each periphery to another
        product = itertools.product(periphery, periphery)
        product = iterutils.unique(tuple(sorted(x)) for x in product if x[0] != x[1])

        paths = []
        for nodes in product:
            paths += nx.all_shortest_paths(graph, nodes[0], nodes[1])

        max_len = max(len(path) for path in paths)
        paths = [path for path in paths if len(path) == max_len]
        return paths

    @functools.lru_cache(maxsize=10)
    def get_room_edges(self):
        """
        For every room, do a dijkstra search for all connected rooms
        Stop at every room that is different and accumulate the pair of room
        identifiers.
        This will current also detect deadends which have a room_identifier
        """

        def action(cell, identifier, accumulator):
            if cell.room_identifier and cell.room_identifier != identifier:
                pair = sorted([cell.room_identifier, identifier])
                if pair not in accumulator:
                    accumulator += [pair]
                return C.WalkAction.CLOSE_CELL
            return C.WalkAction.OPEN_CELL

        # Calculate the rooms connected to each other
        results = []
        for room in self.rooms:
            # pylint: disable=cell-var-from-loop
            self.__walk(room.center, lambda i: action(i, room.identifier, results))
        return sorted(results)

    @functools.lru_cache(maxsize=10)
    def get_periphery(self):
        graph = self._get_graph()
        return list(nx.periphery(graph))

    def __walk(self, start, action):
        open_cells = [start]
        closed_cells = []

        while open_cells:
            current = open_cells.pop()
            closed_cells += [current]
            for direction in C.DIRECTIONS:
                cell = self.get_adjacent_cell(current, direction)
                if cell is None or not cell.is_floor():
                    continue
                if cell in closed_cells or cell in open_cells:
                    continue

                result = action(cell)
                if result == C.WalkAction.RETURN:
                    return
                if result & C.WalkAction.CLOSE_CELL:
                    closed_cells += [cell]
                elif result & C.WalkAction.OPEN_CELL:
                    open_cells += [cell]
