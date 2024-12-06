import numpy as np
import pandas as pd
import networkx as nx

class azpy:

    def __init__(self):
        self.name = "azpy"
    
    def process_data(self, data):
        if isinstance(data, pd.DataFrame):
            return data.describe()
        elif isinstance(data, np.ndarray):
            return np.mean(data, axis=0)
        else:
            raise TypeError("Data must be a pandas DataFrame or numpy array")

    def create_network(self, edges):
        G = nx.Graph()
        G.add_edges_from(edges)
        return G
    
    def resistance_calculator(self, n):
        total_sum = 0  # اضافه کردن مقدار اولیه برای total_sum
        for i in range(n):
            for j in range(i + 1, n):
               Rij = (P[i, i] + P[j, j] - 2 * P[i, j]) * R
               total_sum += Rij
               return f'R({i + 1},{j + 1})={Rij:.3f}\n'

    def full_adjacency(self, G):
         return nx.to_numpy_array(G)

    def diagonal(self, A):
        return np.diag(np.sum(A, axis=1))

    def laplacian(self, A, D):
         return D - A

    def inverse(self, P):
        return np.linalg.pinv(L)