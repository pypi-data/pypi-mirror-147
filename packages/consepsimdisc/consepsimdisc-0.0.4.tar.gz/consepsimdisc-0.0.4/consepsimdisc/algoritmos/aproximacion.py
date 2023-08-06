"""Compute the All Pair Shortest path and path lengths.

These algorithms work with directed and weighed graphs.

All the algorithms here not are deterministic, that means they not always compute
the exact path and path length, but they give a less run time for large graphs.
"""

import numpy as np
import copy
import math
from collections import defaultdict

from disc_python.disc.algoritmos import generic

__all__ = [
    "sketch_apsp",
    "sketches",
    "common_seeds",
    "sketch_shorest_path",
    "all_pairs_ant_colony",
]

def sketch_apsp(G, sketches_labeling = None, memory_save=False, *args, **kwargs):
    """ Find all the shortest distances between all vertices.
    Use the sketches to do the calculation.

    Parameters
    ----------
    G : NetworkX graph
       Directed and weigthed graph

    k : int, (default = 2)
        Amount of times that the generation of a sketch will be executed.

    memory_save: boolean
        To reduce the memory consuming by generate 'on the fly' every pair of distances.

    Returns
    -------
    node, disntaces: node, dictionary
        Current node.
        Distances from current node to all the others.
        If memory save flag is true, then every pair of distances is yielded in each iteration,
        and also the value of return is: source node, destination node and distance

    Notes
    --------
        In each yield, the return is a tuple of current node and a
        dictionary of distances from that node to the others.

    """
    try:
        k = kwargs["k"]
    except KeyError:
        raise KeyError("Give the iterations amount ('k' parameter)")
    if sketches_labeling is None:
        sketches_labeling = sketches(G, k=k)

    data = dict()
    for i in G:
        aux_data = dict()
        for j in G:
            aux_data[j] = sketch_shorest_path(i, j, sketches_labeling)
        if memory_save:
            yield (i,aux_data)
        else:
            data[i] = aux_data
    if not memory_save:
        return dada



def sketches(G, **kwargs):
    """Function that executes k times the generation of a sketch.

    Parameters
    ----------
    G : NetworkX graph
        Directed and weigthed graph.

    k : int
        Number of times that the generation of a sketch will be executed.

    Returns
    -------
    dict : {node_1:[(seed_1,distance_1),...,(seed_r,distance_r) * k],...,node_i}
        sketche with r * k amount of seeds

    Notes
    -----
        The k sketches are combined into one. That is, the combined seeds of k are found in only one.
        For this reason the number of seeds per node is r*k.

    See More
    --------
    _ofline_sample
    """
    try:
        k = kwargs["k"]
    except KeyError:
        raise KeyError("Give the iterations amount ('k' parameter)")
    sketches = {}
    for _ in range(k):
        sketches_samples = _ofline_sample(G)
        for k,v in sketches_samples.items():
            try:
                sketches[k]
            except KeyError:
                sketches[k] = defaultdict(list)
            for kk,vv in v.items():
                sketches[k][kk].extend(vv)
    return sketches

def common_seeds(source, to, sketches):
    """Returns all the seeds (S) that coincide between two nodes, along with their respective distance.
    The distance is the sum of the distance from u to S and from S to v.

    Parameters
    ----------
    source : nodo
        source node.

    to: nodo
        Where it to.

    sketches : dict
        Sketche.

    Returns
    -------
    dict : {seed_i:distance_i,...,seed_S:distance_S}
       Dictionary with all matching seeds.

    Notes
    -----
    If there is a path from u to v then there is also at least one common seed.
    So if it has no seeds in common there is no path and it is represented by float('inf')
    (infinite)
    """

    if source==to:
        return {0:0}
    sketches_u = dict(sketches['in_edge'][source])
    sketches_v = dict(sketches['out_edge'][to])
    intersections_w = {}
    try:
        for k in sketches_u.keys():
            if k in sketches_v:
                distancia = sketches_u[k] + sketches_v[k]
                intersections_w[k] = distancia
        return intersections_w
    except Exception:
        return []

def sketch_shorest_path(source, to, sketches):
    """ Returns the shortest distance between a pair of nodes

    Parameters
    ----------
    source : nodo
        source node.

    to: nodo
        Where it to.

    sketches : dict
        Sketche.

    Returns
    -------
    float : distance
        The minimum distance between all seeds that match between two nodes.
    """

    if source==to:
        return 0.0

    sketche_u = dict(sketches['in'][source])
    sketche_v = dict(sketches['out'][to])
    min_distance = float('inf')
    try:
        for k in sketche_u.keys():
            if k in sketche_v:
                aux = (sketche_u[k] + sketche_v[k])
                if aux <= min_distance:
                    min_distance = aux
        return min_distance
    except Exception:
        return float('inf')

def all_pairs_ant_colony(G, num_ants = 10, max_iter = 1 , *args, **kwargs):
    """ Encuentra todas la ruta más cortas de todos los pares de vertices de
    un grafo dirigido mediante el algoritmo de colonia de hormigas.

    Parameters
    -----------
    G : NetworkX graph
        Grafo dirigido ponderado donde se hara el procesamiento

    num_ants : int (default=10)
        numero de hormigas. El numero de hormigas debe ser igual al numero de nodos.

    max_iter : int (default=100)
        numero maximo de iterciones.

    Returns
    -------
    {
        nodo_origen: {
            nodo_destino: {
                path:[],dist:int
            },
        },
    } : {nodo:{nodo:{path:list,dist:int}}}
        Retorna un diccionario de diccionarios, donde por cada llave de nodo origen
        existen n llaves de nodo destino y cada una de las n llaves destino contienen un diccionario
        donde la primera llave corresponde al path y la seguna a la distancia.

    Notes
    -----
    El numero de hormigas debe ser igual al numero de nodos.
    Al inicializar las variables 'best_path_length' y 'best_path' se hace uso del
    metodo privado _init_pheromones_values, debido a que ambas variables necesitan
    de n^2 iteraciones y se aprovecha el uso de las primeras n iteraciones en está función
    y las siguientes n en el metodo _init_pheromones_values.

    See Also
    --------
    _init_pheromones_values
    _update_pheromones
    """
    i = 0
    best_path = {}
    best_paths = {}
    best_path_length = {}
    pheromones_v = {}
    aux, a, b = _init_pheromones_values(G, best_path, best_path_length)
    for v in G:
        best_path_length[v] = copy.copy(a)
        best_path[v] = copy.copy(b)
        pheromones_v[v] = aux #_init_pheromones_values(G, best_path[v], best_path_length[v])
    while i < max_iter:
        for v in G:
            best_paths[v] = dict()
            for ant in range(num_ants):
                total_edges = []
                best_paths[v][ant] = _path_construction(G, v, ant, pheromones_v[v])
                total_edges.append(best_paths[v][ant]['edges'])
                try:
                    if best_paths[v][ant]['length_path'] <= best_path_length[v][ant]:
                        best_path[v][ant] = {'path':best_paths[v][ant]['path'],"dist":best_paths[v][ant]['length_path']}
                        best_path_length[v][ant] = best_paths[v][ant]['length_path']
                except KeyError as ex:
                    raise(ex)
            _update_pheromones(G, pheromones_v[v], total_edges)
        i += 1
    return best_path_length


def _init_pheromones_values(G, best_path={}, best_path_length={}):
    """ Inicializa una lista de adyacencia de feromonas

    Parameters
    -----------
    G : NetworkX graph
        Grafo dirigido ponderado donde se hara el procesamiento

    best_path : dict, optional(default={})
        Diccionario de los mejores caminos encontrados.

    best_path_length : int, optional(default={})
        Diccionario de las mejores longitudes encontradas por cada camino.

    Returns
    --------
    {node:{node_neighbor:{pheromone:float}}} : {node:{node:{srt:float}}}
        Lista de adyacencia que contiene el nivel de feromona que tiene cada arista.

    Notes
    -----
    Los parametros best_path, best_path_length son uso exclusivo de la funcion all_pairs_ant_colony,
    por lo que si se desea utilizar esta funcion en algun otro sitio es recomendable no pasarle
    como parametros nada en estas dos variables.
    El nivel de feromona se establece con la formula 1/grado_de_salida_del_vertice(n)

    See Also
    ---------
    all_pairs_ant_colony
    """
    adj_pheromones = {}
    for n in G:
        adj_pheromones[n] = dict()
        best_path[n] = []
        best_path_length[n] = float('inf')
        for neighbor in G.adj[n]:
            adj_pheromones[n][neighbor] = {"pheromone":1/G.out_degree(neighbor) if G.out_degree(neighbor) != 0 else 0 }
    return (adj_pheromones, copy.copy(best_path_length), copy.copy(best_path))

def _path_construction(G, source, target, pheromones):
    """ Construye un camino simple entre dos nodos, atraves de una caminata aleatoria
    con interaccion entre la cantidad de pheromonas que existe en las aristas.

    Parameter
    ----------
    G : NetworkX graph
        Grafo dirigido ponderado donde se hara el procesamiento

    source : Network nodo
        Nodo de origen

    target : Network nodo
        Nodo de destino

    pheromones : dict
        Lista de adyacencia de las feromonas

    Returns
    -------
    {path:[],edges:[],length_path:float} : dict()
        Diccionario con las claves:
            path        : lista de los nodos que contiene el camino
            edges       : lista de tuplas, cada tupla es una arista del tipo e=(v1,v2)
            length_path : Distancia total del camino

    Notes
    -----
    Es posible que en el recorrido no se llegue al destino, si esto ocurre,
    entonces, la distacia es infinito y el path son los nodos que se recorrieron.
    La distancia del path se calcula en _eval_path.
    Está version es una version con interaccion, lo que significa que las hormigas
    utilizan informacion de las feromonas de otra colonia, junto con la suya propia
    para encontrar el camino más corto.

    See Also
    --------
    _eval_path
    """
    p = [source]
    i = 0
    v = G.adj[source]
    edges = []
    visited = [source]
    try:
        G.adj[target]
    except KeyError:
        raise KeyError("No hay camino hacia {}".format(target))
    while list(v) != [] and target not in p:
        demoninator = 0
        for neighbor in v:
            demoninator += pheromones[p[i]][neighbor]['pheromone']
        for neighbor in v:
            prob = np.random.uniform(low=0.0, high=1.0, size=None)
            if (pheromones[p[i]][neighbor]['pheromone']/demoninator) >= prob:
                p.append(neighbor)
                v = set(G.adj[neighbor]).difference(visited)
                edges.append((p[i], neighbor))
                visited.append(neighbor)
                i += 1
                break
    return {"path": p, "edges":edges, "length_path":_eval_path(G, edges, target)}


def _update_pheromones(G, pheromones, edges, p=0.5):
    """Actualiza una lista de adyacencia (feromonas)

    Parameters
    -----------
    G : NetworkX graph
        Grafo dirigido ponderado donde se hara el procesamiento

    pheromones : dict , (paso por valor).
        Lista de adyacencia de feromonas a actualizar.

    edges : list of tuples
        Lista de tuplas, donde cada tupla es una arista. Este parametro debe contener todas las
        aristas de todos los caminos encontrados.

    p : float (default=0.5)
        Tasa de evaporación de feromonas

    Returns
    -------
    None

    Notes
    -----
    No retorna nada debido a que la lista de adyacencia de feromonas se pasa por valor y no por
    referencia.
    """
    for n, neighbors in G.adjacency():
        for neighbor in neighbors:
            if (n, neighbor) in edges:
                pheromones[n][neighbor]['pheromone'] = min(1-p*pheromones[n][neighbor]['pheromone']+p, (G.number_of_nodes()**2-1)/G.number_of_nodes()**2)
            else:
                pheromones[n][neighbor]['pheromone'] = max(1-p*pheromones[n][neighbor]['pheromone']+p, 1/G.number_of_nodes()**2)

def _eval_path(G, edges, target):
    """Calcula la distancia total de un camino

    Parameters
    ----------
    G : NetworkX graph
        Grafo dirigido ponderado donde se hara el procesamiento.

    edges : list of tuples
        Lista de tuplas, donde cada tupla es una arista del camino.

    target : NetworkX node
        Nodo de destino, a donde se supone debe terminar el camino.

    Returns
    -------
    length : float
        Retorna la distancia total del camino

    Notes
    -----
    En caso de que la lista de aristas no conduzcan a el nodo destino,
    se retornara infinito.
    """
    length = 0
    if edges == [] or edges[-1][1] is not target:
        return float('inf')
    for f,t in edges:
        length += G.adj[f][t]['weight']
    return length


def _ofline_sample(G):
    """ Function that returns a sketch with r nearest number of seeds.
        r is a sample that depends on the number of nodes, of degree > 2, of the graph.
        Specifically for this version, a base 2 logarithmic sample is used.

    Parameters
    ----------
    G : NetworkX graph
        Directed and weigthed graph

    Returns
    -------
    dict : {node_1:[(seed_1,distance_1),...,(seed_r,distance_r)],...,node_i}
        sketch with r seeds

    Notes:
    -------
        It is possible that not all nodes have r amounts of seeds,
        this can happen if the node has no path to any seed.
        However this is not an error, because if that were to happen it means
        that the node is not connected to the graph or that it has no output edges, so
        there cannot be a path from that node to the others (but to it if it only has input edges).

        The function is only adapted for weighted directed graphs. However it is easily
        generalize it for undirected (unweighted) graphs.

    See More
    --------
        http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.167.9222&rep=rep1&type=pdf
    """
    r = math.floor(math.log2(G.number_of_nodes()))
    degrees = dict(G.degree())
    nodes_v = list(degrees.keys())
    sum_d = sum(degrees.values())
    probs = [x / sum_d for x in degrees.values()]
    sets = [set(np.random.choice(nodes_v, size=2**i, p=probs,replace=False)) for i in range(r)]
    sketches = {}
    directed = [("in",True), ("out",False)]
    for s in sets:
        for d,b in directed:
            path = generic.dijkstra_multisource(G, list(s), in_edges=b)
            try:
                sketches[d]
            except KeyError:
                sketches[d] = defaultdict(list)
            for k,v in path.items():
                sketches[d][k].append(v)
    return sketches
