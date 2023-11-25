import networkx as nx
from typing import TextIO

__all__ = [
    'read_pace_2016',
    'load_pace_2016',
    'write_pace_2016',
    'save_pace_2016',
    'read_pace_2023',
    'load_pace_2023',
    'write_pace_2023',
    'save_pace_2023',
]


def read_pace(input: TextIO) -> nx.Graph:
    G = None
    for line in input.readlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('c'):
            continue  # ignore comments

        if line.startswith('p'):
            _, _, nn, mm = line.split()
            n, m = int(nn), int(mm)
            G = nx.empty_graph(n)
        else:
            u, v = map(int, line.split())
            assert G is not None
            G.add_edge(u - 1, v - 1)

    assert G is not None
    assert m == G.number_of_edges(), 'inconsistent edges'
    return G


def read_pace_2016(input: TextIO) -> nx.Graph:
    return read_pace(input)


def read_pace_2023(input: TextIO) -> nx.Graph:
    return read_pace(input)


def load_pace_2016(path: str) -> nx.Graph:
    with open(path) as f:
        return read_pace_2023(f)


def load_pace_2023(path: str) -> nx.Graph:
    with open(path) as f:
        return read_pace_2023(f)


def write_pace(output: TextIO, G: nx.Graph, problem_name: str) -> None:
    n = G.number_of_nodes()
    m = G.number_of_edges()
    assert set(G.nodes()) == set(range(n))  # labeled [0,n)

    output.write(f'p {problem_name} {n} {m}\n')
    for u, v in G.edges():
        output.write(f'{u + 1} {v + 1}\n')


def write_pace_2016(output: TextIO, G: nx.Graph) -> None:
    write_pace(output, G, 'tw')


def write_pace_2023(output: TextIO, G: nx.Graph) -> None:
    write_pace(output, G, 'tww')


def save_pace_2016(path: str, G: nx.Graph) -> None:
    with open(path, 'w') as f:
        write_pace_2016(f, G)


def save_pace_2023(path: str, G: nx.Graph) -> None:
    with open(path, 'w') as f:
        write_pace_2023(f, G)
