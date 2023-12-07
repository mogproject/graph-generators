from manim import *


class RealGraph:
    def __init__(self) -> None:
        self.obj = Graph([], [])

    def _vconf(self):
        return dict(z_index=100, radius=0.03, stroke_color=GRAY_BROWN, stroke_width=1)

    def _econf(self):
        return dict(color=WHITE, stroke_width=2)

    def has_edge(self, u, v) -> bool:
        return (u, v) in self.obj.edges

    def anim_create_leaves(self, vertices: list[int], pos: dict[int, Point]):
        self.obj.add_vertices(*vertices, positions=pos, vertex_config=self._vconf())
        n = len(vertices)
        ds = [0.5, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2]
        if len(ds) < n:
            ds += [0.1] * (n - len(ds))
        lags = [0]
        for i in range(n - 1):
            lags += [lags[-1] + ds[i]]
        return AnimationGroup(*(Succession(Wait(t), Create(self.obj[v])) for v, t in zip(vertices, lags)))

    def anim_add_edge(self, u: int, v: int):
        ret =  self.obj.animate.add_edges((u, v), edge_config=self._econf())
        self.obj.edges[u, v].set_z_index(98)
        return ret
