from typing import Any

def from_agraph(A, create_using: Any | None = ...): ...
def to_agraph(N): ...
def write_dot(G, path) -> None: ...
def read_dot(path): ...
def graphviz_layout(G, prog: str = ..., root: Any | None = ..., args: str = ...): ...
def pygraphviz_layout(G, prog: str = ..., root: Any | None = ..., args: str = ...): ...
def view_pygraphviz(
    G,
    edgelabel: Any | None = ...,
    prog: str = ...,
    args: str = ...,
    suffix: str = ...,
    path: Any | None = ...,
    show: bool = ...,
): ...
