from manim import *


class TextBox:
    def __init__(self, text: str, height=1, width=4):
        self.box = Rectangle(  # create a box
            height=height, width=width, fill_color=BLUE_E,
            fill_opacity=0.9, stroke_color=LOGO_WHITE
        )
        self.tex = Tex(text, color=LOGO_WHITE)
        self.box.surround(self.tex, buff=LARGE_BUFF)
        self.tex.arrange(center=False, aligned_edge=LEFT)
        self.obj = VGroup(self.box, self.tex).set_z_index(100)

    def get_animations(self, wait_duration=2) -> list[Animation]:
        return [
            FadeIn(self.box, run_time=0.5),
            Write(self.tex),
            Wait(wait_duration),
            FadeOut(self.obj),
        ]
