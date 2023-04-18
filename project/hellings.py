from typing import Set, Tuple
from pyformlang.cfg import CFG
from networkx import MultiDiGraph
from project.cfg_utils import to_wcnf
from project.graph_utils import load_graph_from_file
from project.cfg_utils import wcnf_from_file


def hellings_all_pairs_rpq(graph: MultiDiGraph, cfg: CFG) -> Set[Tuple]:
    """
    Solve the reachability problem between all pairs of vertices
    for a given graph `graph`<V, E, L> and a given CF<N, E, P, S> grammar `cfq`.
    Based on the Hellings algorithm.

     Parameters
     ----------
     graph : `~networkx.MultiDiGraph`
         A source database
     cfq : ~`pyformlang.cfg import CFG`
         Context-free grammar that defines constraints

     Returns
     -------
     A a set of triples of the form:
        * start vertex
        * non_terminal of the cfg
    """
    wcfq = to_wcnf(cfg)
    E = graph.edges(data="label")
    V = graph.nodes()
    P = wcfq.productions
    # rules like N_i -> eps \in P
    non_term_to_eps = {p.head.value for p in P if not p.body}
    # non term to term: N -> t
    NT = {(p.head.value, p.body[0].value) for p in P if len(p.body) == 1}
    # non term to 2 non term: N -> NN
    NN = {p for p in P if len(p.body) == 2}
    # NN = {(p.head.value, p.body) for p in P if len(p.body) == 2}
    result = {
        # loop in graph with label N_i -> eps
        (u, N_i, u)
        for u in V
        for N_i in non_term_to_eps
    } | {
        # add all productions to terminals
        (v, N, u)
        for (v, u, t) in E
        for (N, t2) in NT
        if t2 == t
    }

    m = result.copy()
    while len(m) > 0:
        tmp_result = set()
        v, Ni, u = m.pop()
        # x -> v -> u
        for x, Nj, to in result:
            if v == to:
                for p in NN:
                    Nk = p.head.value
                    NjNi = p.body
                    if (x, Nk, u) not in result and NjNi == [Nj, Ni]:
                        m.add((x, Nk, u))
                        tmp_result.add((x, Nk, u))
        for r in tmp_result:
            result.add(r)
        # v -> u -> x
        for frm, Nj, x in result:
            if u == frm:
                for p in NN:
                    Nk = p.head.value
                    NiNj = p.body
                    if (v, Nk, x) not in result and NiNj == [Ni, Nj]:
                        m.add((v, Nk, x))
                        tmp_result.add((v, Nk, x))
        for r in tmp_result:
            result.add(r)
    return result


def hellings_rpq(
    graph: MultiDiGraph, cfg: CFG, non_term: str, start_v=None, final_v=None
) -> Set[Tuple]:
    """
    Solve the reachability problem for a given set of starting and final vertices,
    and a given non terminal `N`.

    Parameters
    ----------
    graph : `~networkx.MultiDiGraph`
        A source database
    cfq : ~`yformlang.cfg import CFG`
        Context-free grammar that defines constraints
    non_term: str
        View of a non terminal
    start_states: iterable
        Numbers of nodes in the graph that will be marked as the initial states of the automaton. By default, all vertices are marked.
    final_states: iterable
        Numbers of nodes in the graph that will be marked as the final states of the automaton. By default, all vertices are marked.

    Returns
    -------
    A a set of triples of the form:
        * start vertex
        * non_terminal of the cfg
        * final vertex
    """
    if start_v is None:
        start_v = graph.nodes()
    if final_v is None:
        final_v = graph.nodes()

    hellings_res = hellings_all_pairs_rpq(graph, cfg)
    return {
        (v, N, u)
        for (v, N, u) in hellings_res
        if v in start_v and u in final_v and (non_term is None or N == non_term)
    }


def hellings_all_pair_rpq_from_file(path_to_cfg: str, path_to_graph: str) -> Set[Tuple]:
    """
    Solve the reachability problem between all pairs of vertices
    for a given graph `graph`<V, E, L> and a given CF<N, E, P, S> grammar `cfq`.
    Based on the Hellings algorithm.

     Parameters
     ----------
     path_to_graph : str
         Path to a source graph database
     path_to_cfg : str
         Path to a context-free grammar that defines constraints

     Returns
     -------
    A a set of triples of the form:
        * start vertex
        * non_terminal of the cfg
        * final vertex
    """
    graph = load_graph_from_file(path_to_graph)
    cfg = wcnf_from_file(path_to_cfg)
    return hellings_all_pairs_rpq(graph, cfg)


def hellings_all_pair_rpq_text(graph: MultiDiGraph, cfg_text: str) -> Set[Tuple]:
    """
    Solve the reachability problem between all pairs of vertices
    for a given graph `graph`<V, E, L> and a given CF<N, E, P, S> grammar `cfq`.
    Based on the Hellings algorithm.

     Parameters
     ----------
     graph : str
         Source graph database
     cfg : str
         A text representation of context-free grammar that defines constraints

     Returns
     -------
         A a set of triples of the form:
            * start vertex
            * non_terminal of the cfg
            * final vertex
    """
    cfg = CFG.from_text(cfg_text)
    return hellings_all_pairs_rpq(graph, cfg)
