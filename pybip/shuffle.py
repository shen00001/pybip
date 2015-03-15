import networkx as nx
import numpy as np
import random


def connectance_shuffling(M):
    """
    Shuffle the edges of a graph while approximatively conserving
    connectance (C = L/N^2, with L the number of edges and N the
    number of nodes).

    Args:
        M: The biadjacency matrix.  

    Returns:
        The shuffled matrix. 
    """
    
    k_i = np.sum(M,0,dtype=float)/M.shape[0]
    k_j = np.sum(M,1,dtype=float)/M.shape[1]
    A = np.hstack([k_j.reshape(-1,1)]*M.shape[1]) + np.vstack([k_i]*M.shape[0])
    A /= 2 
    return A > np.random.random(size=A.shape)

def mcmc_shuffling(graph,N=None,inplace=False):
    """
    Shuffle the edges of a graph while conserving the node degree.

    Args:
        graph (nx.graph): The bipartite network.
        N (int): the number of (sucessfull) edges shuffling. If None is given,
            N is computed from the number of edges to have each edge choosen once
            with probability 0.999: ln(.001)/(ln(E-1)-ln(E)), with E the number of edges. 
        inplace (bool): return a copy of the graph if false, shuffle
            the graph inplace otherwise.

    Returns:
        (graph) the shuffled graph if inplace is True. 
    """
    
    if not inplace:
        graph = graph.copy()

    if N is None:
        E = graph.number_of_edges()
        N = int( np.log(0.001) / (np.log(E-1)-np.log(E)) )

    success = 0
    while success <= N:
        E = graph.edges()
        a,b = random.sample(E,2)
        if (a[0],b[1]) not in E and (b[0],a[1]) not in E:
            graph.remove_edges_from((a,b))
            graph.add_edges_from(((a[0],b[1]),(b[0],a[1])))
            success += 1
    if not inplace:
        return(graph)

