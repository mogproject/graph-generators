"""
Run `manim -pqh scene.py TwinWidthComputation` to create a high-quality video.
"""
from random import Random
from collections import Counter, defaultdict
import os
import networkx as nx
from random import Random
import math
from manim import *
from TextBox import TextBox

__version__ = '0.0.1'
__license__ = 'Apache License, Version 2.0'

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PYTHON_MAIN = os.path.join(PROJECT_DIR, 'src', 'main', 'python')


if PYTHON_MAIN not in sys.path:
    sys.path.insert(0, PYTHON_MAIN)

from generator.KAryParseTree import KAryParseTree
from generator.random_regular_multigraph import random_regular_multigraph


# TODO: different square size
# add jitter

# fixed metagraphs of 4 vertices
META_EDGES = {
    # level 0
    0: [(0, 1), (0, 1), (0, 3), (1, 2), (2, 3), (2, 3)],

    # level 1
    1: [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
    2: [(0, 2), (0, 2), (0, 2), (1, 3), (1, 3), (1, 3)],
    3: [(0, 1), (0, 1), (0, 2), (1, 3), (2, 3), (2, 3)],
    4: [(0, 1), (0, 3), (0, 3), (1, 2), (1, 2), (2, 3)],

    # level 2
    5: [(0, 1), (0, 2), (0, 2), (2, 3), (1, 3), (1, 3)],
    6: [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
    7: [(0, 3), (0, 3), (0, 3), (1, 2), (1, 2), (1, 2)],
    8: [(0, 2), (0, 2), (0, 3), (1, 2), (1, 3), (1, 3)],

    9: [(0, 2), (0, 3), (0, 3), (1, 2), (1, 2), (1, 3)],
    10: [(0, 1), (0, 3), (0, 3), (1, 2), (1, 2), (2, 3)],
    11: [(0, 1), (0, 1), (0, 2), (1, 3), (2, 3), (2, 3)],
    12: [(0, 2), (0, 3), (0, 3), (1, 2), (1, 2), (1, 3)],

    13: [(0, 2), (0, 2), (0, 2), (1, 3), (1, 3), (1, 3)],
    14: [(0, 1), (0, 1), (0, 3), (1, 2), (2, 3), (2, 3)],
    15: [(0, 2), (0, 2), (0, 3), (1, 2), (1, 3), (1, 3)],
    16: [(0, 1), (0, 1), (0, 1), (2, 3), (2, 3), (2, 3)],

    17: [(0, 3), (0, 3), (0, 3), (1, 2), (1, 2), (1, 2)],
    18: [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
    19: [(0, 1), (0, 1), (0, 1), (2, 3), (2, 3), (2, 3)],
    20: [(0, 1), (0, 2), (0, 2), (2, 3), (1, 3), (1, 3)],
}

class MetaGraph:
    def __init__(self, node_id: int, edges: list[(int, int)], tree_pos: dict[int, list[int]]) -> None:
        self.node_id = node_id
        self.edges = Counter(edges)

        scale = 2.2 if node_id < 1 else 1.6 if node_id < 5 else 1
        meta_vconf = dict(color=BLUE, fill_opacity=1.0, fill_color=BLACK, radius=0.1 * scale, z_index=4, stroke_width=1 * scale)
        meta_econf = dict(color=BLUE, z_index=3, stroke_width=1.2 * scale)
        meta_interval = 0.2 * scale

        self.vertex_objs = [
            Circle(**meta_vconf).move_to(tree_pos[node_id]).shift([-meta_interval, meta_interval, 0]),
            Circle(**meta_vconf).move_to(tree_pos[node_id]).shift([-meta_interval, -meta_interval, 0]),
            Circle(**meta_vconf).move_to(tree_pos[node_id]).shift([meta_interval, meta_interval, 0]),
            Circle(**meta_vconf).move_to(tree_pos[node_id]).shift([meta_interval, -meta_interval, 0]),
        ]

        shifts = []
        for (u, v), mult in self.edges.items():
            if mult == 1:
                shifts += [(u, v, True, [0, 0, 0])]
            elif mult == 2:
                if (u, v) in [(0, 2), (1, 3)]:
                    shifts += [(u, v, True, [0, meta_interval / 7, 0])]
                    shifts += [(u, v, False, [0, -meta_interval / 7, 0])]
                elif (u, v) in [(0, 1), (2, 3)]:
                    shifts += [(u, v, True, [-meta_interval / 7, 0, 0])]
                    shifts += [(u, v, False, [meta_interval / 7, 0, 0])]
                elif (u, v) in [(0, 3)]:
                    shifts += [(u, v, True, [meta_interval / 10, meta_interval / 10, 0])]
                    shifts += [(u, v, False, [-meta_interval / 10, -meta_interval / 10, 0])]
                elif (u, v) in [(1, 2)]:
                    shifts += [(u, v, True, [-meta_interval / 10, meta_interval / 10, 0])]
                    shifts += [(u, v, False, [meta_interval / 10, -meta_interval / 10, 0])]
                else:
                    assert False, 'never happens'
            elif mult == 3:
                if (u, v) in [(0, 2), (1, 3)]:
                    shifts += [(u, v, False, [0, meta_interval / 6, 0])]
                    shifts += [(u, v, True, [0, 0, 0])]
                    shifts += [(u, v, False, [0, -meta_interval / 6, 0])]
                elif (u, v) in [(0, 1), (2, 3)]:
                    shifts += [(u, v, False, [-meta_interval / 6, 0, 0])]
                    shifts += [(u, v, True, [0, 0, 0])]
                    shifts += [(u, v, False, [meta_interval / 6, 0, 0])]
                elif (u, v) in [(0, 3)]:
                    shifts += [(u, v, False, [meta_interval / 8, meta_interval / 8, 0])]
                    shifts += [(u, v, True, [0, 0, 0])]
                    shifts += [(u, v, False, [-meta_interval / 8, -meta_interval / 8, 0])]
                elif (u, v) in [(1, 2)]:
                    shifts += [(u, v, False, [-meta_interval / 8, meta_interval / 8, 0])]
                    shifts += [(u, v, True, [0, 0, 0])]
                    shifts += [(u, v, False, [meta_interval / 8, -meta_interval / 8, 0])]
                else:
                    assert False, 'never happens'
            else:
                assert False, 'never happens'

        self.edge_objs = [Line(self.vertex_objs[u].get_center(), self.vertex_objs[v].get_center(), **meta_econf).shift(s) for u, v, _, s in shifts]
        self.shifts = shifts

    def get_edge_animations(self):
        ret = []
        for i, c in enumerate(self.edge_objs):
            u, v = self.shifts[i][:2]
            ret += [c.animate.put_start_and_end_on(self.vertex_objs[u].get_center(), self.vertex_objs[v].get_center()).set_z_index(9)]
        return Succession(*ret)


class InnerData:
    def __init__(self, n: int, k: int, d: int, rand: Random) -> None:
        parse_tree = KAryParseTree(k, n)
        real_graphs: dict[int, nx.Graph] = {}
        # real_graph_layout: dict[int, dict[int, list[int]]] = defaultdict(dict)
        meta_graphs: dict[int, nx.MultiGraph] = {}
        meta_to_real: dict[int, list[((int, int), (int, int))]] = {}
        # canvas_width = 2
        # separator_width = 0.2

        for i in parse_tree.leaves():
            G = nx.Graph()
            assert len(parse_tree.vertex_range(i)) == 1
            G.add_nodes_from(parse_tree.vertex_range(i))
            real_graphs[i] = G
            # real_graph_layout[i] = {j: [0, 0, 0] for j in parse_tree.vertex_range(i)}

        for i in parse_tree.internal_nodes_bottom_up():
            G = nx.Graph()
            G.add_nodes_from(parse_tree.vertex_range(i))
            for t, j in enumerate(parse_tree.children(i)):
                G.add_edges_from(real_graphs[j].edges())  # internal edges
                # for v in real_graphs[j].nodes():
                #     x, y, z = real_graph_layout[j][v]
                #     scale = ((canvas_width - separator_width) / 2.0) / canvas_width
                #     shift = [(zx * f, zy * f, 0) for f in [(canvas_width + separator_width) / 4.0] for zx, zy in [(-1, 1), (-1, -1), (1, 1), (1, -1)]][t]
                #     real_graph_layout[i][v] = (x * scale + shift[0], y * scale + shift[1], z)

            # mg = random_regular_multigraph(parse_tree.num_children(i), d, rand)
            mg = nx.empty_graph(4, create_using=nx.MultiGraph)
            mg.add_edges_from(META_EDGES[i])
            m2r = []
            for x, y in mg.edges():
                assert x != y
                u = rand.choice(list(real_graphs[parse_tree.left(i) + x].nodes()))
                v = rand.choice(list(real_graphs[parse_tree.left(i) + y].nodes()))
                m2r += [((x, y), (u, v))]
                G.add_edge(u, v)  # external edges

            meta_graphs[i] = mg
            real_graphs[i] = G
            meta_to_real[i] = m2r

        self.n = n
        self.N = parse_tree.num_nodes
        self.k = k
        self.d = d
        self.parse_tree = parse_tree
        self.meta_graphs = meta_graphs
        self.real_graphs = real_graphs
        self.meta_to_real = meta_to_real
        # self.real_graph_layout = real_graph_layout


class RNMAnimation:

    def __init__(self, data: InnerData) -> None:
        self.data = data

        # tree object
        self.tree_pos = self.compute_tree_pos(data.N, data.k)
        self.tree = Graph([0], [], layout=self.tree_pos, root_vertex=0, vertex_type=self.get_tree_vtype(0), edge_config=self.get_tree_econf())

        # metagraph objects
        self.meta_graphs = {i: MetaGraph(i, data.meta_graphs[i].edges(), self.tree_pos) for i in range(data.N - data.n)}

        # realgraph objects
        self.real_graphs = {}
        self.initialize_real_graph()

    def get_level(self, i):
        ret = 0
        while i > 0:
            i = (i - 1) // self.data.k
            ret += 1
        return ret

    def get_tree_vtype(self, i: int):
        length = [1.6, 1.1, 0.7, 0.16][self.get_level(i)]
        w = [3, 2, 2, 1][self.get_level(i)]
        return lambda: Square(side_length=length).set_fill(BLACK, opacity=1.0).set_z_index(2).set_stroke(width=w)

    def get_tree_econf(self):
        return dict(stroke_width=1.5)

    def get_real_vconf(self, i: int):
        # r = [0.01, 0.02, 0.03, 0.03][self.get_level(i)]
        # w = [0.3, 0.5, 1, 1][self.get_level(i)]
        r = 0.03
        w = 1
        return dict(z_index=10, radius=r, stroke_color=GRAY_BROWN, stroke_width=w)

    def get_real_econf(self, i: int):
        # w = [0.6, 0.8, 1.2, 1.2][self.get_level(i)]
        w = 1.2
        return dict(color=GRAY_BROWN, stroke_width=w)

    def set_edge_z_index(self, G: Graph, z_index: int):
        for obj in G.edges.values():
            obj.set_z_index(z_index)

    def initialize_real_graph(self) -> None:
        for i in self.data.parse_tree.leaves():
            G = Graph.from_networkx(self.data.real_graphs[i], vertex_config=self.get_real_vconf(i), edge_config=self.get_real_econf(i), layout_scale=3)
            G.move_to(self.tree_pos[i])
            self.set_edge_z_index(G, 9)
            self.real_graphs[i] = G

    def merge_real_graph(self, i: int, subgraphs: list[Graph]) -> None:
        # vs = [v for g in subgraphs for v in g.vertices.keys()]
        pos = {v: obj.get_center() for g in subgraphs for v, obj in g.vertices.items()}
        # es = [e for g in subgraphs for e in g.edges.keys()] + [e for _, e in self.data.meta_to_real[i]]

        G = Graph.from_networkx(self.data.real_graphs[i], vertex_config=self.get_real_vconf(i), edge_config=self.get_real_econf(i), layout=pos, layout_scale=3)
        G.move_to(self.tree_pos[i])
        # G = Grafffph(vs, es, vertex_config=self.get_real_vconf(i), edge_config=self.get_real_econf(i), layout=pos, layout_scale=3)
        self.set_edge_z_index(G, 9)
        self.real_graphs[i] = G

    def compute_tree_pos(self, n: int, k: int):
        edges = [((i - 1) // k, i) for i in range(1, n)]
        g = Graph(list(range(n)), edges, layout='tree', root_vertex=0).stretch_to_fit_height(9).stretch_to_fit_width(14)
        ret = {}
        for i in range(n):
            x, y, z = g.vertices[i].get_center()
            ret[i] = [-x, y, z]  # flip the x-coordinate
        ret[0][1] -= 0.5
        return ret

    def anim_create_tree(self) -> Animation:
        return Create(self.tree)

    def anim_extend_tree(self, level: int) -> Animation:
        k = self.data.k
        lv = self.data.parse_tree.levels[level]

        def parent(i):
            return (i - 1) // k

        return self.tree.animate.add_edges(*[(parent(i), i) for i in lv], positions=self.tree_pos, vertex_type=self.get_tree_vtype(min(lv)))

    def anim_create_leaf(self, node: int) -> Animation:
        return Create(self.real_graphs[node])

    def anim_create_metagraph(self, node: int) -> AnimationGroup:
        return Succession(
            AnimationGroup(*(Create(c) for c in self.meta_graphs[node].vertex_objs)),
            AnimationGroup(*(Create(c) for c in self.meta_graphs[node].edge_objs)),
        )

    def anim_move_subgraphs(self, node: int) -> (list[Mobject], AnimationGroup):

        scale_factor = [0.5, 0.5, 1.0, 1.0][self.get_level(node)]
        # print(f'node={node}, level={self.get_level(node)}, scale_factor={scale_factor}')
        objs, ret = [], []
        for i, c in enumerate(self.data.parse_tree.children(node)):
            obj = self.real_graphs[c].copy()

            objs += [obj]
            ret += [obj.animate.move_to(self.meta_graphs[node].vertex_objs[i].get_center()).scale(scale_factor)]
        return objs, AnimationGroup(*ret)

    def anim_move_metaedges(self, node: int, subgraphs: list[Mobject]) -> list[AnimationGroup]:
        ret = []
        for i, ((x, y), (u, v)) in enumerate(self.data.meta_to_real[node]):
            obj = self.meta_graphs[node].edge_objs[i]
            uu = subgraphs[x].vertices[u].get_center()
            vv = subgraphs[y].vertices[v].get_center()
            ret += [Succession(
                AnimationGroup(obj.animate.set_color(YELLOW).set_z_index(9), run_time=0.2),  # flash
                AnimationGroup(obj.animate.put_start_and_end_on(uu, vv), run_time=0.4)  # move
            )]
        return ret


class RNMExample(MovingCameraScene):
    def compute_tree_pos(self, n: int, k: int):
        edges = [((i - 1) // k, i) for i in range(1, n)]
        g = Graph(list(range(n)), edges, layout='tree', root_vertex=0).stretch_to_fit_height(9).stretch_to_fit_width(14)
        ret = {}
        for i in range(n):
            x, y, z = g.vertices[i].get_center()
            ret[i] = [-x, y, z]  # flip the x-coordinate
        ret[0][1] -= 0.5
        return ret

    def construct(self):
        # settings
        n = 64
        k = 4
        d = 3
        N = sum(4 ** i for i in range(4))

        data = InnerData(n, k, d, Random(12345))
        anim = RNMAnimation(data)

        def run_animations(*animations):
            for a in animations:
                self.play(a)

        # -----------------------------------------------------------------------
        #    Start animation.
        # -----------------------------------------------------------------------

        title_text = Tex('Example: $\\textsf{RandomNearModularGraph}' + f'(n={n}, k={k}, d={d})$').to_edge(UL)
        self.play(Write(title_text))

        # -----------------------------------------------------------------------
        #    Create a near-modular decomposition tree.
        # -----------------------------------------------------------------------
        text_step_1 = TextBox('Step 1:\\linebreak Create a $k$-ary complete tree with $n$ leaves.')
        run_animations(*text_step_1.get_animations())

        # Level 0, 1
        self.play(anim.anim_create_tree())
        self.play(anim.anim_extend_tree(1))

        # Caption 1
        brace = Brace(mobject=anim.tree, direction=DOWN, buff=0.5)
        brace_text = brace.get_tex('k=4')

        self.play(GrowFromCenter(brace), FadeIn(brace_text))
        self.wait()
        self.play(ShrinkToCenter(brace), FadeOut(brace_text))

        # Level 2, 3
        self.play(anim.anim_extend_tree(2), run_time=0.8)
        self.play(anim.anim_extend_tree(3), run_time=0.8)

        # Caption 3
        # brace2 = Brace(mobject=nmd_tree, direction=DOWN, buff=0.2)
        brace2 = Brace(mobject=anim.tree, direction=DOWN, buff=0.2)
        brace2_text = brace2.get_tex('n=64')

        self.play(GrowFromCenter(brace2), FadeIn(brace2_text))
        self.wait()
        self.play(ShrinkToCenter(brace2), FadeOut(brace2_text))

        # -----------------------------------------------------------------------
        #    Create singletons at the leaves.
        # -----------------------------------------------------------------------

        # for i in lv3:
        #     inner_graphs[i] = Graph([0], [], vertex_config=inner_vertex_config).move_to(nmd_tree[i])

        self.camera.frame.save_state()

        text_step_2 = TextBox('Step 2:\\linebreak Assign a new vertex to each leaf node.')
        run_animations(*text_step_2.get_animations())

        self.play(
            # self.camera.auto_zoom(nmd_tree[1 + k + k ** 2], margin=2), run_time=1
            self.camera.auto_zoom(anim.tree[1 + k + k ** 2], margin=2), run_time=1
        )
        self.play(
            AnimationGroup(
                anim.anim_create_leaf(1 + k + k ** 2),
                anim.anim_create_leaf(1 + k + k ** 2 + 1),
                anim.anim_create_leaf(1 + k + k ** 2 + 2),
                anim.anim_create_leaf(1 + k + k ** 2 + 3),
                lag_ratio=0.1
            )
        )

        self.play(
            AnimationGroup(*(anim.anim_create_leaf(i) for i in range(1 + k + k ** 2 + 4, data.N)), lag_ratio=0.1),
            Restore(self.camera.frame),
            run_time=3
        )

        # -----------------------------------------------------------------------
        #    Create metagraphs.
        # -----------------------------------------------------------------------

        # metagraphs = {node: MetaGraph(node, META_EDGES[node], tree_pos) for node in range(1 + k + k ** 2)}
        # metagraphs = {node: MetaGraph(node, data.meta_graphs[node].edges(), tree_pos) for node in range(1 + k + k ** 2)}
        text_step_3 = TextBox('Step 3:\\linebreak~Create a metagraph---$d$-regular multigraph---\\linebreak~for each internal node.')
        run_animations(*text_step_3.get_animations())

        for node in [5, 6]:
            # zoom in
            self.play(self.camera.auto_zoom(anim.tree[node], margin=0.5), runtime=1)
            # self.play(self.camera.auto_zoom(nmd_tree[node], margin=0.5), runtime=1)
            self.play(anim.anim_create_metagraph(node))
            # self.play(*(Create(c) for c in metagraphs[node].vertex_objs))
            # self.play(*(Create(c) for c in metagraphs[node].edge_objs))

        self.play(
            AnimationGroup(
                *(anim.anim_create_metagraph(i) for i in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 1, 2, 3, 4, 0]),
                lag_ratio=0.2
            ),
            Restore(self.camera.frame),
            run_time=4
        )
        self.wait()

        # -----------------------------------------------------------------------
        #    Build internal graphs.
        # -----------------------------------------------------------------------

        def process_one_metagraph(node, metagraphs):
            # subgraphs = [anim.real_graphs[node * k + 1 + i].copy() for i in range(k)]

            # move subgraphs
            # self.play(self.camera.auto_zoom(nmd_tree[node], margin=3), runtime=0.5)
            self.play(self.camera.auto_zoom(anim.tree[node], margin=3), runtime=0.5)
            sg, anims = anim.anim_move_subgraphs(node)
            self.play(anims)

            # self.play(*(subgraphs[i].animate.move_to(metagraphs[node].vertex_objs[i].get_center()).scale(7 / 20) for i in range(k)))

            # assign external edges
            self.play(self.camera.auto_zoom(anim.tree[node], margin=0.5), runtime=1)
            # self.play(self.camera.auto_zoom(nmd_tree[node], margin=0.5), runtime=1)

            for i, ((x, y), (u, v)) in enumerate(data.meta_to_real[node]):
                obj = metagraphs[node].edge_objs[i]
                uu = sg[x].vertices[u].get_center()
                vv = sg[y].vertices[v].get_center()
                obj.set_z_index(20)
                self.play(obj.animate.set_color(YELLOW), run_time=0.4)  # flash
                self.play(obj.animate.put_start_and_end_on(uu, vv), run_time=0.3)  # move
            # for i, r in enumerate(anim.anim_move_metaedges(node, sg)):
            #     self.play(
            #         r,
            #         anim.meta_graphs[node].edge_objs[i].animate.set_color(YELLOW)
            #     )
            #     ,
            #     # metagraphs[node].get_edge_animations(),
            # )
            # for obj in anim.meta_graphs[node].edge_objs:
            #     obj.set_color(YELLOW)

            # set up real graph
            anim.merge_real_graph(node, sg)

            self.play(
                *(FadeOut(c) for c in metagraphs[node].vertex_objs),
                *(FadeOut(c) for c in metagraphs[node].edge_objs),
                # *(FadeOut(c) for c in metagraphs[node].get_auxiliary_edge_objects()),
                # *(c.animate.set_stroke_color(GRAY_BROWN) for c in metagraphs[node].get_primary_edge_objects()),
                FadeIn(anim.real_graphs[node]),
                *(FadeOut(ss) for ss in sg),
            )

            # replace graphs
            # self.remove(*sg)
            # self.remove(*metagraphs[node].edge_objs)
            # self.add(anim.real_graphs[node])

        def process_multiple_metagraphs(nodes, metagraphs):
            ret = []
            sgs = []
            anim_move = []

            for node in nodes:
                sg, am = anim.anim_move_subgraphs(node)
                sgs += [sg]
                anim_move += [am]

            self.play(*anim_move, Restore(self.camera.frame), run_time=2)

            for node, sg in zip(nodes, sgs):
                anim.merge_real_graph(node, sg)

            self.play(
                *(FadeOut(c) for node in nodes for c in metagraphs[node].vertex_objs),
                *(FadeOut(c) for node in nodes for c in metagraphs[node].edge_objs),
                *(FadeIn(anim.real_graphs[node]) for node in nodes),
                *(FadeOut(ss) for sg in sgs for ss in sg),
                run_time=2
            )
            # subgraphs = [anim.real_graphs[node * k + 1 + i].copy() for i in range(k)]

            #     anims = [
            #         AnimationGroup(
            #             *(subgraphs[i].animate.move_to(metagraphs[node].vertex_objs[i].get_center()) for i in range(k)),
            #             run_time=2
            #         ),
            #         AnimationGroup(
            #             metagraphs[node].get_edge_animations(),
            #             *(FadeOut(c) for c in metagraphs[node].vertex_objs),
            #             run_time=1
            #         ),
            #         AnimationGroup(
            #             *(FadeOut(c) for c in metagraphs[node].get_auxiliary_edge_objects()),
            #             *(c.animate.set_stroke_color(GRAY_BROWN) for c in metagraphs[node].get_primary_edge_objects()),
            #             run_time=1
            #         )
            #     ]
            #     ret += [AnimationGroup(*anims, lag_ratio=1.0)]

            # self.play(
            #     *ret,
            #     Restore(self.camera.frame),
            #     # run_time=6
            # )
        process_one_metagraph(1 + k, anim.meta_graphs)
        process_one_metagraph(1 + k + 1, anim.meta_graphs)
        process_multiple_metagraphs(range(1 + k + 2, 1 + k + k ** 2), anim.meta_graphs)

        # level 1
        process_one_metagraph(1, anim.meta_graphs)
        process_one_metagraph(2, anim.meta_graphs)
        process_one_metagraph(3, anim.meta_graphs)
        process_one_metagraph(4, anim.meta_graphs)

        # # level 0
        process_one_metagraph(0, anim.meta_graphs)

        self.play(Restore(self.camera.frame))
