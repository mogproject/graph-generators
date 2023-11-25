from collections.abc import Generator
from typing import Any

class Graph:
    node_dict_factory: Any
    node_attr_dict_factory: Any
    adjlist_outer_dict_factory: Any
    adjlist_inner_dict_factory: Any
    edge_attr_dict_factory: Any
    graph_attr_dict_factory: Any
    def to_directed_class(self): ...
    def to_undirected_class(self): ...
    graph: Any
    def __init__(self, incoming_graph_data: Any | None = ..., **attr) -> None: ...
    @property
    def adj(self): ...
    @property
    def name(self): ...
    @name.setter
    def name(self, s) -> None: ...
    def __iter__(self): ...
    def __contains__(self, n): ...
    def __len__(self): ...
    def __getitem__(self, n): ...
    def add_node(self, node_for_adding, **attr) -> None: ...
    def add_nodes_from(self, nodes_for_adding, **attr) -> None: ...
    def remove_node(self, n) -> None: ...
    def remove_nodes_from(self, nodes) -> None: ...
    @property
    def nodes(self): ...
    def number_of_nodes(self): ...
    def order(self): ...
    def has_node(self, n): ...
    def add_edge(self, u_of_edge, v_of_edge, **attr) -> None: ...
    def add_edges_from(self, ebunch_to_add, **attr) -> None: ...
    def add_weighted_edges_from(
        self, ebunch_to_add, weight: str = ..., **attr
    ) -> None: ...
    def remove_edge(self, u, v) -> None: ...
    def remove_edges_from(self, ebunch) -> None: ...
    def update(self, edges: Any | None = ..., nodes: Any | None = ...) -> None: ...
    def has_edge(self, u, v): ...
    def neighbors(self, n): ...
    @property
    def edges(self): ...
    def get_edge_data(self, u, v, default: Any | None = ...): ...
    def adjacency(self): ...
    @property
    def degree(self): ...
    def clear(self) -> None: ...
    def clear_edges(self) -> None: ...
    def is_multigraph(self): ...
    def is_directed(self): ...
    def copy(self, as_view: bool = ...): ...
    def to_directed(self, as_view: bool = ...): ...
    def to_undirected(self, as_view: bool = ...): ...
    def subgraph(self, nodes): ...
    def edge_subgraph(self, edges): ...
    def size(self, weight: Any | None = ...): ...
    def number_of_edges(self, u: Any | None = ..., v: Any | None = ...): ...
    def nbunch_iter(self, nbunch: Any | None = ...) -> Generator[None, None, Any]: ...