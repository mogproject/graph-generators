"""
Run `manim -pqh scene.py TwinWidthComputation` to create a high-quality video.
"""
from random import Random
import os
from random import Random
from manim import *

__version__ = '0.0.1'
__license__ = 'Apache License, Version 2.0'

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PYTHON_MAIN = os.path.join(PROJECT_DIR, 'src', 'main', 'python')


if PYTHON_MAIN not in sys.path:
    sys.path.insert(0, PYTHON_MAIN)

from TextBox import TextBox
from ParseTree import ParseTree
from RealGraph import RealGraph
from MetaGraph import MetaGraph

# ===============================================================================
#    Data
# ===============================================================================

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

    def get_level(self, i: int, k: int):
        ret = 0
        while i > 0:
            i = (i - 1) // k
            ret += 1
        return ret

    def construct(self):
        # settings
        n = 64
        k = 4
        d = 3
        N = sum(4 ** i for i in range(4))

        def run_animations(*animations, **args):
            for a in animations:
                self.play(a, **args)

        # -----------------------------------------------------------------------
        #    Start animation.
        # -----------------------------------------------------------------------

        title_text = Tex('Example: $\\textsf{RandomNearModularGraph}' + f'(n={n}, k={k}, d={d})$').to_edge(UL, MED_LARGE_BUFF)
        self.play(Write(title_text))

        # -----------------------------------------------------------------------
        #    Create a near-modular decomposition tree.
        # -----------------------------------------------------------------------
        text_step_1 = TextBox('Step 1:\\linebreak Create a $k$-ary complete tree with $n$ leaves.')
        run_animations(*text_step_1.get_animations())

        parse_tree = ParseTree(n, k)

        # Level 0, 1
        self.play(parse_tree.anim_create_root())
        self.play(parse_tree.anim_extend(1))

        # Caption 1
        brace = Brace(mobject=parse_tree.tree, direction=DOWN, buff=0.5)
        brace_text = brace.get_tex('k=4')

        self.play(GrowFromCenter(brace), FadeIn(brace_text))
        self.wait()
        self.play(ShrinkToCenter(brace), FadeOut(brace_text))

        # Level 2, 3
        self.play(parse_tree.anim_extend(2), run_time=0.8)
        self.play(parse_tree.anim_extend(3), run_time=0.8)

        # Caption 3
        brace2 = Brace(mobject=parse_tree.tree, direction=DOWN, buff=0.2)
        brace2_text = brace2.get_tex('n=64')

        self.play(GrowFromCenter(brace2), FadeIn(brace2_text))
        self.wait()
        self.play(ShrinkToCenter(brace2), FadeOut(brace2_text))
        self.wait()

        self.camera.frame.save_state()

        # -----------------------------------------------------------------------
        #    Create singletons at the leaves.
        # -----------------------------------------------------------------------

        rg = RealGraph()

        text_step_2 = TextBox('Step 2:\\linebreak Assign a new vertex to each leaf node.')
        run_animations(*text_step_2.get_animations())

        self.play(
            self.camera.auto_zoom(parse_tree.tree[1 + k + k ** 2], margin=2), run_time=1
        )
        self.play(
            rg.anim_create_leaves(range(1 + k + k ** 2, N), parse_tree.tree_pos),
            Succession(
                Wait(1),
                Restore(self.camera.frame, run_time=3),
            ),
            run_time=4
        )
        self.wait()

        # -----------------------------------------------------------------------
        #    Create metagraphs.
        # -----------------------------------------------------------------------

        mgs = {i: MetaGraph(i, es, parse_tree.tree_pos[i]) for i, es in META_EDGES.items()}

        text_step_3 = TextBox('Step 3:\\linebreak~Create a random metagraph---$d$-regular multigraph---\\linebreak~for each internal node.')
        run_animations(*text_step_3.get_animations(3))

        for node in [1 + k, 1 + k + 1]:
            # zoom in
            self.play(self.camera.auto_zoom(parse_tree.tree[node], margin=0.5), runtime=1)
            # create
            self.play(mgs[node].anim_create())

        self.play(
            AnimationGroup(
                *(mgs[i].anim_create() for i in list(range(1 + k + 2, 1 + k + k ** 2)) + list(range(1, 1 + k)) + [0]),
                lag_ratio=0.3
            ),
            Restore(self.camera.frame),
            run_time=4
        )
        self.wait()

        # -----------------------------------------------------------------------
        #    Create realization hierarchies.
        # -----------------------------------------------------------------------

        text_step_4 = TextBox('Step 4:\\linebreak~Construct a hierarchy of metagraphs.')
        run_animations(*text_step_4.get_animations(2))

        self.play(
            AnimationGroup(*(rg.obj[i].animate.move_to(
                mgs[(i - 1) // k].vertices[(i - 1) % k]
            ).scale(1.5) for i in parse_tree.data.leaves()), lag_ratio=0.1),
            run_time=3
        )

        # group metagraphs with singleton vertices
        meta_groups = {}
        for i in parse_tree.data.levels[2]:
            meta_groups[i] = VGroup(
                mgs[i].obj,
                *(rg.obj[c] for c in parse_tree.data.children(i))
            )

        self.play(
            AnimationGroup(*(meta_groups[i].animate.move_to(
                mgs[(i - 1) // k].vertices[(i - 1) % k]
            ).scale(0.35).set_stroke(width=1.0) for i in parse_tree.data.levels[2]), lag_ratio=0.1),
            Succession(
                Wait(1),
                self.camera.auto_zoom(parse_tree.tree[0], margin=6.0)
            ),
            run_time=3
        )

        for i in parse_tree.data.levels[1]:
            meta_groups[i] = VGroup(
                mgs[i].obj,
                *(meta_groups[c] for c in parse_tree.data.children(i))
            )

        self.play(
            AnimationGroup(*(meta_groups[i].animate.move_to(
                mgs[(i - 1) // k].vertices[(i - 1) % k]
            ).scale(0.35).set_stroke(width=0.35) for i in parse_tree.data.levels[1]), lag_ratio=0.1),
            Succession(
                Wait(0.5),
                self.camera.auto_zoom(parse_tree.tree[0], margin=0.2)
            ),
            run_time=2.5
        )
        self.wait()

        meta_groups[0] = VGroup(mgs[0].obj, *(meta_groups[c] for c in parse_tree.data.children(0)))

        self.play(
            FadeOut(parse_tree.tree),
            meta_groups[0].animate.move_to((0, -0.4, 0)).scale(9).set_stroke(width=3),
            Restore(self.camera.frame),
        )

        # -----------------------------------------------------------------------
        #    Realize metaedges.
        # -----------------------------------------------------------------------

        text_step_5 = TextBox('Step 5:\\linebreak~Realize metaedges:\\linebreak~Randomly assign endpoints to group members.')
        run_animations(*text_step_5.get_animations(3))

        rand = Random(12344)

        def realize_metagraph(nodes, speed=1.0):
            for idx in range(6):
                # create data
                xx = {node: parse_tree.data.left(node) + mgs[node].edge_data[idx][0] for node in nodes}
                yy = {node: parse_tree.data.left(node) + mgs[node].edge_data[idx][1] for node in nodes}
                xs = {node: parse_tree.data.vertex_range(xx[node]) for node in nodes}
                ys = {node: parse_tree.data.vertex_range(yy[node]) for node in nodes}
                u = {node: rand.randint(xs[node].start, xs[node].stop - 1) + (N - n) for node in nodes}
                v = {node: rand.randint(ys[node].start, ys[node].stop - 1) + (N - n) for node in nodes}
                uu = {node: rg.obj.vertices[u[node]].get_center() for node in nodes}
                vv = {node: rg.obj.vertices[v[node]].get_center() for node in nodes}

                # flash group pair
                self.play(
                    *(
                        mgs[node].vertex_objs[mgs[node].edge_data[idx][k]].animate.set_stroke(color=YELLOW)
                        for node in nodes for k in [0, 1]
                    ),
                    *(
                        mgs[node].edge_data[idx][2].animate.set_stroke(color=YELLOW)
                        for node in nodes
                    ),
                    run_time=0.2 * speed
                )

                # move highlighted edge
                self.play(
                    *(mgs[node].edge_data[idx][2].animate.set_z_index(99) for node in nodes),
                    run_time=0.1 * speed
                )

                self.play(
                    *(mgs[node].vertex_objs[mgs[node].edge_data[idx][k]].animate.set_stroke(color=BLUE) for node in nodes for k in [0, 1]),
                    *(mgs[node].edge_data[idx][2].animate.put_start_and_end_on(uu[node], vv[node]) for node in nodes),
                    run_time=0.3 * speed
                )

                # add real edge
                anims = []
                for node in nodes:
                    if not rg.has_edge(u[node], v[node]):
                        anims += [rg.anim_add_edge(u[node], v[node])]

                self.play(
                    *anims,
                    *(FadeOut(mgs[node].edge_data[idx][2]) for node in nodes),
                    run_time=0.2 * speed
                )

            self.play(*(FadeOut(mgs[node].obj) for node in nodes), run_time=0.4 * speed)

        # level 2
        self.play(self.camera.auto_zoom(mgs[1 + k].obj, margin=2))
        realize_metagraph([1 + k])

        self.play(self.camera.auto_zoom(mgs[1].obj, margin=1))
        realize_metagraph([1 + k + 1, 1 + k + 2, 1 + k + 3], 0.3)

        self.play(Restore(self.camera.frame))
        realize_metagraph(list(range(1 + k + 4, N - n)), 0.3)

        self.play(
            *(
                Rotate(rg.obj.vertices[v], angle=PI / 12, about_point=mgs[(v - 1) // k].obj.get_center())
                for v in parse_tree.data.leaves()
            ),
        )

        self.play(
            self.camera.auto_zoom(mgs[1].obj, margin=1),
            *(
                rg.obj.vertices[v].animate.scale(1.5)
                for v in parse_tree.data.leaves()
            )
        )

        # level 1
        realize_metagraph([1])

        self.play(self.camera.auto_zoom(mgs[2].obj, margin=1))
        realize_metagraph([2])

        self.play(self.camera.auto_zoom(mgs[3].obj, margin=1))
        realize_metagraph([3])

        self.play(self.camera.auto_zoom(mgs[4].obj, margin=1))
        realize_metagraph([4])

        self.play(Restore(self.camera.frame))
        self.wait()

        realize_metagraph([0])

        self.play(
            *(
                Rotate(rg.obj.vertices[v], angle=2 * PI, about_point=mgs[(v - 1) // k].obj.get_center())
                for v in parse_tree.data.leaves()
            ),
            run_time=5
        )
        self.wait(3)
        self.play(FadeOut(rg.obj), FadeOut(title_text))
