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

def solve_sudoku(G,a):
    nc = {}
    H = nx.convert_node_labels_to_integers(G, first_label=1) #converts node labels 1-81
    node = 1
    total_vertices = int(a**4)
    return sud_helper(H,node,total_vertices,nc) 



def sud_helper(H,node,total_vertices,nc):
    #if all vertices have been gone through and checked to be safe, return true and print the outputs
    if node == total_vertices + 1:
        max_color = max(nc.values())
        print(max_color)
        print(nc)
        return True

    #else iterate through each color per node and see what works
    for color in range(1,10):
        if check_neighbors(H,node,nc,color): #if a safe configuration, set the color and call sud_helper on next node
            nc[node] = color
            if sud_helper(H,node+1,total_vertices,nc): #if it returns true, then return true and break the loop
                return True 
            nc[node] = 0  #otherwise reset the color of the node and try the next color
    return False #if coloring not possible return false



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
