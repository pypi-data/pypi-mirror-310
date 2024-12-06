import random

import networkx as nx

def list_init(G, colours, k, seed):
    """Assign a random subset of k colours to the list of permissible colours for every edge of G."""
    random.seed(seed)
    for u, v, permissible in G.edges.data("permissible"):
        G[u][v]["permissible"] = random.sample(colours, k)
        
    for u, v, colour in G.edges.data("colour"):
        G[u][v]["colour"] = None

    return(G)

def list_init_node(G, colours, k, seed):
    """Assign a random subset of k colours to the list of permissible colours for every node of G."""
    random.seed(seed)

    permissible_colours = [random.sample(colours, k) for i in range(G.order())]
    permissible_dict = dict(zip(G.nodes, permissible_colours))

    nx.set_node_attributes(G, permissible_dict, "permissible")
    nx.set_node_attributes(G, None, "colour")

    return(G)

def colours_incident_with(G, u):
    """The list of colours on edges incident with vertex u in graph G."""
    return(set([G[u][v]["colour"] for v in nx.neighbors(G, u)]))

def colours_on_neighbours(G, n):
    """The set of all colours on neighbours of a node n in a graph G."""
    return(set([nx.get_node_attributes(G, "colour")[m] for m in G.neighbors(n)]))

def first_permissible_or_none(G, u, v):
    """
    Returns the first element of A if A is non-empty otherwise returns None.
    Where A is P minus (X union Y).
    X is the list of colours on edges incident with u.
    Y is the list of colours on edges incident with v.
    P is the list of permissible colours for edge uv.
    """
    X = colours_incident_with(G, u)
    Y = colours_incident_with(G, v)
    P = set(G[u][v]["permissible"])
    choices = P - X.union(Y)
    if(len(choices) > 0):
        choice = list(choices)[0]
    else:
        choice = None
    return(choice)

def first_permissible_or_none_node(G, u, edges = False):
    """ Returns the first element of A = P - X if A is non-empty otherwise returns None.
    X is the list of colours on neighbours of u if edges = False and the union of
    the list of colours on neighbours of u and the list of colours on edges incident
    with u if edges = True.
    P is the list of permissible colours for node u.
    """
    if edges:
        X = colours_on_neighbours(G, u).union(colours_incident_with(G, u))
    else:
        X = colours_on_neighbours(G, u)
    P = set(G.nodes[u]["permissible"])
    choices = P - X
    if(len(choices) > 0):
        choice = list(choices)[0]
    else:
        choice = None
    return(choice)

def greedy_list_edge_colouring(G):
    """Assign the first permissible colour to every edge (or None if all permissible
    colours already used on incident edges)."""
    for u, v, colour in G.edges.data("colour"):
        G[u][v]["colour"] = first_permissible_or_none(G, u, v) # random.choice(colours)
    return(G)

def greedy_list_node_colouring(G, edges = False):
    """Assign the first permissible colour to every node or None if all permissible
    colours already used on neighbouring nodes (and incident edges if edges = True)."""
    for u in G.nodes:
        G.nodes[u]["colour"] = first_permissible_or_none_node(G, u, edges)
    return(G)

def greedy_list_total_colouring(G):
    """Use a greedy strategy to colour the edges of G and then use a greedy node colouring
    strategy to colour the nodes of G."""
    G = greedy_list_edge_colouring(G)
    G = greedy_list_node_colouring(G, edges = True)
    return(G)

def print_list_edge_colouring(G):
    """Print assigned colours and lists of permissible colours for all edges in G."""
    for n, nbrs in G.adj.items():
        for nbr, eattr in nbrs.items():
            perm = eattr['permissible']
            col = eattr['colour']
            print(f"({n}, {nbr}, {perm}, {col})")

