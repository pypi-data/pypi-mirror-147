import numpy as np
import tensorflow as tf


class PersLay(tf.keras.layers.Layer):
    """
    A tf.keras.layers.Layer for computing a vectorized representation of persistence
    diagrams using deep neural networks.

    Attributes
    ---------

    w : tf.keras.Model
        - Network for mapping points to a weight

    rho : tf.keras.Model
        - Network for vectorized representation of birth, death pairs

    op : str
        - Determines which permutation invariant operation the model uses
    """

    def __init__(self, name, q, rho=None, w=None, operation='max'):
        """

        Parameters
        ----------
        name : The name of the model
        q : Size of the vector representation - Gives the size of final layer in param - rho
        rho : Network for mapping points of diagram to vector
        w : Network for mapping points to weight
        operation : Permutation Invariant operation, either; 'max', 'min', 'sum', 'mean'
        """
        super().__init__()
        self.layername = name
        self.op = operation
        if rho == None:
            self.rho = tf.keras.Sequential([tf.keras.layers.Dense(64, activation='relu'),
                                            tf.keras.layers.Dense(64, activation='relu'),
                                            tf.keras.layers.Dense(32, activation='relu'),
                                            tf.keras.layers.Dense(q)])
        else:
            self.rho = rho
        if w == None:
            self.W = tf.keras.Sequential([tf.keras.layers.Dense(64, activation='relu'),
                                          tf.keras.layers.Dense(64, activation='relu'),
                                          tf.keras.layers.Dense(32, activation='relu'),
                                          tf.keras.layers.Dense(1)])
        else:
            self.W = w

    def forward(self, data):
        """
        Performs a forward pass through the model.
        Parameters
        ----------
        data : NumpyArray - Batch Size x Num Points x Num Features
        training : Boolean -

        Returns
        -------

        Vector representation given by model of the input diagrams

        """
        # Get weight vector
        x = self.W(data)

        # Get net output
        y = self.rho(data)

        # Multiply
        x = tf.math.multiply(x, y)

        # Operation
        if self.op == 'sum':
            vector = tf.math.reduce_sum(x, axis=1)
        elif self.op == 'max':
            vector = tf.math.reduce_max(x, axis=1)
        elif self.op == 'min':
            vector = tf.math.reduce_min(x, axis=1)
        elif self.op == 'mean':
            vector = tf.math.reduce_mean(x, axis=1)

        return vector

    def call(self, inputs, training=False):
        return self.forward(inputs)
