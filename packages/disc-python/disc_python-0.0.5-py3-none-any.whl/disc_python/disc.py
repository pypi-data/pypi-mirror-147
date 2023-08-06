import sys
import networkx as nx
from collections import Counter
import numpy as np

from disc_python import algoritmos as algos

this_module = sys.modules[__name__]
has_key = lambda k, d: k in d


# --- ALAGOS CONFIG TO APSP PROBLEM -------
    # key   = Alias APSP algo
    # value = Algo PLL o Skeche name
STANDAR = {
    "dijkstra":        "all_pairs_dijkstra",
    "pruned_dijkstra": "apsp_labeling",
    "sketche":         "sketch_apsp"
    }
# Same above, jist for simple algorithm
SIMPLES = {
    "pruned_dijkstra_simple": "cover_labeling",
    "sketches_simple":        "sketches"
    }

__all__ = ['disc']

def disc(G, algo='sketches_simple', verbose = False, all_pairs = False,*args, **kwargs):
    """Compute the DIS-C graph. This function can compute the DIS-C distance between pairs
    of concepts.
    
    Parameters
    -----------
    G : NetworkX graph
        Conceptual graph where are the concepts an its realations.

    algo : str - 'sketches_simple' (default)
        Algorithm´s name to calculte the generality, the time computing of the method depends
        of this algo becouse it´s the more expensive process. To see the algo you can use,
        consulting the __all__ variable of this module.

    verbose : bool
        To see the verbose.

    all_pairs : bool
        To compute the dis-c distance between whole pairs of concepts in the graph G.

    Return
    -----
    DIS-C graph. This graph contains the distance between the pair of concepts declared in the
    'pairs' kwargs params.

    See More
    -----
    To see the format of the 'pairs' kwargs params, see the README.md in the root directory.
    """
    if verbose:
        print("\n -- Executing DIS-C with algorithm {}({}) --".format(algo,kwargs))
    card = Counter(r[2]['tipo'] for r in G.edges.data())
    s_p = {}
    s_p_inverse = {}
    for p in card.keys():
        s_p[p] = 1
        s_p_inverse[p] = 1
    """ - Calcula los atributos topologicos de cada nodo:
        - + i_a - grado de entrada
        - + o_a - grado de salida
        - + wi_a - costo de entrar al nodo
        - + wo_a - costo de salir del nodo
        - + v_a - generalidad
    """
    for index , (i,o) in enumerate(zip(G.in_degree, G.out_degree)):
        i_a, o_a = i[1] , o[1]
        wi_a = 1 - (i_a / (i_a + o_a))
        wo_a = 1 - (o_a / (i_a + o_a))
        G.nodes[i[0]]['i_a'] = i_a
        G.nodes[i[0]]['o_a'] = o_a
        G.nodes[i[0]]['wi_a'] = wi_a
        G.nodes[i[0]]['wo_a'] = wo_a
        G.nodes[i[0]]['v_a'] = 1.0
        G.nodes[i[0]]['index'] = index

    eps, curEPS, oldEPS = 1000, 1000, 1000  # Parametros de las condiciones de paro
    eps_K = 1e-5
    j = 0
    p_w = 0.5
    while j < 15 and eps > eps_K:
        disc_graph = nx.DiGraph()
        if verbose:
            print(" Adding edges to DIS-C graph...")
        total_weight = 0.0
        for a,b,p in G.edges.data():
            tipo = p['tipo']
            w_oa = G.nodes[a]['wo_a']
            w_ia = G.nodes[a]['wi_a']
            w_ib = G.nodes[b]['wi_a']
            w_ob = G.nodes[b]['wo_a']
            v_a  =  G.nodes[a]['v_a']
            v_b  =  G.nodes[b]['v_a']
            index_a = G.nodes[a]['index']
            index_b = G.nodes[b]['index']
            w_ab = (p_w)*(v_a*w_oa + v_b*w_ib) + (1-p_w)*s_p[tipo]
            w_ba = (p_w)*(v_b*w_ob + v_a*w_ia) + (1-p_w)*s_p_inverse[tipo]
            disc_graph.add_edge(a,b, weight=np.float32(w_ab))
            disc_graph.add_edge(b,a, weight=np.float32(w_ba))
            disc_graph.nodes[a]['index'] = index_a
            disc_graph.nodes[b]['index'] = index_b
            total_weight += w_ab + w_ba
        if verbose:
            print(" Computing thresholds ...")
        curEPS = _compute(disc_graph, G, algo, **kwargs)
        eps = (oldEPS - curEPS)**2
        oldEPS = curEPS
        if verbose:
            print(" Computing weights for each type of relation ...")
        for p_tipo in card.keys():
            aux_s_p = 0
            aux_s_p_inverso = 0
            for a, b, p in G.edges.data():
                if p_tipo == p['tipo']:
                    aux_s_p += disc_graph[a][b]['weight']
                    aux_s_p_inverso += disc_graph[b][a]['weight']
            s_p[p_tipo] = aux_s_p / card[p_tipo]
            s_p_inverse[p_tipo] = aux_s_p_inverso / card[p_tipo]
        j+=1
    return disc_graph


def get_disc(disc, term_a, term_b):
    """Get the dis-c value between two concepts.

    Params
    ----------------
    disc : NetworkX graph
        DIS-C graph.

    term_a : str
        First Concept/Term in the graph.

    term_b : str
        Second Concept/Term in the graph.
    """
    try:
        disc.nodes[term_a]
    except KeyError:
        raise KeyError('The term {} does not exists in the ontology'.format(term_a))
    try:
        disc.nodes[term_b]
    except KeyError:
        raise KeyError('The term {} does not exists in the ontology'.format(term_b))
    try:
        disc.nodes[term_a]['disc_to_node_']
    except KeyError:
        raise KeyError('The term {} does not have any asociated DISC disntance'.format(term_a))
    try:
        disc.nodes[term_a]['disc_to_node_'][term_b]
    except KeyError:
        raise KeyError('The term {} does not have any asociated DISC disntance with the term {}'.format(term_a,term_b))
    try:
        return disc.nodes[term_a]['disc_to_node_'][term_b]
    except Exception as ex:
        raise ex




def _compute(disc, algo, **kwargs):
    """Redirect the computing of the DIS-C distnace.

    Params.
    ---------------------
    disc : NetworkX graph
        The DIS-C graph.

    algo : str
        The algorithm that will be executed to compute the DIS-C distance.

    Return
    --------------------
    The average of the generality reached in the actual iteration.
    """
    if algo in STANDAR:
         ret_val = _standard(disc, algo,  **kwargs)
    elif algo in SIMPLES:
        ret_val = _simples(disc, algo, **kwargs)
    else:
        raise ValueError("Algorithm in params does not exist. Please use: dijkstra, pruned_dijkstra,\
        sketche, pruned_dijkstra_simple or sketches_simple")
    return ret_val / disc.number_of_nodes()


def _generality(fromm, to):
    """Return the generality of one node to the others."""
    return fromm / to

def _standard(graph_disc, algo, all_terms = False, **kwargs):
    """Execute the standart algorithms to the DIS-C distance computing. This algorithms, to computing the
    DIS-C distance, resolve the APSP problem. That´s means, there are to steps to get the DIS-C distance.
    The first step compute the cover or index of the graph; this can be reached by using the PLL method
    (using Pruned dijkstra algorithm) or by Oracles Distance (using Skeching algorithm). The second step
    is about computing the distance between the pairs of concepts declared in the 'pairs' kwargs params,
    if all_pairs falg is true, then is computing the distance between all the pairs of concepts in the graph;
    this is very slow becouse at least take n^2 time plus the time consulting.
    If the dijkstra algorithm is passed as param, then the cover/index is just the APSP matrix and the
    time consulting just take n^2.

    Params.
    ----------------
    graph_disc : NetworkX graph
        The DIS-C graph.

    algo : str
        The standart algorithm to be used in the distance computation.

    all_terms : bool, default False
        Flag to determine if all pairs of concepts in the graph should be considered for the DIS-C distance computation.
        If this falg is true, then the method will need n^2 extra time and if the graph is huge, the memory could be
        overflowed.

    Return.
    ----------------
    The sum squared of the generality of the whole graph.
    """
    ret_val = 0
    list_pairs = list()
    distances = dict()
    distances['out'] = dict()
    distances['in'] = dict()
    # compute the cover/index of the graph.
    apsp = getattr(algos, STANDAR[algo])(graph_disc, memory_save=True, **kwargs)
    for _, pairs in kwargs['concepts'].items():
        list_pairs.extend(pairs.values())
    for fromm, length in apsp:
        distances['out'][fromm] = 0
        if not all_terms:
            try:
                if fromm in list_pairs:
                    graph_disc.nodes[fromm]['disc_to_node_'] = length
            except KeyError:
                raise KeyError("There are not concepts pairs in the arg 'concepts' to compute")
        else:
            graph_disc.nodes[fromm]['disc_to_node_'] = length
        for k,v in length.items():
            distances['out'][fromm] += v
            try:
                distances['in'][k] += v
            except KeyError:
                distances['in'][k] = v
    for n in graph_disc:
        fromm, to = distances['out'][n], distances['in'][n]
        v_a = graph_disc.nodes[n]['v_a']
        ret_val += (v_a - _generality(fromm, to)) ** 2
        graph_disc.nodes[n]['v_a'] = _generality(fromm, to)
    return ret_val


def _simples(graph_disc, algo, all_terms = False, **kwargs):
    """ Execute the simples algorithms to the DIS-C distance computing. This algorithms just compute
    the cover/index of the graph by using the techniques: PLL method (using Pruned dijkstra algorithm)
    or by Oracles Distance (using Skeching algorithm).

    To get the generality of the nodes, the method just compute the division between the sum
    of the distances in the 'in cover' and the sum of the distances in the 'out cover', insted
    of get the distance from APSP matrix; therefore it is not necesary to compute the APSP problem.

     Params.
    ----------------
    graph_disc : NetworkX graph
        The DIS-C graph.

    algo : str
        The simple algorithm to be used in the distance computation.

    all_terms : bool, default False
        Flag to determine if all pairs of concepts in the graph should be considered for the DIS-C distance computation.
        If this falg is true, then the method will need n^2 extra time and if the graph is huge, the memory could be
        overflowed. Also the time consulting could be slow down the method, even it could be slower than the standart versrion.
        Becaouse of the tiem consulting required a linear search plus the n^2 pairs of nodes.

    Return.
    ----------------
    The sum squared of the generality of the whole graph.
    """
    from disc_python.algoritmos.determistas import _query_directes
    try:
        if not all_terms:
            p = kwargs['concepts']
    except KeyError:
        raise KeyError("There is not pairs of concepts in the parameter 'concepts'. Please see the format.")
    ret_val = 0
    list_pairs = list()
    labeling_landmark = getattr(algos, SIMPLES[algo])(graph_disc, memory_save=True, **kwargs)
    if all_terms:
        for u in graph_disc:
            if not has_key('disc_to_node_', graph_disc.nodes[u]):
                graph_disc.nodes[u]['disc_to_node_'] = dict()
            for v in graph_disc:
                graph_disc.nodes[u]['disc_to_node_'][v]  = _query_directes(u,v,labeling_landmark)
    else:
        for k in p.keys():
            for w_a, w_b in p.values():
                try:
                    if not has_key('disc_to_node_', graph_disc.nodes[p[k][w_a]]):
                        graph_disc.nodes[p[k][w_a]]['disc_to_node_'] = dict()
                    if not has_key('disc_to_node_', graph_disc.nodes[p[k][w_b]]):
                        graph_disc.nodes[p[k][w_b]]['disc_to_node_'] = dict()
                    graph_disc.nodes[p[k][w_b]]['disc_to_node_'][p[k][w_a]]  = _query_directes(p[k][w_a],p[k][w_b],labeling_landmark)
                    graph_disc.nodes[p[k][w_a]]['disc_to_node_'][p[k][w_b]]  = _query_directes(p[k][w_b],p[k][w_a],labeling_landmark)
                except KeyError:
                    continue
    for n in graph_disc:
        fromm, to = 1.0, 1.0
        for k,v in dict(labeling_landmark['in'][n]).items():
            to += v
        for k,v in dict(labeling_landmark['out'][n]).items():
            fromm += v
        v_a = graph_disc.nodes[n]['v_a']
        ret_val += (v_a - _generality(fromm, to)) ** 2
        graph_disc.nodes[n]['v_a'] = _generality(fromm, to)
    return ret_val


def _floyd_warshall(graph_disc, graph, bound = None, **kwargs):
    from disc_python.algoritmos import all_pairs_floyd_warshall

    ret_val = 0
    distancias = all_pairs_floyd_warshall(graph_disc, **kwargs)
    for fromm, length in distancias.items():
        graph_disc.nodes[fromm]['disc_to_node_'] = length
    for n in graph_disc:
        fromm, to = 0.0, 0.0
        for m in graph_disc:
            fromm += graph_disc.nodes[n]['disc_to_node_'][m]
            to += graph_disc.nodes[m]['disc_to_node_'][n]
        v_a = graph_disc.nodes[n]['v_a']
        ret_val += (v_a - _generality(fromm, to)) ** 2
        graph_disc.nodes[n]['v_a'] = _generality(fromm, to)
    return ret_val
