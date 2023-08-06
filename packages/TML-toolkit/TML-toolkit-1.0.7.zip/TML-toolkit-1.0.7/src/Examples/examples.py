import time

import numpy as np
from GF import GraphTools as gt
import sklearn.datasets as skd
import tensorflow as tf
from GF.SOM import SOM
from GF.GGG import GenerativeGaussianGraph as GGG
from GF.GNG import GrowingNeuralGas as GNG
from GF.GMM import GausianMixtureModel as GMM
from GF.RGM import ReebGraphMapper as RGM
from PersistentHomology.PersistenceDiagram import PersistenceDiagram
from PersistentHomology.FilteredSimplicialComplexes import VietorisRipsComplex
from PersistentHomology.PersistenceImage import PersistenceImage
from PersistentHomology.PersistenceLandscapes import PersistanceLandscapes
from PersistentHomology.PersLay import PersLay
from PersistentHomology.TopologicalAutoencoder import TopologicalAutoencoder
import matplotlib.pyplot as plt

def testSOM():
    """
        Demonstration of the @class -> SOM, Self Organizing Map.

        Create a test dataset, construct a 6 by 6 grid as a graph.
        Then organize it to fit the dataset. Finally, map every point
        to the closest node in the graph.
    """
    a = createTestData(2, 80)
    plt.scatter(*a.T)
    adjacency_matrix, nodes = gt.make_2DGrid(6,6)
    som = SOM(adjacency_matrix, nodes = nodes)
    gt.plotGraph(som.graph.getNodeEmbedding(), som.graph.adjacency_matrix)
    som.fit(a, nodes=[])
    plt.scatter(*a.T)
    gt.plotGraph(som.graph.getNodeEmbedding(), som.graph.adjacency_matrix)
    som.transform(a)

def testGNG():
    """
        Demonstration of the @class -> GNG, Growing Neural Gas.

        Create a test dataset. Fit a graph to the dataset using the GNG.fit()
        method. Finally, map every point to the closest node in the graph.
    """
    a = createTestData(2, 150)
    plt.scatter(*a.T, s = 6)
    gng = GNG()
    gt.plotGraph(gng.graph.getNodeEmbedding(), adjacency_matrix=gng.graph.adjacency_matrix)
    gng.fit(a, nello_version=False, m=180, max_age= 15)
    plt.scatter(*a.T, s=6)
    gt.plotGraph(gng.graph.getNodeEmbedding(), adjacency_matrix=gng.graph.adjacency_matrix)

    gng.transform(a)

def testGMM():
    """
    Demonstration of GMM. Create a dataset, uses the EM algorith to fit 35
    gaussian distributions to it. Then cluster the dataset based on this and also
    generate 500 new datapoints from this GMM.

    """
    data = createTestData(2, 150)
    upper_bounds = np.amax(data, axis=0)
    lower_bounds = np.amin(data, axis=0)
    nodes = (np.random.rand(35, data.shape[1]) * (upper_bounds - lower_bounds)) + lower_bounds

    '''-----    Use the GMM EM-algorithm to do centroid based clustering and find a node embedding      -----'''
    gmm = GMM(data, len(nodes))
    gmm.EM_algorithm(data, epochs=750)
    nodes = gmm.cluster_means

    plt.scatter(*data.T)
    plt.scatter(*nodes.T, s=50)
    plt.show()

    gmm.transform(data)
    new_samples = gmm.generate(500)
    plt.scatter(*data.T)
    plt.scatter(*new_samples.T)
    plt.show()

def testGGG():
    """
    Demonstration of GGG. Create a dataset, fit a GGG to it.
    Then cluster the dataset based on its GMM with centers in its nodes. Also
    generate 500 new datapoints from this GGG.

    """
    a = createTestData(2, 80)
    ggg = GGG()
    ggg.fit(a, 20, c_epochs = 100, epochs = 50)

    new_data = ggg.GMM.generate(500)
    plt.scatter(*a.T)
    plt.scatter(*new_data.T)
    plt.show()

def testReebGraph():
    a =  skd.make_circles(n_samples=150, noise=0.1, random_state=2)[0]
    plt.scatter(*a.T)
    plt.show()

    rgm = RGM()
    rgm.fit(a, 5, 0.2, plot= True)
    rgm.transform(a)


def testMatrixReduction():
    """
        Test of the Persistence Diagram class and its boundary reduction algorithm.
        Initializes a sparse representaion of the same boundary matrix used in the
        example video "Intuition for Persistent Homology Reduction Algorithm [Teresa Heiss]", Youtube.
    """

    sparse_boundry_matrix = [[], [], [], [], [1,2], [1,3], [0,3], [0,2], [2,3], [7,8,9], [4,5,9]]

    ph = PersistenceDiagram()
    bm = ph.transform(sparse_boundry_matrix)
    print(bm)

def testRipsComplex():
    """
        Method for testing the Rips Complex class. Visualizes a small dataset
        with annotated nodes for checking correctness of simplices and their order
        in the filtered simplicial complex.
    """
    a = skd.make_blobs(n_samples=5, cluster_std=5, random_state=3)[0] / 10 # MAX 77 POINTS
    plt.scatter(*a.T)
    for idx, point in enumerate(a):
        plt.annotate(idx, point)
    plt.show()

    fc = VietorisRipsComplex()
    fc.fit(a, max_dim=2)
    print(len(fc.filtered_complex))
    print(fc.filtered_complex)

def testPD_PersIMG_PersLandscape():
    """
        Method for testing Peristence Diagrams, Persistence Images and Persistence landscapes.
        Creates a dataset, computes the PD and both vectorized representations, then plots them .
    """
    a = skd.make_circles(n_samples=25, noise=0.1, random_state=2)[0] # MAX 77 POINTS
    plt.scatter(*a.T)
    plt.show()
    print('Created data...')
    rp = VietorisRipsComplex()
    bm = rp.fit(a, max_dim=2, timer=True)
    print('Found complex..')
    pm = PersistenceDiagram()
    pm.transform(bm, timer=True)
    print('Reduced bm to persistance diagram')
    barcode = pm.getBarCodes(births=rp.birth_values)
    pm.plot()
    pi = PersistenceImage()
    pi.transform(barcode, res= 75, var=0.001)

    pl = PersistanceLandscapes()
    t = pl.transform(barcode)
    print(t)

def testPersLay():
    """
        Method for testing PersLay. Creates 5 datasets and computes their persistence images.
        Use a model consisting of a PersLay layer for training a model which learns to map from PD to PI.
        PLots PI and the prediction from the model on the corresponding PD in succession.
        In this example I pad persistence diagrams with extra points along the diagonal just so the training data
        can be fitted into a numpy tensor and to run batches of size > 1. HOWEVER, THIS IS NOT NECESSARY!
        (In fact it is stupid to do, and was done here for the sake of simplicity)
    """
    X_train = []
    y_train = []
    for i in range(5):
        a = skd.make_circles(n_samples=30, noise=0.1, random_state=i)[0]

        rp = VietorisRipsComplex()
        rp.fit(a, max_dim=2)
        sbm = rp.sbm
        pm = PersistenceDiagram()
        pm.transform(sbm)

        barcode = pm.getBarCodes(births=rp.birth_values, dims=[1])
        for i in range(6 - len(barcode)):
            barcode = np.vstack((barcode, [0, 0, 0]))
        X_train.append(barcode[:, :2])

        pi = PersistenceImage()
        img = pi.transform(barcode, var=0.01, res=10, plot=False)
        y_train.append(img.flatten())

    print('Starting training...')
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    p = tf.keras.Sequential([PersLay('perlay1', 100)])
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.1, epsilon=1e-4)
    loss = tf.keras.losses.MeanSquaredError()
    p.compile(loss=loss, optimizer=optimizer, metrics=[tf.keras.metrics.CategoricalAccuracy()])

    # print(p.predict(X_train))

    print(X_train.shape, y_train.shape)

    start = time.time()
    p.fit(X_train,
                   y=y_train, epochs=500, batch_size=5,
                   verbose=0)
    print(time.time() - start)

    preds = p.predict(X_train[:5])
    for idx, i in enumerate(preds):
        plt.imshow(np.reshape(y_train[idx], newshape=(10, 10)))
        plt.show()
        plt.imshow(np.reshape(i, newshape=(10, 10)))
        plt.show()

def testAutoEncoder():
    """
        Method for testing the TopologicalAutoencoder class. Create a dataset of points
        in the 2-D plane. Using the TA we map them to 1-D and back. PLotting both
        the PD of the original data and its latentspace representation we can evaluate
        their similarity. The 4'th plot is a plot of the decoded and encoded data
        representations.
    """

    a = skd.make_blobs(n_samples=25, n_features=2, centers=[[-1,0], [1,0],
                                                            [1,1], [0,1]],
                       cluster_std=0.05, random_state=2)[0]

    fsc = VietorisRipsComplex()
    pd = PersistenceDiagram()
    pd.transform(fsc.fit(a, max_dim=2, timer=True), timer= True)
    diagram = pd.getBarCodes(births=fsc.birth_values, dims = [0,1])
    pd.plot()

    encoder = tf.keras.Sequential([tf.keras.layers.Dense(256, activation = 'relu'), tf.keras.layers.Dense(64, activation = 'relu'),
                                   tf.keras.layers.Dense(32, activation = 'relu'), tf.keras.layers.Dense(1)])
    decoder = tf.keras.Sequential([tf.keras.layers.Dense(256, activation = 'relu'), tf.keras.layers.Dense(128, activation = 'relu'), tf.keras.layers.Dense(2)])

    model = TopologicalAutoencoder(encoder = encoder, decoder= decoder, dim = 1)
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001, epsilon=1e-4)
    loss = tf.keras.losses.MeanAbsoluteError()
    model.compile(loss = loss,optimizer=optimizer, metrics=[tf.keras.metrics.CategoricalAccuracy()], run_eagerly = True)
    print(a.shape)
    plt.scatter(*a.T, s = 20)
    plt.show()

    for i in range(1):
        model.fit(a,a, epochs = 70, batch_size = 15)
        pred = model.predict(a)
        plt.scatter(*pred.T, s = 20)
        plt.scatter(model.encode(a), np.zeros(len(a)))
        plt.show()

    fsc = VietorisRipsComplex()
    pd = PersistenceDiagram()
    pd.transform(fsc.fit(model.encode(a), max_dim=2))
    diagram = pd.getBarCodes(births=fsc.birth_values, dims = [0,1])
    pd.plot()

def createTestData(seed, num):
    a = skd.make_moons(n_samples=num, noise=0.1, random_state=seed)[0] * 1.5
    a = np.concatenate((a, skd.make_circles(n_samples=num, noise=0.1, random_state=seed)[0] + [0, 3]))
    b = (skd.make_moons(n_samples=num, noise=0.1, random_state=seed)[0] * 1.3) + [2, 3]
    a = np.concatenate((a, b))
    b = (skd.make_blobs(n_samples=num, cluster_std=1, random_state=seed)[0] * 0.6) + [-1, 1]
    a = np.concatenate((a, b))
    return a

def loss_1(input, pred):
    return tf.pow(tf.reduce_sum(input-pred), 0) *0
