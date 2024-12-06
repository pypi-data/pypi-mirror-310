import networkx as nx

from .. import constants as C
from ..idungeon import IDungeon
from ..mixins import PathMixin


class Tree(IDungeon, PathMixin):
    def __init__(self, dungeon):
        IDungeon.__init__(self, dungeon)
        PathMixin.__init__(self)

        self._output_tree = self.args.get("output_tree", C.DEFAULT_OUTPUT_TREE)

    def save(self):
        if not self._output_tree:
            return

        # The following import is very slow, so move it here in case
        # graph is not to be created
        # pylint: disable=import-outside-toplevel
        import matplotlib.pyplot as plt

        filename = self.args["filepath"] + ".tree.png"

        graph = self._get_graph()
        layout = nx.spring_layout(graph, seed=0)

        # TODO: When an entrance is added, we should rather print from entrance to furthestpoint
        longest_path = self.get_longest_path()
        color_map = ["#00a080" if node in longest_path else "#00b4d9" for node in graph]

        nx.draw(graph, pos=layout, with_labels=True, node_color=color_map, font_weight="bold")
        plt.savefig(filename)
