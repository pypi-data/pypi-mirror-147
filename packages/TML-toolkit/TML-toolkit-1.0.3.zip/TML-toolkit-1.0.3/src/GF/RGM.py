import matplotlib.pyplot as plt
import numpy as np
from .GraphTools import Graph
from sklearn.cluster import DBSCAN

class ReebGraphMapper:


    def fit(self, data, k, i, filter = None,  min_samples = 2, plot = False):
        # Define intervals

        self.graph = Graph()

        c = self.define_intervals(k, i)

        # Map trough filter function
        # Store based on intervall it is contained in, call them c_i
        if filter == None:
            mapping = x_value_filtration(data)
        else:
            mapping = filter(data)

        mapping -= np.min(mapping)
        mapping /= np.max(mapping)

        c_i = []
        for i in range(k):
            c_i.append(np.where((mapping >= c[i, 0]) & (mapping <= c[i, 1]))[0])

        # For each c_i: cluster points and return number of components
        clusters = {}

        for points in c_i:
            c_labels = DBSCAN(min_samples= min_samples).fit_predict(data[points])
            for i in range(np.max(c_labels) + 1):
                c_points = np.where(c_labels == i)[0]
                neigbours = []
                for p in points[c_points]:
                    for key in clusters.keys():
                        if p in clusters[key]:
                            neigbours.append(key)
                cluster_center = np.mean(data[points[c_points]], axis=0)
                self.graph.addNode(cluster_center, neigbours)
                clusters[len(clusters.keys())] = points[c_points]

        if plot:
            plt.scatter(*data.T)
            self.graph.plot()

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
        node_assignment = dict.fromkeys(range(0, len(self.graph.getNodes())), [])
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

    def define_intervals(self, k, i):
        length = 1 / (k - k * i + i)
        margin = length - 1 / k
        intervals = np.zeros(shape=(k, 2))
        intervals[0] = [0, length]
        for i in range(1, k):
            intervals[i, 0] = max(intervals[i - 1] - (margin + margin / (k - 1)))
            intervals[i, 1] = intervals[i, 0] + length

        return intervals

def x_value_filtration(data):
    return data[:, 0]
