from manim import *

from generator.KAryParseTree import KAryParseTree


class ParseTree:
    def __init__(self, n: int, k: int) -> None:
        self.data = KAryParseTree(k, n)
        self.tree_pos = self.compute_tree_pos(self.data.num_nodes, k)
        self.tree = Graph([0], [], layout=self.tree_pos, root_vertex=0, vertex_type=self._root_vconf, edge_config=self._econf())
        self.k = k

    def _vconf(self, length, width):
        z_index = 2
        stroke_color=LIGHT_GRAY
        return Square(side_length=length).set_fill(BLACK, opacity=1.0).set_z_index(z_index).set_stroke(width=width, color=stroke_color)

    def _econf(self):
        stroke_color=LIGHT_GRAY
        return dict(stroke_width=1.5, stroke_color=stroke_color)

    def _root_vconf(self):
        return self._vconf(0.7, 2)

    def _leaf_vconf(self):
        return self._vconf(0.16, 1)

    def parent(self, i):
        return (i - 1) // self.k

    def compute_tree_pos(self, n: int, k: int):
        edges = [((i - 1) // k, i) for i in range(1, n)]
        g = Graph(list(range(n)), edges, layout='tree', root_vertex=0).stretch_to_fit_height(9).stretch_to_fit_width(14)
        ret = {}
        for i in range(n):
            x, y, z = g.vertices[i].get_center()
            ret[i] = [-x, y, z]  # flip the x-coordinate
        ret[0][1] -= 0.5  # adjust the root position
        return ret

    def anim_create_root(self):
        return Create(self.tree)

    def anim_extend(self, level: int):
        new_edges = [(self.parent(i), i) for i in self.data.levels[level]]
        vtype = self._leaf_vconf if level == len(self.data.levels) - 1 else self._root_vconf
        return self.tree.animate.add_edges(*new_edges, positions=self.tree_pos, vertex_type=vtype)

    def anim_fade_out(self):
        return FadeOut(self.tree)
