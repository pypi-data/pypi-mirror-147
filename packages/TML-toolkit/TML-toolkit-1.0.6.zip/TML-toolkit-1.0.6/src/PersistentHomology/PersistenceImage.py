import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mvn import mvnun


class PersistenceImage:
    """
    Class for computing PersistenceImages from persistence diagrams.
    Can handle input structured in the way described in @class -> PersistenceDiagram.

    Methods
    -------
    transform(self, bars, res = 50, var = 0.0001, plot = True)
        - Finds the image representation of given persistence diagram.
    """

    def transform(self, bars, res=50, var=0.0001, plot=True):
        """
        Parameters
        ----------
        bars : Nx3 array - [birth, death, dimension] by N
        res : Gives resolution of image as res x res
        var : Hyperparameter: Variance of normal distributions

        Returns
        ----------
        PersistenceImage
        """

        bars[:, 1] -= bars[:, 0]

        '''-----    Set image scale    -----'''
        max_x = np.max(bars[:, 0])  # birth
        min_x = 0
        max_y = np.max(bars[:, 0])  # persistence
        min_y = 0
        step_x = (max_x - min_x) / res
        step_y = (max_y - min_y) / res

        '''-----    Create Image    -----'''
        image = np.zeros(shape=(res, res, len(bars)))
        for i, [birth, persistance, dim] in enumerate(bars):  # For each feature ...
            for x in range(res):
                for y in range(res):  # For each pixel in the image ...

                    '''-----    Calculate integrated probability over pixel given 
                    by gaussian distribution centered in current feature-coordinates   -----'''
                    rest, err = mvnun(np.array([min_x + x * step_x, max_y - (y + 1) * (step_y)]),
                                      np.array([min_x + (x + 1) * step_x, max_y - y * step_y]),
                                      [birth, persistance], var * np.identity(2))
                    image[y, x, i] = abs(rest * persistance)  # Scale linearly by persistance value

        image = np.sum(image, axis=2)

        if plot:
            plt.imshow(image)
            plt.show()

        return image
