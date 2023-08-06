import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial
import time
from scipy.stats import multivariate_normal as norm
from scipy.special import erf


class GausianMixtureModel:
    """
        A class for Gaussian Mixture Models used as a supplement for the Generative Gaussian Graph class.
        The fit function runs the Expecation-Maximation algorithm on both sets of points (nodes) but also on
        entire graphs (points and linesegments / edges).

        The @input -> GGG is ment to decide whether or not
        to run a standard EM or run it on a graph with edges as well. The standard method is implemented for
        covariance matrixes as representation of the variances of each gaussian model, while the GGG-version
        only allows for spherical variance which is equal for all gaussians (as described in the paper), this is represented by a float.

        Attributes
        ----------
        cluster_means : np.array
            - Array of shape N x d defining the centers of the gaussian distributions
            N is the number of clusters and d is the dimensions of the space

        cluster_segments : np.array
            - Array of shape M x 2, containing the edges of the graph referenced by the
            indices of the nodes is conects. M is the number of edges.

        cluster_variances : List[np.array] / Int
            - If working with graphs (nodes and edges -> GGG == True) variances is an
            Integer applying for all segments and cluster centers. If not, cluster variances
            is a list of covariance matrixes.

        cluster_probs : np.array
            - An array of shape 1 x N+M giving the probability of each cluster mean and segment
            ordered by index where all edges have higher index than the centers.

        clusters : List[List[int]]
            - List of k lists containing the indexes of all datapoints assigned to each cluster.

        expectations : np.array
            - Array of shape D x N+M containing the expectations of each datapoints belonging
            to each node and edge of the graph. D is the number of datapoints, N is the number
            of nodes and M is the number of edges.

        g_1 : np.array
            - Array of shape D x M containing the un-normalized expectations of the edges

        k : int
            - Number of cluster centers

        s : int
            - Number of edges

        Methods
        -------
        EM_algorithm(data, epochs)
            Fits a Gausian Mixture Model to a given dataset using the EM algorithm.

        generate(n)
            Generates data according to the already fitted Gassian Mixture Model. Can be used both with
            regular Gausian Mixture Models and GGG's.

        e_step(data)
            Utility: Runs the expectations step of the EM algorithm

        m_step(data)
            Utility: Performs the maximization step of the EM algorithm

        line_segment_pdf(points, n1, n2, cov, L)
            pass

        sigma_update(data)
            pass

        transform(data):
            Maps all data-points to the closest node in the graph.

        plot(data)
            Visualizes the GMM through the clusters given by getClusters()

        Utility Methods: Q(), q(), L(), I1(), I2() are all described in the paper:
        Aupetit, 2005, 'Learning Topology with the Generative Gaussian Graph and
        the EM algorithm', pp. 4-5.
        """

    cluster_means = []
    cluster_segments = []
    cluster_variances = []
    cluster_probs = []
    clusters = []
    expectations = []
    g_1 = []
    k = 0
    s = 0

    def __init__(self, data, num_nodes, means=[], segments=[], variances=[], GGG=False):
        self.k = num_nodes
        self.s = len(segments)
        self.GGG = GGG

        '''-----    Initialize variables according depending on whether we are running standard EM
           -----    or EM on graphs    -----'''
        if not GGG:
            if means == []:
                new_X = np.array_split(data, self.k)
                self.cluster_means = np.array([np.mean(x, axis=0) for x in new_X])
            else:
                self.cluster_means = means

            if variances == []:
                self.cluster_variances = [np.cov(x.T, ddof=0) for x in new_X]
                del new_X
            else:
                self.cluster_variances = variances
        else:
            self.cluster_variances = 1
            self.cluster_means = means

        self.L_table = scipy.spatial.distance_matrix(self.cluster_means, self.cluster_means)
        self.cluster_segments = segments
        self.cluster_probs = np.ones(shape=(self.k + self.s, 1)) / (self.k + self.s)

    def EM_algorithm(self, data, epochs=100):
        """
        Performs a number of EM steps to optimize a Gaussian Mixture Model or GGG to
        the given dataset.

        Parameters
        ----------
        data : np.array
            - Dataset to which we apply the mixture model

        epochs : int
            - Number of EM steps to perform.

        """
        e_time = 0
        m_time = 0
        for i in range(epochs):
            start = time.time()
            self.e_step(data)
            end = time.time()
            e_time += end - start
            self.m_step(data)
            end2 = time.time()
            m_time += end2 - end
        print('E_time: ', e_time)
        print('M_time: ', m_time)

    def generate(self, n):
        """
        Generates new samples from the GMM

        Parameters
        ----------
        n : int
            - Number of samples to generate

        Returns
        -------
            np.array of shape n x d. Dataset of newly generated samples
        """

        new_data = np.zeros(shape=(n, self.cluster_means.shape[1]))
        for i in range(n):
            obj = np.random.choice(np.arange(0, len(self.cluster_probs)), p=np.array(self.cluster_probs).flatten())
            if obj >= self.k:  # We are generating from an edge:
                start = self.cluster_means[self.cluster_segments[obj - self.k][0]]
                end = self.cluster_means[self.cluster_segments[obj - self.k][1]]
                pos = start + np.random.uniform(0, 1) * (end - start)
                point = pos + np.random.normal([0, 0], np.sqrt(self.cluster_variances))
            else:  # We are generating from a point
                if self.GGG:
                    point = np.random.normal(self.cluster_means[obj], np.sqrt(self.cluster_variances))
                else:
                    point = np.random.multivariate_normal(self.cluster_means[obj],
                                                          np.sqrt(np.abs(self.cluster_variances[obj])))
            new_data[i] = point
        return new_data

    def e_step(self, data):
        """
        Performs a calculation of the expectations as a step in the EM algorithm.

        Parameters
        ----------
        data : np.array
            - Dataset to which we apply the mixture model

        Returns
        -------
            np.array of shape D x N+M describing the expectations of each datapoint being sampled from each node or edge
            of the graph
        """
        probs = np.zeros((len(data), self.k + self.s))
        self.g_1 = np.zeros((len(data), self.s))

        if not self.GGG:
            for node, [mean, variance, pi] in enumerate(
                    zip(self.cluster_means, self.cluster_variances, self.cluster_probs[:self.k])):
                distribution = norm(mean, variance)
                probs[:, node] = distribution.pdf(data) * pi

        else:
            # Expectation of nodes
            std = np.sqrt(self.cluster_variances)
            for node, [mean, pi] in enumerate(zip(self.cluster_means, self.cluster_probs[:self.k])):
                distribution = norm(mean, std)
                probs[:, node] = distribution.pdf(data) * pi

            # Exspectation of edges
            for idx, point in enumerate(data):
                for edge_idx, [edge, pi] in enumerate(zip(self.cluster_segments, self.cluster_probs[self.k:])):
                    col_nr = edge_idx + self.k
                    L = self.L(edge[0], edge[1])
                    n1 = self.cluster_means[edge[0]]
                    n2 = self.cluster_means[edge[1]]
                    p = self.line_segment_pdf(point, n1, n2, std, L)
                    probs[idx, col_nr] = p * pi
                    if p == 0:
                        p = np.finfo(float).eps
                    self.g_1[idx, edge_idx] = p

        probs = (probs.T * 1 / np.sum(probs, axis=1)).T
        self.expectations = probs
        return probs

    def m_step(self, data):
        """
        Performs an update of the model parameters as a step in the EM algorithm based on the expectations from the
        last e_step().

        Parameters
        ----------
        data : np.array
            - Dataset to which we apply the mixture model
        """

        m = np.sum(self.expectations)

        m_c = np.sum(self.expectations, axis=0)

        if not self.GGG:
            for cluster in range(self.k):
                self.cluster_probs[cluster] = m_c[cluster] / m
                self.cluster_means[cluster] = np.sum((data.T * self.expectations[:, cluster]).T, axis=0) / m_c[cluster]
                self.cluster_variances[cluster] = np.cov(data.T,
                                                         aweights=self.expectations[:, cluster])  # / m_c[cluster]
        else:
            self.cluster_probs = m_c / m
            self.cluster_variances = np.abs(self.sigma_update(data))

    def line_segment_pdf(self, point, n1, n2, cov, L):
        """
        Function for handling the pdf of a line segment in the graph.

        Returns
        -------
        object
        """
        D = len(point)
        Q = self.Q(point, n1, n2, L)
        q = self.q(n1, n2, Q, L)
        dist = point - q
        a = (np.exp((-np.dot(dist, dist)) / (2 * (cov)))) / ((2 * np.pi * cov) ** ((D - 1) / 2))
        b = (erf(Q / (cov * np.sqrt(2))) - erf((Q - L) / (cov * np.sqrt(2)))) / (2 * L)
        return a * b

    def sigma_update(self, data):
        """
        Updates the variances of the models.

        Parameters
        ----------
        data : np.array
            - Dataset to which we apply the mixture model

        Returns
        -------
            The new cluster_variances (See class description for more detailed info on cluster_variances)
        """
        new_v = np.array(self.cluster_variances) * 0
        for idx, point in enumerate(data):
            p_0__point = self.expectations[:, :self.k]
            distances = (point - (self.cluster_means)) ** 2
            node_sum = np.sum(np.dot(p_0__point[idx], distances))

            edge_sum = np.array(self.cluster_variances) * 0
            p_1__point = self.expectations[:, self.k:]
            var = self.cluster_variances
            std = np.sqrt(self.cluster_variances)
            for i, [n1, n2] in enumerate(self.cluster_segments):
                L = self.L(n1, n2)
                n1 = self.cluster_means[n1]
                n2 = self.cluster_means[n2]
                Q = self.Q(point, n1, n2, L)
                dis = point - self.q(n1, n2, Q, L)
                distances_1 = (2 * np.pi * var) ** (-data.shape[1] / 2) * np.exp(
                    -(np.dot(point - self.q(n1, n2, Q, L), point - self.q(n1, n2, Q, L))) / (2 * var))
                distances_2 = (self.I1(std, Q, L) * (np.dot(dis, dis) + var)) + self.I2(Q, L)
                distances_3 = L * self.g_1[idx, i]
                distances = (distances_1 * distances_2) / distances_3

                edge_sum += p_1__point[idx, i] * distances
            new_v += (node_sum + edge_sum)
        new_v /= (data.shape[0] * data.shape[1])
        return new_v

    def Q(self, point, n1, n2, L):
        return np.dot(point - n1, n2 - n1) / L

    def q(self, n1, n2, Q, L):
        return n1 + (n2 - n1) * (Q / L)

    def L(self, n1, n2):
        return self.L_table[n1, n2]  # np.linalg.norm(n2-n1)

    def I1(self, std, Q, L):
        a = erf(Q / (std * np.sqrt(2)))
        b = erf((Q - L) / (std * np.sqrt(2)))
        return std * np.sqrt(np.pi / 2) * (a - b)

    def I2(self, Q, L):
        c = Q - L
        a = (c) * np.exp(-((np.dot(c, c)) / (2 * self.cluster_variances)))
        b = Q * np.exp(-(np.dot(Q, Q) / (2 * self.cluster_variances)))
        return self.cluster_variances * (a - b)

    def transform(self, data):
        """
        Maps every point in the dataset to the closest node in the graph.
        Parameters
        ----------
        data : np.array
            - Set of data-points

        Returns
        -------
            List of arrays, where each array contains the indices of datapoints
            assigned to the node with corresponding index to the array.
        """
        a = np.argmax(self.expectations, axis=1)
        self.clusters = [[], ] * self.k
        for i in range(self.k):
            self.clusters[i] = np.where(a == i)[0]
        self.plot(data)
        return self.clusters

    def plot(self, data):
        for c in range(self.k):
            plt.scatter(*data[self.clusters[c]].T)
        for i, txt in enumerate(self.cluster_means):
            plt.annotate(i, (self.cluster_means.T[0][i], self.cluster_means.T[1][i]))
        plt.show()
