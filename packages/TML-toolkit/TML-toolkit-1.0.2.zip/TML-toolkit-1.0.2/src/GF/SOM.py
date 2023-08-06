from src.Utility import GraphTools as gt
import numpy as np
import matplotlib.pyplot as plt


class SOM:
    """
    Class for creating Self Organizing Maps as described in paper by Kohonen, 1982.
    Finds a node embedding that fits the graph to some data distribution.
    Can be used on datasets in any-dimensional spaces.

    Attributes
    ----------
    graph : GraphTools.Graph-object
        - A graph object that gets organized to fit the data provided

    Methods
    -------
    fit(data, lr, epochs, nodes)
        - Fits the graph to the data

    transform(data):
        - Maps all data-points to the closest node in the graph.

    neighbourhood(v1, f)
        - Utility: Method that finds the closest node to a given point and its topological neighbours.
    """

    def __init__(self, adjacency_matrix, nodes=None):
        """
        Initialize a Self Organizing Map with a graph. The graph is given by an adjacency
        matrix and a set of points indicating the initial embedding of the nodes.

        Parameters
        ----------
        adjacency_matrix : np.array
            - Array of shape N x N describing adjacent nodes in the graph

        nodes : np.array
            - Array of shape N x d specifying the initial node embedding
        """
        self.graph = gt.Graph(nodes, adjacency_matrix=adjacency_matrix)

    def fit(self, data, lr=0.02, epochs=15, nodes=[], neighbour_factor=0.1):
        """
        Fits the embedding of the graph-nodes to match the given data.

        Parameters
        ----------
        data : np.array
            - Array of size N x d, where N is the number of points and d is the dimension of the
            space

        lr : float
            - Determining factor for the step size with each update

        epochs : int
            - The number of iterations through the entire dataset

        nodes : np.array - OPTIONAL
            - An array describing an embedding of nodes (See __init__() for info).
            If given input of length 0 this function will use the nodes given in __init__().
            DEFAULT: []
        """

        if len(nodes) == 0:
            nodes = self.graph.getNodeEmbedding()

        '''-----    Organize Node Embedding    -----'''
        for epoch in range(epochs):
            for count, point in enumerate(data):
                # Compute distance to all nodes and find closest ...
                dist_vectors = nodes - point
                distances = np.linalg.norm(dist_vectors, axis=1)
                closest = np.argmin(distances, axis=0)

                # Update the vectors accordingly ...
                nodes -= (lr * dist_vectors.T * self.neighbourhood(closest, neighbour_factor)).T
                self.graph.updateNodeEmbedding(nodes)

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
        node_assignment = dict.fromkeys(range(0,len(self.graph.getNodes())), [])
        for idx, point in enumerate(data):
            closest = np.argmin(np.linalg.norm(self.graph.node_embedding - point, axis=1))
            if len(node_assignment[closest]) < 1:
                node_assignment[closest] = [idx]
            else:
                node_assignment[closest].append(idx)

        for i in node_assignment.keys():
            plt.scatter(*data[node_assignment[i]].T)
        self.graph.plot()
        plt.show()
        return node_assignment

    def neighbourhood(self, v1, f):
        """
        Neighbourhood-function that includes the closest neighbour and its topological
        neighbours. The later are updated by a fixed fraction of what the closest neighbour is.

        Parameters
        ----------
        v1 : int
            - Datapoint to find closest neighbour of

        f : float
            - Factor determening the stepsize of neighbours to the closest point

        Returns
        -------
            np.array() of shape 1 x N
        """
        h_table = np.zeros(len(self.graph.node_embedding))
        h_table[v1] = 1
        ns = self.graph.getNeighbour(v1)
        h_table[ns] = f
        return h_table
