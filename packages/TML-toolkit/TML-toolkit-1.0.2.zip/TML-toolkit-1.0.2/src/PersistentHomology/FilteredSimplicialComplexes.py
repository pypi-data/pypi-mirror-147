import numpy as np
from scipy.spatial.distance import cdist
import itertools
import time


class VietorisRipsComplex:
    """
    Class for finding the Vietoris-Rips-complex of a dataset. Can use both euclidian- and
    the density based mutual-reachability distance.

    Attributes
    ----------
    filtered_complex : list
        - List of all simplices in the complex, each represented as a list of point indices, ordered by its birth value.

    birth_values : list
        - The corresponding birth values to the ordered list of simplices

    sbm: list
        - Sparse representation of the boundary matrix describing the filtered simplicial complex. Represented as a list of sub-lists
        where each sublist contains the indices of all non-zero entries its corresponding column of the boundary matrix.

    n : int
        - Size of the provided dataset

    points_from_edge : dict
        - Dictionary that gives the index of points connected by an edge of a given length.
        ASSUMES UNIQUE DISTANCES! (This is only used for computation of topological loss within this
        library, but it will create errors in the loss when distances are not unique, should be fixed in fututre update).

    distances : np.array
        - Sorted array of all edge lengths

    birth_order : dict
        - Dictionary describing the ordered index of a given edge length, equivalent to np.argsort(distances).

    Methods
    -------
    fit(self, data, d_matrix = [], max_dim = 1, density = False, k = 5, timer = False)
        - Finds the Rips-complex of the provided dataset.

    getBirth(simplex, data)
        - Utility: Method that finds the longest edge in a simplex

    mutual_reachability(data, k)
        - Utility: Computes the mutual reachability distance of the provided dataset
    """

    def __init__(self):
        pass

    # TODO transform/predict methods
    # TODO: d_matrix  =   [] er faktisk programerfeil, mutable default!!!
    def fit(self, data, d_matrix=None, max_dim=1, density=False, k=5, timer=False):
        """
        Creates a boundary matrix and a list of corresponding birth
        values to the simplices in the Vietoris-Rips Complex over a dataset.

        Parameters
        ----------
        data : np.array
            - Datapoints as [[x,y],...] of length N.

        d_matrix: np.array
            - Custom distance matrix. Defaults to [], in which case euclidian or mutual-reachability distance
            will be used for computation.

        max_dim : int
            - Finds the homologies of order (max-dim - 1) and lower, finds simplices
            of order max-dim

        density: bool
            - Determines whether to use a density based metric or euclidian metric.

        k: int
            - Hyperparameter of the density based mutual-reachability distance.

        Returns
        ----------
        NxN boundary matrix of the simplicial complex
        """
        if d_matrix is None:
            d_matrix = []
        start = time.time()

        self.n = data.shape[0]
        if len(d_matrix) < 1:
            d_matrix = self.mutual_reachability(data, k) if density else cdist(data, data)
        points = list(range(self.n))

        m_edges = np.array(np.triu_indices(len(data), 1)).T
        edges = m_edges[:, 1] + m_edges[:, 0] * len(data)

        '''-----    Create a dictionary giving the ordered index of a given edge length    ----'''
        self.points_from_edge = {0: []}
        distances = d_matrix.flatten()[edges]
        self.distances = np.sort(np.append(d_matrix.flatten()[edges], 0))
        self.birth_order = dict()  # Dictionary telling the index of edge length

        for i, [d, p] in enumerate(zip(distances, m_edges)):
            self.points_from_edge[d] = p

        for i, d in enumerate(self.distances):
            self.birth_order[d] = i

        simplicial_complex = list(range(len(data)))  # List of all simplices represented by their boundaries
        birth_edge = [0, ] * len(data)  # List of births given by index of longest edge

        '''-----    Initialize a dictionary assigning an index to each simplex    -----'''
        simplex_indices = dict()
        for i in range(len(data)):
            simplex_indices[frozenset([i])] = i

        '''-----    Append simplices and their corresponding birth value to the lists    -----'''
        i = len(data)
        for dim in range(2, max_dim + 2):  # For each dimension ...
            simplices = np.array(list(itertools.combinations(points, dim)))
            for simplex in simplices:  # For each simplex of this dimension ...
                simplex = list(simplex)
                simplex_indices[frozenset(simplex)] = i  # Assign some representative index to all simplices

                '''-----    Find boundary representation of simplex  -----'''
                boundaries = np.array(list(itertools.combinations(simplex, dim - 1)))
                b_simplex = []
                for b in boundaries:
                    b_simplex.append(simplex_indices[frozenset(b)])

                '''-----    Append to lists    -----'''
                simplicial_complex.append(b_simplex)
                birth_edge.append(self.getBirth(simplex, d_matrix) + 0.0001 * dim)
                i += 1

        '''-----    Reorder simplices in terms of birth values    -----'''
        order = np.argsort(birth_edge)
        birth_values = np.sort(birth_edge)
        simplicial_complex = [simplicial_complex[i] for i in order]
        self.filtered_complex = simplicial_complex
        self.birth_values = [self.distances[int(i)] for i in birth_values]

        inverse_order = dict()
        for i, j in enumerate(order):
            inverse_order[j] = i

        '''-----    Create sparse boundary matrix    -----'''
        self.sbm = [[], ] * len(simplicial_complex)
        for i, boundary in enumerate(self.filtered_complex[self.n:]):
            col = []
            for j in boundary:
                col.append(inverse_order[j])
            self.sbm[i + self.n] = np.array(col)

        if timer:
            print('Found complex as SBM in: ', time.time() - start)
        return self.sbm

    def getBirth(self, simplex, data):
        """
        Parameters
        ----------
        simplex : A d-simplex represented as d nodes
        data : Data matrix

        Returns
        ----------
        The ordered index of the longest edge in the simplex

        """
        max = 0
        for idx, n1 in enumerate(simplex):
            for n2 in simplex[idx:]:
                dist = data[n1, n2]
                if dist > max:
                    max = dist
        return self.birth_order[max]

    def mutual_reachability(self, data, k):
        """
        Computes the distance matrix of a given pointset using the mutual-reachability
        distance as described in: https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html.
        Parameters
        ----------
        data : np.array
            - Set of datapoints
        k : int
            - Hyperparameter, sets minimum distance to the k'th nearest neighbour.

        Returns
        -------

        """
        cores = [np.sort(row)[k + 1] for row in data]  # Add 1 to adjust for distance to self
        d_matrix = np.zeros(shape=data.shape)
        d = len(data)
        for i in range(d):
            for j in range(i):
                dist = np.max(cores[i], cores[j], data[i, j])
                d_matrix[i, j] = dist
                d_matrix[j, i] = dist
        return d_matrix
