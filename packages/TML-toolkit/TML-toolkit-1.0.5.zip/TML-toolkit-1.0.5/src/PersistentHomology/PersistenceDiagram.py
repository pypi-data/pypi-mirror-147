import time
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt

class PersistenceDiagram:
    """
        Class for handling computation of persistence diagrams from a boundary matrix.
        Takes as input a boundary matrix represented as the sparse boundary matrix given by classes
        in the FilteredSimplicialComplexes file. That is, a list of sublist (See documentation in
        @class -> Vietoris-RipsComplex for more details).

        Attributes
        ----------
        lowest : list
            - List where each entry gives the index of the last '1' in the corresponding column
            of the boundary matrix.

        simplex_type : np.array
            - 1-d array where each entry indicates the dimension of the homotopy of the corresponding point in
            the diagram

        lowest_is_at : dict
            - A dictionary that a row number to the column where this index is the lowest.

        Methods
        -------
        transform(boundary_matrix, timer)
            Transforms a boundary matrix with the Persistent Homology Reduction Algorithm.

        getBarCodes(births, dims, fixed_length)
            Extraxts the persistence diagram from the reduced boundry matrix.

        plot()
            Visualize the persistence diagrams.
        """

    def __init__(self):
        pass

    def transform(self, boundary_matrix, timer = False):
        """
        Transforms a boundary matrix of a filtered simplicial complex into a reduced boundary matrix.
        The reduced matrix is represented in the same was as its input.

        Parameters
        ----------
        boundary_matrix : NxN matrix

        Returns
        -------
        Transformed NxN matrix

        """
        start = time.time()

        s = len(boundary_matrix)
        self.lowest = [0 for i in boundary_matrix]
        self.lowest_is_at = dict.fromkeys(list(range(len(boundary_matrix))), -1)
        self.simplex_type = np.zeros(s)

        for idx, col in enumerate(boundary_matrix):
            self.simplex_type[idx] = len(col)
            while 1 > 0:
                if len(col) > 0: # Not all zeros ...
                    low = np.max(col)
                    death_idx = self.lowest_is_at[low]
                    if  death_idx > 0:  # Featured already killed ...
                        new_col = np.append(boundary_matrix[death_idx], col)
                        counter = Counter(new_col)
                        keys = np.array([*counter])
                        col = keys[np.where(np.array([*counter.values()]) == 1)]
                        boundary_matrix[idx] = col
                    else:  # Feature got killed here
                        self.lowest[idx] = low
                        self.lowest_is_at[low] = idx
                        break
                else:
                    self.lowest[idx] = -1
                    break
        if timer:
            print('Reduced SBM in: ', time.time() - start)
        return boundary_matrix

    def getBarCodes(self, births, dims = [0,1], fixed_length = -1):
        """
        Extract barcodes from a persistence diagram.
        Features that never die will be set to die at final radius.

        Parameters
        ----------
        dims : List of Betti dimensions to include in diagram
        births : List of birth values

        Returns
        -------
        Nx3 array - [birth, death, dimension] by N
        """
        self.pi = []
        bar_codes = [] #np.zeros(shape=(len(self.lows), 2))
        dims = np.where(np.array(dims) < 1, -1, dims)
        for idx, [birth, dim] in enumerate(zip(births, self.simplex_type)):
            if dim - 1 not in dims or idx == 0:
                continue
            low = self.lowest[idx]
            if low == -1:
                death_idx = self.lowest_is_at[idx]
                death = births[death_idx]
                if death - birth > 0:
                    self.pi.append([idx, death_idx])
                    bar_codes.append([birth, death, dim])

        if fixed_length >= len(bar_codes): # Add points along the diagonal
            bar_codes.extend([[0,0,0],]*(fixed_length-len(bar_codes)))

        self.barcodes = np.array(bar_codes)
        return self.barcodes

    def plot(self):
        '''-----    Plots persistence diagram with y-axis as death and persistence    -----'''
        max_x = np.max(self.barcodes[:, :2].flatten())
        plt.scatter(*self.barcodes[:, :2].T)
        plt.plot([0, max_x], [0, max_x])
        plt.show()
        barcodes = self.barcodes.copy()
        barcodes[:, 1] -= barcodes[:, 0]
        plt.scatter(*barcodes[:, :2].T)
        plt.show()
