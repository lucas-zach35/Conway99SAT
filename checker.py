# Conway 99: Does there exist a strongly regular graph with 99 vertices and parameters λ=1, μ=2?
# Equivalent: srg(99,14,1,2)   (the 14 part is proven but unclear why)



#In graph theory, a strongly regular graph (SRG) is defined as follows. 
# Let G = (V, E) be a regular graph with v vertices and degree k. 
# G is said to be strongly regular if there are also integers λ and μ such that:

#Every two adjacent vertices have λ common neighbours.
#Every two non-adjacent vertices have μ common neighbours.
#= srg(v, k, λ, μ)

# 99+98+97+..+1 variables



def is_valid_srg(adjMatrix, v, k, l, mu):
    if len(adjMatrix)!=v or len(adjMatrix[0])!=v:
        return False
    
    for row in adjMatrix:
        if sum(row)!=k:
            return False

    # no self loops
    for i in range(len(adjMatrix)):
        if adjMatrix[i][i]!=0:
            return False

    for i in range(len(adjMatrix)):
        for j in range(len(adjMatrix)):
            if i==j:
                continue
            if adjMatrix[i][j]==1:
                if common_neighbours(adjMatrix, i, j)!=l:
                    return False
            elif adjMatrix[i][j]==0:
                if common_neighbours(adjMatrix, i, j)!=mu:
                    return False
            else:
                raise Exception("Invalid adjacency matrix")
    return True
def common_neighbours(adjMatrix, i, j):
    import numpy as np
    return np.dot(adjMatrix[i], adjMatrix[j])

def conway_99_valid(adjMatrix):
    return is_valid_srg(adjMatrix, 99, 14, 1, 2)
def conway_9_valid(adjacency):
    pass


def generate_random_conways_99(numberOfIterations):
    import numpy as np
    import random
    for i in range(numberOfIterations):
        adjMatrix=[]
        for i in range(0, 99):
            indices = random.sample(range(0, 99), 14)
            row=[0 for ele in range(99)]
            for j in indices:
                row[j]=1
            adjMatrix.append(row)
        if conway_99_valid(adjMatrix):
            print(adjMatrix)
            return adjMatrix
    print('None found')



# NOTE: Simplest is the (unique) srg(9,4,1,2):

def paley_graph_order_9():
    adjMatrix=[ [ 0, 1, 1, 1, 0, 0, 1, 0, 0 ], [ 1, 0, 1, 0, 1, 0, 0, 1, 0 ], 
    [ 1, 1, 0, 0, 0, 1, 0, 0, 1 ], [ 1, 0, 0, 0, 1, 1, 1, 0, 0 ], 
    [ 0, 1, 0, 1, 0, 1, 0, 1, 0 ], [ 0, 0, 1, 1, 1, 0, 0, 0, 1 ], 
    [ 1, 0, 0, 1, 0, 0, 0, 1, 1 ], [ 0, 1, 0, 0, 1, 0, 1, 0, 1 ], 
    [ 0, 0, 1, 0, 0, 1, 1, 1, 0 ] ]
    assert is_valid_srg(adjMatrix, 9, 4, 1, 2)
    print('----Paley graph is valid----')
    return adjMatrix
def generate_random_order_9_graphs(numberOfIterations):
    import numpy as np
    for i in range(numberOfIterations):
        adjMatrix=np.random.randint(0,2, size=(9,9))
        if is_valid_srg(adjMatrix, 9, 4, 1, 2):
            assert(adjMatrix==paley_graph_order_9())
            print('Found paley graph')
    
paley_graph_order_9()
#generate_random_conways_99(10000000)
generate_random_order_9_graphs(10000000)