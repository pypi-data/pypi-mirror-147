import numpy as np
import tensorflow as tf

from .FilteredSimplicialComplexes import VietorisRipsComplex
from .PersistenceDiagram import PersistenceDiagram


class TopologicalAutoencoder(tf.keras.Model):
    """
        A tf.keras.Model for Topological Autoencoders.
        Through the use of @topological_loss this autoencoder allows for
        regularization of the loss of topological features in the original datainput,
        both in the latent- and output-space of the model.

        Attributes
        ----------
        name : str
            - Name of the model
        encoder: tf.keras.Model / tf.keras.Sequential
            - Encoder network of the model
        decoder: tf.keras.Model / tf.keras.Sequential
            - Decoder network of the model
        dim: int
            - Dimention of latentspace
        output_loss: bool
            - Determines weather to include the topological loss of the output in addition to the latentspace

        Methods
        -------
        call(input):
            Makes a forward pass through the network

        encode(input):
            Returns a latentspace representation of the input

        decode(input):
            Returns a reconstruction of an input from the latentspace
        """

    def __init__(self, encoder, decoder, dim, name='TAE1', output_loss=False):
        """

        Parameters
        ----------
        encoder : tf.keras.Sequential-object
            - Defines the encoder network

        decoder : tf.keras.Sequential-object
            - Defines the decoder network

        dim : int
            - Sets the dimension of the latentspace representation of the data

        output_loss : bool
            - Decide weather to include the topological loss of the output in addition to the latentspace or not
        """

        super(TopologicalAutoencoder, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.dim = dim
        self.output_loss = output_loss

    def call(self, input):
        """
        Makes a forwardpass through the network and returns the reconstructed
        inputdata.

        Parameters
        ----------
        input : Iterable
            - Batch: An iterable object containing a number (batch_size) of: num_points x num_features - numpy.arrays()

        Returns
        -------
            numpy.array() of dimentions: batch_size x num_points x num_features.
        """
        preds = self.encoder(input)
        self.add_loss(topological_loss(input, preds))
        preds = self.decoder(preds)
        if self.output_loss:
            self.add_loss(topological_loss(input, preds))
        return preds

    def encode(self, input):
        return self.encoder(input)

    def decode(self, input):
        return self.decoder(input)


def topological_loss(X, Z):
    """
    Calculates the topological loss between two data representations as given by
    Moore,2020,'Topological Autoencoders', pp. 3-5.

    Parameters
    ----------
    X : numpy.array - Data representation in space X
    Z : numpy.array - Data representation in space Z

    Returns
    -------
        float - The topological loss
    """

    '''-----    Find relevant edges in space X  -----'''
    fsc = VietorisRipsComplex()
    pd = PersistenceDiagram()
    pd.transform(fsc.fit(X, max_dim=2))
    diagram = pd.getBarCodes(births=fsc.birth_values, dims=[0, 1])
    pi_x = []  # Relevant edges in X
    if len(diagram) > 0:
        for point in diagram[:, :2]:
            if point[0] != 0:
                pi_x.append(fsc.points_from_edge[point[0]])
            pi_x.append(fsc.points_from_edge[point[1]])
    pi_x = np.array(pi_x)

    '''-----    Find relevant edges in space Z  -----'''
    fsc = VietorisRipsComplex()
    pd = PersistenceDiagram()
    pd.transform(fsc.fit(Z, max_dim=2))
    diagram = pd.getBarCodes(births=fsc.birth_values, dims=[0, 1])
    pi_z = []  # Relevant edges in Z
    if len(diagram) > 0:
        for point in diagram[:, :2]:
            if point[0] != 0:
                pi_z.append(fsc.points_from_edge[point[0]])
            pi_z.append(fsc.points_from_edge[point[1]])
    pi_z = np.array(pi_z)

    '''-----    Compute Loss from relevant edges in X    -----'''
    L_x = 0
    for n1, n2 in pi_x:
        d_x = tf.math.sqrt(tf.math.reduce_sum(tf.math.pow(X[n1] - X[n2], 2)))
        d_z = tf.math.sqrt(tf.math.reduce_sum(tf.math.pow(Z[n1] - Z[n2], 2)))
        L_x += 0.5 * tf.math.pow(d_x - d_z, 2)

    '''-----    Compute Loss from relevant edges in Z    -----'''
    L_z = 0
    for n1, n2 in pi_z:
        d_x = tf.math.sqrt(tf.math.reduce_sum(tf.math.pow(X[n1] - X[n2], 2)))
        d_z = tf.math.sqrt(tf.math.reduce_sum(tf.math.pow(Z[n1] - Z[n2], 2)))
        L_x += 0.5 * tf.math.pow(d_z - d_x, 2)

    return L_x + L_z
