""" Compute the All Pair Shortest path and path lengths.

These algorithms work with directed and weighed graphs.

All the algorithms here are deterministic, that means they always compute
the exact path and path length.

The two main approaches to solve the problem are:
    - algorithms that solve the single source shortest problem
    - algorithms base on min-plus matrix multiplication
"""
from heapq import heappush, heappop
from itertools import count

__all__ = [
    "all_pairs_dijkstra",
    "all_pairs_floyd_warshall",
    "cover_labeling",
    "apsp_labeling"
]

def all_pairs_dijkstra(G, weight="weight", *args, **kwargs):
    """Encuentre las rutas y longitudes ponderadas más cortas entre todos los nodos.

    Parameters
    -----------
    G : NetworkX graph
        Grafo dirigido ponderado donde se hara el procesamiento

    weigth : str
        Nombre del atributo donde que contiene el peso de una arista

    Yield
    -----
    (node, (distancia, path)) : (node obj, (dict, dict))
        Cada nodo tienen asociado dos diccionarios. Uno mantiene las distancias(float)
        por cada un de los nodos donde la llave es el nodo correspondiente.
        El segundo contiene el camino, en forma de lista, hacia cada nodo,
        de igual manera el nodo es la llave y cada elemento de lista es nodo del camino (en orden).

    Notes
    -----
    Los pesos de las aristas deben ser numericos.

    Los diccionarios que retorna la funcion solo contiene los nodos accesibles.

    """
    for n in G:
        dist, _ = _single_source_dijkstra(G, n, weight=weight)
        yield (n, dist)


#@distances_decorator
#@run_time_decorator
def all_pairs_floyd_warshall(G, weight="weight",*args, **kwargs):
    """Encuentra todos los caminos más cortos entre todos los pares de vertices
    usando el algoritmo de floyd_warshall

    Parameters
    ----------
    G : NetworkX graph
        Grafo dirigido ponderado donde se hara el procesamiento

    weigth : str
        Nombre del atributo donde que contiene el peso de una arista

    Returns
    -------
    distance : dictionaries
    Diccionario de diccionarios, donde la llave superior corresponde a el nodo i,
    y la inferior al j.

    """
    from collections import defaultdict

    dist = defaultdict(lambda: defaultdict(lambda: float("inf")))
    for u in G:
        dist[u][u] = 0
    for u, v, d in G.edges(data=True):
        e_weight = d.get(weight, 1.0)
        dist[u][v] = min(e_weight, dist[u][v])
    for w in G:
        dist_w = dist[w]  # save recomputation
        for u in G:
            dist_u = dist[u]  # save recomputation
            for v in G:
                d = dist_u[w] + dist_w[v]
                if dist_u[v] > d:
                    dist_u[v] = d
    return dict(dist)


def cover_labeling(G, weigth='weigth', **kwargs):
    """Use Pruned Dijkstra to construct a 2-hop cover labeling from a directed and weighted graph.

    Parameters
    ----------
    G : NetworkX graph
        Directed and weighted graph.

    weigth : str
        Nombre del atributo donde que contiene el peso de una arista

    Returns
    -------
    2-hop cover : dictionaries
        The 'in' key in the dictionary correspond to the coverage for the nodes, taken the in-edges.
        The 'out' key in the dictionary correspond to the coverage for the nodes, taken the out-edges

    Notes
    --------
    To know more about 2-hop cover labeling using pruned algorithms, see the paper:
    https://arxiv.org/abs/1304.4661
    """
    #L = ac.two_hop_cover_dirigido(G)
    cover = {}
    cover['in'] = {}
    cover['out'] = {}
    for v in G:
        cover['in'][v] = dict()
        cover['out'][v] = dict()
    s = sorted(G.degree, key= lambda x: x[1], reverse=True)
    for (k,_) in s:
        cover['out'],_ = _pruned_dijkstra(G, k, cover, edges='out')
        cover['in'],_ = _pruned_dijkstra(G, k, cover, edges='in')
    return cover


def apsp_labeling(G, labeling = None, memory_save=False, **kwargs):
    """Return the APSP distances by yield. The yield statement gets every distance
        from one node to all the others, not one by one distance.

    Parameters
    ----------
    G : NetworkX graph
        Directed and weighted graph.

    labeling : dictionary
        2-Hop Cover Labeling of the graph

    memory_save: boolean
        To reduce the memory consuming by generate 'on the fly' every pair of distances.

    Returns
    -------
    node, disntaces: node, dictionary
        Current node.
        Distances from current node to all the others.
        If memory save flag is true, then every pair of distances is yielded in each iteration,
        and also the value of return is: source node, destination node and distance

    See more
    ---------
        cover_labeling()

    Notes
    --------
    In each yield, the return is a tuple of current node and a
    dictionary of distances from that node to the others.
    """
    #data = ac.calculate_distances(G,l)
    data = dict()
    if labeling is None:
        labeling = cover_labeling(G)
    for i in G.nodes:
        aux_data = dict()
        for j in G:
            aux_data[j] = _query_directes(i, j, labeling)
        if memory_save:
            yield (i,aux_data)
        else:
            data[i] = aux_data
    if not memory_save:
        return dada



def _pruned_dijkstra(G, source, cover, edges='out', weigth='weight'):
    """Pruned Dijkstra, this function uses the coverage to compute the distances from source node
    to all the others. Also it updates the labeling of the nodes that were visited by the source node.

    Parameters
    ----------
    G : NetworkX graph
        Directed and weighted graph.

    source: node
        source node

    cover: dictionary cover
        Coverage o index of the graph

    edges: str
        Type of edges to use; in-edges or out-edges.

    weigth : str
        Atribute name where it´s represented the weigth value.

    Returns
    -------
    coverage updated, distances : dictionary, dictionary
        The coverage updated.
        The distances reached by source node using the cover labeling.
    Notes
    --------
    To know more about 2-hop cover labeling using pruned algorithms, see the paper:
    https://arxiv.org/abs/1304.4661"""
    push = heappush
    pop = heappop
    fringe = []
    dist = {}  # dictionary of final distances
    seen = {}
    c = count()
    adj = G._pred if edges == 'in' else G.adj
    seen[source] = 0
    push(fringe, (0, next(c), source))
    while fringe:
        (d, _, u) = pop(fringe)
        if u in dist:
            continue  # already searched this node.
        dist[u] = d
        if edges == 'out':
            aux_query = _query_directes(source, u, cover)
            if aux_query <= dist[u]:
                dist[u] = aux_query
                continue
        else:
            aux_query = _query_directes(u, source, cover)
            if aux_query <= dist[u]:
                dist[u] = aux_query
                continue
        cover[edges][u].update({source : dist[u]})
        for v, _ in adj[u].items():
            if edges == 'out':
                uv = G.adj[u][v]["weight"]
            else:
                uv = G.adj[v][u]["weight"]
            uv_dist = dist[u] + uv
            if v not in seen or uv_dist < seen[v]:
                seen[v] = uv_dist
                push(fringe, (uv_dist, next(c), v))
    return cover[edges], dist


def _query_directes(source, to, labeling):
    """Search the min distance between two nodes using the cover labeling.

    Parameters
    ----------
    source: node
        Where it from.

    to: node
        Where it to.

    labeling: dictionary cover labeling
        2-Hop Cover Labeling of the graph

    Notes
    ---------
        The function uses a linear serach, but it can gets better performance by using a binary search."""
    labeling_u = dict(labeling['in'][source])
    labeling_v = dict(labeling['out'][to])
    min_distance = float('inf')
    try:
        for k in labeling_u.keys():
            if k in labeling_v:
                aux = (labeling_u[k] + labeling_v[k])
                if aux <= min_distance:
                    min_distance = aux
        return min_distance
    except Exception:
        return float('inf')

def _single_source_dijkstra(G, source, weight):
    """ Encuentra los caminos más cortos entre un vértice dado source
    y todos los demás vértices en el gráfico.

    Parameters
    -----------
    G : NetworkX graph
        Grafo dirigido ponderado donde se hara el procesamiento

    source : NetworkX node
        Nodo de origen


    weigth : str
        Nombre del atributo donde que contiene el peso de una arista

    Returns
    -------
    (distancias, path) : (dict, dict)
        El primer elemento es el diccionario con todas las distancias y
        el segundo elemento es el diccionario de todos los caminos.
    """
    distancias = {}
    padres = {}
    push = heappush
    pop = heappop
    seen = {}
    fringe = []
    seen[source] = 0
    padres[source] = [source]
    c = count()
    push(fringe, (0, next(c), source))
    while fringe:
        (d, _, u) = pop(fringe)
        if u in distancias:
            continue
        distancias[u] = d
        for v in G._adj[u]:
            uv_dist = distancias[u] + G._adj[u][v]["weight"]
            if v not in seen or uv_dist < seen[v]:
                seen[v] = uv_dist
                push(fringe, (uv_dist, next(c), v))
                padres[v] = padres[u] + [v]
    return (distancias,padres)