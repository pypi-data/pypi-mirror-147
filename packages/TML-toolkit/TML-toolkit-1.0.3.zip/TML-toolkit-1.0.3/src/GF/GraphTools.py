import numpy as np
import matplotlib.pyplot as plt
#import sknetwork as skn
from scipy.stats import gaussian_kde

class Graph():
    """
        Graph representation class. Represents a graph as a set of nodes and adjacency matrix.
    """

    node_embedding = []
    adjacency_matrix = []

    def __init__(self, nodes = [], adjacency_matrix = [], edge_list = []):

        self.updateNodeEmbedding(list(nodes))
        if adjacency_matrix == []:
            self.adjacency_matrix = np.ones((len(nodes), len(nodes))) *(-1)
        else:
            self.adjacency_matrix = adjacency_matrix#np.array([[-1,0], [0,-1]])

        '''if len(adjacency_matrix) > 0:
            self.edge_list = getEdgeList(adjacency_matrix)
            self.adjacency_matrix = adjacency_matrix
        elif len(edge_list) > 0:
            self.edge_list = edge_list
            self.adjacency_matrix = 
            #print(self.adjacency_matrix)'''

    def addNode(self, node, neighbours = []):
        '''new_key = np.max([*self.node_embedding.keys()]) + 1
        self.node_embedding[new_key] = node'''

        neighbourhood_col = np.ones(shape=(1, len(self.node_embedding))) * (-1)
        neighbourhood_col[0, neighbours] = 0
        #print('Merge this: ', np.vstack((self.adjacency_matrix, neighbourhood_col)))
        #print('With this: ',  np.append(neighbourhood_col, -1).reshape(self.adjacency_matrix.shape[0]+1, 1))
        self.adjacency_matrix = np.hstack((np.vstack((self.adjacency_matrix, neighbourhood_col)),
                                           np.append(neighbourhood_col, -1).reshape(self.adjacency_matrix.shape[0]+1, 1)))
        self.node_embedding.append(node)

    def updateConnection(self, edge, value):
        self.adjacency_matrix[edge[0], edge[1]] = value
        self.adjacency_matrix[edge[1], edge[0]] = value

    def removeNode(self, node):
        self.adjacency_matrix = np.delete(self.adjacency_matrix, node, axis=0)
        self.adjacency_matrix = np.delete(self.adjacency_matrix, node, axis=1)
        self.node_embedding.pop(node)

    def removeEdge(self, edge):
        self.adjacency_matrix[edge[0], edge[1]] = -1
        self.adjacency_matrix[edge[1], edge[0]] = -1

    def updateNodeEmbedding(self, nodes):
        self.node_embedding = nodes

    def getNodeEmbedding(self):
        return self.node_embedding

    def getNodes(self):
        return self.node_embedding

    def getNeighbour(self, node):
        return np.where(self.adjacency_matrix[node] >= 0)[0].tolist()

    def plot(self):
        plotGraph(self.node_embedding, adjacency_matrix=self.adjacency_matrix)

def getEdgeList(adjacency_matrix):
    edgelist = []
    for row, i in enumerate(adjacency_matrix):
        for collumn, j in enumerate(i):
            if j >= 0 and row != collumn:
                if not edgelist.__contains__([row, collumn]) and not edgelist.__contains__([collumn, row]):
                    edgelist.append([row, collumn])
    return np.array(edgelist)

def plotGraph(nodes, adjacency_matrix, show = True, label = ''):
    nodes = np.array(nodes)
    edges = getEdgeList(adjacency_matrix)

    if len(edges) > 0:
        plt.plot(*nodes[edges].T, color = 'black', alpha = 0.6, linewidth = 1.5, label = label)
    plt.scatter(*nodes.T, s=50, color='white', edgecolors='black', linewidths=1, zorder = 100)
    if show:
        plt.show()

def make_2DGrid(rows, cols):
    n = rows*cols
    adjacency_matrix = np.ones((n,n), dtype='float64') * (-1)
    x = np.linspace(0, 1, rows)
    y = np.linspace(0, 1, cols)
    nodes = np.array(np.meshgrid(x, y)).transpose().reshape((n, 2))
    for r in range(rows):
        for c in range(cols):
            i = r*cols + c
            # Two inner diagonals
            if c > 0:
                adjacency_matrix[i-1,i] = adjacency_matrix[i,i-1] = 1
            # Two outer diagonals
            if r > 0:
                adjacency_matrix[i-cols,i] = adjacency_matrix[i,i-cols] = 1

    return adjacency_matrix, nodes

def make_2DCircle(num_nodes):

    x = np.linspace(0,1, num_nodes//2)
    y = np.hstack((np.zeros((num_nodes//2)), np.ones(num_nodes//2)))

    nodes = np.vstack((np.hstack((x, 1-x)), y)).T -0.5

    a = np.array(list(range(num_nodes)))
    b = list(range(1,num_nodes))
    b.append(0)
    b = np.array(b)
    edges = np.vstack((a,b))

    return edges.T, nodes




