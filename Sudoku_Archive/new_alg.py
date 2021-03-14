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
    for (x,n) in numbers:
       d[x] = n
    return d

def solve_sudoku(G,a):
    # presets = [0,0,0,4,0,0,0,0,0,
    #         4,0,9,0,0,6,8,7,0,
    #         0,0,0,9,0,0,1,0,0,
    #         5,0,4,0,2,0,0,0,9,
    #         0,7,0,8,0,4,0,6,0,
    #         6,0,0,0,3,0,5,0,2,
    #         0,0,1,0,0,7,0,0,0,
    #         0,4,3,2,0,0,6,0,5,
    #         0,0,0,0,0,5,0,0,0]
    # fills = []
    # given = []
    # for i in range (len(presets)):
    #     if presets[i] != 0:
    #         given.append(i+1)
    #         fills.append((i+1,presets[i]))
    nc = {}
    #fill_presets(fills)
    #fill_presets([(1,1,1),(1,5,4),(2,1,4),(2,5,8),(2,8,3),(2,9,6),(3,5,7),(3,7,9),(4,1,2),(4,3,7),(4,6,8),(4,8,6),(5,6,4),(5,8,8),(6,3,1),(6,6,5),(6,8,2),(6,9,4),(7,5,5),(7,7,3),(8,2,6),(8,3,3),(8,4,1),(9,1,7)])
    # mapping = {}
    # i = 0
    # for n in G.nodes():
    #     i +=1
    #     mapping[n] = i
    H = nx.convert_node_labels_to_integers(G, first_label=1)
    # print(H.nodes())
    #print(G.nodes())
    node = 1
    total_vertices = int(a**4)
    return sud_helper(H,node,total_vertices,nc)



def sud_helper(H,node,total_vertices,nc):
    if node == total_vertices + 1:
        max_color = max(nc.values())
        print(max_color)
        print(nc)
        return True
    for color in range(1,10):
        if check_neighbors(H,node,nc,color):
            nc[node] = color
            if sud_helper(H,node+1,total_vertices,nc):
                return True 
            nc[node] = 0  
    return False



# check if any neighbors are same color
def check_neighbors(H,node,nc,color):
    for neigh in H.neighbors(node):
        if neigh in nc.keys():
            if nc[neigh] == color:
                return False
    return True


if __name__ == "__main__":
    a = 3.0
    G = create_sudoku(a)
    print(solve_sudoku(G,a))
