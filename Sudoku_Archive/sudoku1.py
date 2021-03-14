import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def create_sudoku(a):
    #creates graph
    G = nx.Graph()

    #creates all the nodes
    for row in range(int(a*a)):
        for column in range(int(a*a)):
            G.add_node((row+1,column+1))

    # give nodes attributes.
    #attribute = 0
    #nx.set_node_attributes(G, attribute, "numbers")

    #creates edges b/w nodes in same row and same column
    for node in G.nodes():
        for node1 in G.nodes():
            if node[0] == node1[0] and node != node1:
                G.add_edge(node,node1)
            if node[1] == node1[1] and node != node1:
                G.add_edge(node,node1)
            #creates edges b/w nodes in same box
            nodex = np.ceil(node[0]/a)
            nodey = np.ceil(node[1]/a)
            node1x = np.ceil(node1[0]/a)
            node1y = np.ceil(node1[1]/a)
            if nodex == node1x and nodey == node1y and node != node1:
                G.add_edge(node,node1)

    return G

# numbers is a list of tuples (x, y, number)
def fill_presets(numbers):
#first we need to fill out pre-set colors
    d = {}
    for (x,y,n) in numbers:
       d[(x,y)] = n
    return d

def solve_sudoku(G,a):
    nc = {}
    color = 1
    for n in G.nodes():
        if n not in nc.keys():
            b, color = check_neighbors(G,n,nc,color)
            if b: 
                nc[n] = color
                for nn in not_neighbor(G,n):
                    if nn not in nc.keys():
                        b1, color1 = check_neighbors(G,nn,nc,color)
                        if b1:
                            nc[nn] = color1
    max_color = max(nc.values())
    print(max_color)
    return nc


def not_neighbor(G, node):
    s = list(set(G.nodes()) - set(G.neighbors(node)))
    s.remove(node)
    return s

# check if any neighbors are same color
def check_neighbors(H,node,nc,color):
    for neigh in H.neighbors(node):
        if neigh in nc.keys():
            if nc[neigh] == color:
                return False, color+1
    return True,color


if __name__ == "__main__":
    a = 3.0
    G = create_sudoku(a)
    print(solve_sudoku(G,a))
