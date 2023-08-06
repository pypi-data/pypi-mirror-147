import numpy as np
import matplotlib.pyplot as plt


class PersistanceLandscapes:
    """
        Class for vectorizing persistence diagrams as persistence landscapes.

        Methods
        -------
        transform(persistence_pairs):
            Computes the persistence landscapes given a diagram.
    """

    def transform(self, persistence_pairs):
        """
        Transforms a persistence diagram into a persistence landscape.

        Parameters
        ----------
        persistence_pairs : np.array
            - D x 2 array, where D is the number of points in the diagram. Each row contains
            a birth and a death.

        Returns
        -------
            Dictionary where each element contains points ordered by x-value indicating the lines
            at each level of the landscape.
        """
        persistence_pairs[:, 2] -= persistence_pairs[:, 0]  # Get birth, persistence values
        lambda_k = {0: [np.array([0, 0])]}
        relevant_points = persistence_pairs[:, :2]  # All triangle tops
        k = 0
        while 1>0:
            if len(relevant_points) < 1:
                break
            starting_order = np.argsort(relevant_points[:, 0] - relevant_points[:, 1])  # Sort based on start of triangle
            new_tops = []
            for p2 in relevant_points[starting_order]:
                p1 = lambda_k[k][-1]
                p1_stop = np.array([p1[0] + p1[1], 0])
                if p1[0] > p2[0]:
                    new_tops.append(p2)
                    continue
                if p1[1] == 0:
                    lambda_k[k].append(p2)
                    continue
                p2_start = np.array([p2[0] - p2[1], 0])
                p2_stop = np.array([p2[0] + p2[1], 0])
                if p2_start[0] <= p1_stop[0]:  # It starts before our current position has ended ...
                    if p2_stop[0] >= p1_stop[0]:   # They intersect
                        height = (p1_stop[0] - p2_start[0])/2
                        x = p2_start[0] + height
                        y = height
                        lambda_k[k].append(np.array([x,y]))
                        lambda_k[k].append(p2)
                        new_tops.append([x,y])
                    else:
                        new_tops.append(p2)
                else:
                    lambda_k[k].append(p1_stop)
                    lambda_k[k].append(p2_start)
                    lambda_k[k].append(p2)

            if lambda_k[k][-1][1] != 0.:
                lambda_k[k].append(np.array([np.sum(lambda_k[k][-1]), 0]))
            relevant_points = np.array(new_tops)
            k += 1
            lambda_k[k] = [np.array([0,0])]

        for idx, key in enumerate(lambda_k.keys()):
            if len(lambda_k[key]) < 2:
                del lambda_k[key]
                break
            lambda_k[key][0] = np.array([lambda_k[key][1][0] - lambda_k[key][1][1], 0])
            lambda_k[key] = np.array(lambda_k[key])
            plt.plot(*lambda_k[key].T)
        plt.show()

        return lambda_k
