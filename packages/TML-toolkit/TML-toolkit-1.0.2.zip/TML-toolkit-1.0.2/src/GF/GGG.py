import numpy as np
from src.Utility import GraphTools as gt
import matplotlib.pyplot as plt

from scipy.spatial import Delaunay
from src.GF.GMM import GausianMixtureModel as GMM


class GenerativeGaussianGraph:
    """
        A class for Generative Gaussian Graphs as described in the paper by Aupetit, 2005.
        Utilizes the @class -> GaussianMixtureModel. Finds a graph from with new samples that matches the
        distribution of the provided data can be generated. Generate function is given by the GMM.

        Attributes
        ----------
        GMM : GausianMixtureModel()
            The GMM from which data is can be generated. Use self.GMM.generate() to sample from the GGG.

        Methods
        -------
        fit(data, k, c_epochs, epochs)
            Creates a Gaussian Graph with k nodes.
        """

    def __init__(self):
        self.GMM = None

    def fit(self, data, k, c_epochs=10, epochs=10):
        """
        Creates a Gausian Graph with k nodes and performs the EM algorithm 2 times. First
        for the initial embedding of the graph nodes. Secondly, to optimize variance and
        relative cluster/edge probability.

        Parameters
        ----------
        data : np.array
            - The dataset to fit a GGG to in order to generate more samples like it.
        k : int
            - Number of nodes in the generative graph
        c_epochs :
            - Number of EM steps to take in the initial embedding of the nodes.
        epochs :
            - Number of EM steps to take in the optimization of the generative graph.
        """
        upper_bounds = np.amax(data, axis=0)
        lower_bounds = np.amin(data, axis=0)
        nodes = (np.random.rand(k, data.shape[1]) * (upper_bounds - lower_bounds)) + lower_bounds

        '''-----    Use the GMM EM-algorithm to do centroid based clustering and find a node embedding      -----'''
        gmm = GMM(data, len(nodes))
        gmm.EM_algorithm(data, epochs=c_epochs)
        nodes = gmm.cluster_means

        plt.scatter(*data.T)
        plt.scatter(*nodes.T, s=200)
        plt.show()

        a = Delaunay(nodes)
        graph = gt.Graph(nodes=nodes)
        for simplex in a.simplices:
            graph.updateConnection([simplex[0], simplex[1]], 0)
            graph.updateConnection([simplex[1], simplex[2]], 0)
            graph.updateConnection([simplex[0], simplex[2]], 0)

        '''-----    Run another GMM with GGG == True     -----'''
        edges = gt.getEdgeList(graph.adjacency_matrix)

        plt.scatter(*data.T)
        graph.plot()
        gmm.transform(data)

        self.GMM = GMM(data, len(nodes), segments=edges,
                       means=nodes, GGG=True)
        self.GMM.EM_algorithm(data, epochs=epochs)

        self.GMM.transform(data)
