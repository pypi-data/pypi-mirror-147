"""Generic algoritms for Grphs"""

from heapq import heappush, heappop
from itertools import count

__all__ = [
    "bfs",
]

def bfs(G, seeds=[0], sketche = True, in_edges = False):
    """ TODO: Adaptar correctamente
    Breadth First Search

    Parameters
    -----------
    G : NetworkX graph
        Grafo dirigido ponderado donde se hara el procesamiento

    s: list, (default = [0])
        Nodos iniciales donde comenzara la busqueda

    Returns
    -------
    list : []
        Lista de nodos

    Notes
    -----
    """
    visited = seeds
    queue = seeds[:]
    sketche_dict = {}
    adj = G.adj
    for n in G:
        if n in seeds:
            sketche_dict[n] = (n,0)
            continue
        sketche_dict[n] = None
    if in_edges:
        adj = G._pred
    while queue:
        s = queue.pop(0)
        for neighbor in adj[s]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.append(neighbor)
                sketche_dict[neighbor] = _find_seed(sketche_dict,s)
    if sketche:
        return sketche_dict
    return visited

def _find_seed(sketche,s):
    value, seed = sketche[s], s
    i = 1
    while value[0] != seed:
        value, seed, i = sketche[value[0]], value[0], i+value[1]
    return (seed,i)

def dijkstra_multisource(G, sources = [0], sketche = True, in_edges= False):
    """Ejecuta el algoritmo de Dijkstra desde multiples nodos.
    El algoritmo está adaptado para identificar la semilla (nodo fuente de sources)
    más cercana a cada uno de los demás nodos, a esto se le conoce como sketche

    Parameters
    ----------
    G : NetworkX graph
        Grafo dirigido ponderado donde se hara el procesamiento

    sources : list(int)
        Lista de nodos fuente. Si contiene solo un nodo, se comporta como Dijkstra standart

    sketche : bool,(default = True)
        Bandera para indicar si regresa el sketche o si regresa las distancias

    in_edges : bool, (default = False)
        Bandera para identificar que aristas se utilizan en el algoritmo. Si False,
        utiliza las aristas que salen de los nodos, si True, utiliza las aristas
        que entran a los nodos.

    Returns
    -------
    dict : {nodo:(semilla,distancia)...}
        Sketch es un diccionario donde cada clave es un nodo y el valor es una tupla
        que contiene la semilla más cercana a el nodo(clave) y la distancia.

    Notes
    -----
    Las semillas son los nodos que estan en sources
    """
    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {}
    fringe = []
    c = count()
    sketche_dict = {}
    adj = G._pred if in_edges else G.adj
    for source in sources:
        if source not in G:
            raise Exception(f"Source {source} not in G")
        seen[source] = 0
        sketche_dict[source] = (source,0)
        push(fringe, (0, next(c), source))
    while fringe:
        (d, _, u) = pop(fringe)
        if u in dist:
            continue  # already searched this node.
        dist[u] = d
        for v, _ in adj[u].items():
            if not in_edges:
                uv = G.adj[u][v]["weight"]
            else:
                uv = G.adj[v][u]["weight"]
            uv_dist = dist[u] + uv
            if v not in seen or uv_dist < seen[v]:
                seen[v] = uv_dist
                push(fringe, (uv_dist, next(c), v))
                sketche_dict[v] = _find_seed_weighted(sketche_dict, v, u, uv)
    if sketche:
        return sketche_dict
    return dist

def _find_seed_weighted(sketche, s, padre, distancia):
    """ Funcion que retorna la semilla más cercana a un nodo y su distancia

    Parameters
    ----------
    sketche : dict
        Diccionario con los sketches

    s : nodo
        Nodo al que se le buscara la semilla

    padre : nodo
        Nodo padre de s

    distancia : float
        Distancia del nodo padre a s
    """
    value, seed = (padre,distancia), s
    i = 0
    while value[0] != seed:
        value, seed, i = sketche[value[0]], value[0], i+value[1]
    return (seed,i)