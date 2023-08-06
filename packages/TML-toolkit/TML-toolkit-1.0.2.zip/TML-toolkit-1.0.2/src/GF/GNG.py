import numpy as np
from src.Utility import GraphTools as gt
import matplotlib.pyplot as plt
import matplotlib.colors as colors

class GrowingNeuralGas:
    """
    Class for creating a Growing Neural Gas as described in the paper by Fritzke, 1994.
    Given a dataset this class aims to find a graph structure and a node embedding in the feature
    space of the data that preserves the topology of the underlying manifold from which the data
    was sampled.

    Attributes
    ----------
    graph : GraphTools.Graph-object
        - A graph object that is fitted the data provided

    Methods
    -------
    fit(self, data, lr, epochs, max_age, m, gamma, B, e_n, nello_version)
        - Grows the graph to math the data provided.

    transform(data):
        - Maps all data-points to the closest node in the graph.
    """

    graph = None
    errors = []

    def __init__(self):
        """
        Initialize a graph consisting of two nodes with an edge between them
        """
        self.graph = gt.Graph(nodes=np.array([[0., 0.], [1., 1.]]), adjacency_matrix=np.array([[-1, 0], [0, -1]]))
        self.errors = [0, 0]

    def fit(self, data, lr=0.01, epochs=15, max_age=100, m=500, gamma=0.9, B=0.1, e_n=0.1, nello_version=True):
        """
        Finds a graph-structure matching the datapoints provided.

        Parameters
        ----------
        data : np.array
            - Array of shape N x d, where N is the number of points and d is the dimentions
            of the space

        lr : float
            - Determining factor for the step size with each update

        epochs : int
            - The number of iterations through the entire dataset

        max_age : int
            - Hyperparameter determining the maximum age of an edge before it is removed

        m : int
            - Hyperparameter determining the number of iterations between the addition of
            a new node

        gamma : float
            - Hyperparameter determining the error-reduction at each step

        B : float
            - Hyperparameter determining the error-increase at the chosen node

        e_n : float
            - Hyperparameter determining the degree of which topological neighbours are shifted
            relative to the closest nodes.

        nello_version : bool
            - If True shifts only the two closest neighbours, else also moves the neighbours by a
            factor given by param: e_n
        """
        counter = 0

        nodes = self.graph.getNodeEmbedding()

        '''-----    Find graph structure    -----'''
        for epoch in range(epochs):
            for count, point in enumerate(data):

                counter += 1

                '''-----    Compute distance to all nodes and find closest  -----'''
                d_vec = nodes - point
                dists = np.linalg.norm(d_vec, axis=1)
                closest1, closest2 = np.argsort(dists, axis=0)[:2]

                '''-----    Update embedding and errors     -----'''
                self.errors[closest1] += dists[closest1]

                nodes[closest1] -= lr * d_vec[closest1]
                if nello_version:  # Update embedding of 2 closest only
                    nodes[closest2] -= lr * d_vec[closest2]
                else:  # Update embedding of all topological neighbours of closest1
                    for n in self.graph.getNeighbour(closest1):
                        nodes[n] -= lr * d_vec[n] * e_n

                '''-----    Update edges    -----'''
                new = True
                for neighbour, age in enumerate(self.graph.adjacency_matrix[closest1]):
                    if age < 0:  # if there is no edge ...
                        continue
                    elif neighbour == closest2:
                        self.graph.updateConnection([closest1, neighbour], 0)
                        new = False
                    elif neighbour != closest1:
                        age = self.graph.adjacency_matrix[neighbour, closest1]
                        if age >= max_age:
                            self.graph.updateConnection([closest1, neighbour], -1)
                        else:
                            self.graph.updateConnection([closest1, neighbour], age + 1)
                if new:
                    self.graph.updateConnection([closest1, closest2], 0)

                '''-----    Remove unconnected nodes    -----'''
                ref = np.ones(len(self.errors)) * (-1)
                id = np.where(np.all(self.graph.adjacency_matrix == ref, axis=1))[0]
                for i in id.tolist():
                    self.graph.removeNode(i)
                    self.errors.pop(i)

                '''-----    Add nodes   -----'''
                if counter % m == m - 1:
                    worst = np.argmax(self.errors)
                    ns = self.graph.getNeighbour(worst)
                    worst_neighbour = ns[np.argmax(np.array(self.errors)[ns])]

                    self.errors[worst] *= B
                    self.errors[worst_neighbour] *= B
                    self.graph.addNode(
                        (self.graph.node_embedding[worst] + self.graph.node_embedding[worst_neighbour]) / 2,
                        [worst, worst_neighbour])
                    self.graph.updateConnection([worst, worst_neighbour], -1)
                    self.errors.append(self.errors[worst])
                    nodes = self.graph.getNodeEmbedding()

                '''----- Update errors  -----'''
                self.errors = list(np.array(self.errors) * gamma)

        print('Nodes: ', len(self.errors))
        print('Edges: ', len(np.where(self.graph.adjacency_matrix.flatten() >= 0)[0]))

    def transform(self, data):
        """
        Maps every point in the dataset to the closest node in the graph.
        Parameters
        ----------
        data : np.array
            - Set of data-points

        Returns
        -------
            Dictionary which assigns a list of the indices of all points closest to a node, which
            is itself referenced by its index in the graph.node_embedding.
        """
        nodes = len(self.graph.getNodes())
        node_assignment = dict.fromkeys(range(0, nodes), [])
        for idx, point in enumerate(data):
            closest = np.argmin(np.linalg.norm(self.graph.node_embedding - point, axis=1))
            if len(node_assignment[closest]) < 1:
                node_assignment[closest] = [idx]
            else:
                node_assignment[closest].append(idx)

        colors_list = list(colors._colors_full_map.values())
        for s, i in enumerate(node_assignment.keys()):
            plt.scatter(*data[node_assignment[i]].T, color = colors_list[(3*s)%1163])
        self.graph.plot()
        plt.show()
        return node_assignment