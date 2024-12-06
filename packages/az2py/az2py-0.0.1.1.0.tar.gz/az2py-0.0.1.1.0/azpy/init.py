import networkx as nx
import numpy as np
import itertools

def resistance_calculator(n):
    for i in range(n):
        for j in range(i + 1, n):
           Rij = (P[i, i] + P[j, j] - 2 * P[i, j]) * R
           total_sum += Rij
           return(f'R({i + 1},{j + 1})={Rij:.3f}\n')


def full_adjacency(G):
    return(nx.to_numpy_array(G))

def diagonal(A):
    return(np.diag(np.sum(A, axis=1)))

def laplacian(A,D):
    return(D - A)

def inverse(P):
    return np.linalg.pinv(L)
