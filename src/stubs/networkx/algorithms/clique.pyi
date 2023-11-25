from collections.abc import Generator
from typing import Any

def enumerate_all_cliques(G) -> Generator[Any, None, None]: ...
def find_cliques(G, nodes: Any | None = ...) -> Generator[Any, None, Any]: ...
def find_cliques_recursive(
    G, nodes: Any | None = ...
) -> Generator[None, None, Any]: ...
def make_max_clique_graph(G, create_using: Any | None = ...): ...
def make_clique_bipartite(
    G, fpos: Any | None = ..., create_using: Any | None = ..., name: Any | None = ...
): ...
def graph_clique_number(G, cliques: Any | None = ...): ...
def graph_number_of_cliques(G, cliques: Any | None = ...): ...
def node_clique_number(
    G, nodes: Any | None = ..., cliques: Any | None = ..., separate_nodes: bool = ...
): ...
def number_of_cliques(G, nodes: Any | None = ..., cliques: Any | None = ...): ...
def cliques_containing_node(G, nodes: Any | None = ..., cliques: Any | None = ...): ...

class MaxWeightClique:
    G: Any
    incumbent_nodes: Any
    incumbent_weight: int
    node_weights: Any
    def __init__(self, G, weight) -> None: ...
    def update_incumbent_if_improved(self, C, C_weight) -> None: ...
    def greedily_find_independent_set(self, P): ...
    def find_branching_nodes(self, P, target): ...
    def expand(self, C, C_weight, P) -> None: ...
    def find_max_weight_clique(self): ...

def max_weight_clique(G, weight: str = ...): ...