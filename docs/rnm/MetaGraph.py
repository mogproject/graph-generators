from manim import *

from collections import Counter


class MetaGraph:
    def _get_level(self, i):
        k = 4
        ret = 0
        while i > 0:
            i = (i - 1) // k
            ret += 1
        return ret

    def __init__(self, node_id: int, edges: list[(int, int)], pos: Point) -> None:
        self.node_id = node_id
        self.level = self._get_level(node_id)
        base_z_index = 50 + self.level * 2

        radius = 0.1 if self.level == 2 else 0.14
        vstroke = 1.5
        estroke = 1.8
        meta_interval = 0.2 if self.level == 2 else 0.17

        meta_vconf = dict(
            color=BLUE,
            fill_opacity=1.0,
            fill_color=BLACK,
            radius=radius,
            z_index=base_z_index + 1,
            stroke_width=vstroke
        )
        meta_econf = dict(color=BLUE, z_index=base_z_index, stroke_width=estroke)

        self.vertex_objs = [
            Circle(**meta_vconf).move_to(pos).shift([-meta_interval, meta_interval, 0]),
            Circle(**meta_vconf).move_to(pos).shift([-meta_interval, -meta_interval, 0]),
            Circle(**meta_vconf).move_to(pos).shift([meta_interval, meta_interval, 0]),
            Circle(**meta_vconf).move_to(pos).shift([meta_interval, -meta_interval, 0]),
        ]
        self.vertices = VGroup(*self.vertex_objs)

        edge_data = []
        for (u, v), mult in Counter(edges).items():
            shift = [[0, 0, 0]]
            if mult == 2:
                k1, k2 = 5, 7
                if (u, v) in [(0, 2), (1, 3)]:  # parallel
                    shift = [[0, meta_interval / k1, 0], [0, -meta_interval / k1, 0]]
                elif (u, v) in [(0, 1), (2, 3)]:
                    shift = [[-meta_interval / k1, 0, 0], [meta_interval / k1, 0, 0]]
                elif (u, v) in [(0, 3)]:  # diagonal
                    shift = [[meta_interval / k2, meta_interval / k2, 0], [-meta_interval / k2, -meta_interval / k2, 0]]
                elif (u, v) in [(1, 2)]:
                    shift = [[-meta_interval / k2, meta_interval / k2, 0], [meta_interval / k2, -meta_interval / k2, 0]]
                else:
                    assert False, 'never happens'
            elif mult == 3:
                k1, k2 = 3, 4
                if (u, v) in [(0, 2), (1, 3)]:  # parallel
                    shift += [[0, meta_interval / k1, 0], [0, -meta_interval / k1, 0]]
                elif (u, v) in [(0, 1), (2, 3)]:
                    shift += [[-meta_interval / k1, 0, 0], [meta_interval / k1, 0, 0]]
                elif (u, v) in [(0, 3)]:  # diagonal
                    shift += [[meta_interval / k2, meta_interval / k2, 0], [-meta_interval / k2, -meta_interval / k2, 0]]
                elif (u, v) in [(1, 2)]:
                    shift += [[-meta_interval / k2, meta_interval / k2, 0], [meta_interval / k2, -meta_interval / k2, 0]]
                else:
                    assert False, 'never happens'
            else:
                assert mult == 1

            for s in shift:
                uu = self.vertex_objs[u].get_center()
                vv = self.vertex_objs[v].get_center()
                obj = Line(uu, vv, **meta_econf).shift(s)
                edge_data += [(u, v, obj)]

        self.edge_data = edge_data
        self.edge_objs = [obj for _, _, obj in edge_data]
        self.edges = VGroup(*self.edge_objs)
        self.obj = VGroup(self.vertices, self.edges)

    def anim_create(self):
        return Succession(
            Create(self.vertices, lag_ratio=0),
            Create(self.edges, lag_ratio=0),
        )
