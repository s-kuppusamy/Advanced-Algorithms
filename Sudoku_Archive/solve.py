import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
#from sudoku import create_sudoku
#from sudoku import fill_presets


def create_sudoku(a):
    #creates graph
    G = nx.Graph()

    #creates all the nodes
    for row in range(int(a*a)):
        for column in range(int(a*a)):
            G.add_node((row+1,column+1))

    # give nodes attributes.
    attribute = 0
    nx.set_node_attributes(G, attribute, "numbers")

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

def fill_presets(numbers):
#first we need to fill out pre-set colors
    d = {}
    for (x,y,n) in numbers:
       d[(x,y)] = n
    return d

def solver(G,a):
    """
    1. select colored vertex and check if an edge is uncolored
    2. color the uncolored edges of this vertex
    3. find vertex with max colored in_degree
    4. color it the lowest option possible
    5. repeat steps 1-4
    """
    ec = {}
    nc = fill_presets([(1,1,1),(1,5,4),(2,1,4),(2,5,8),(2,8,3),(2,9,6),(3,5,7),(3,7,9),(4,1,2),(4,3,7),(4,6,8),(4,8,6),(5,6,4),(5,8,8),(6,3,1),(6,6,5),(6,8,2),(6,9,4),(7,5,5),(7,7,3),(8,2,6),(8,3,3),(8,4,1),(9,1,7)])
    #chosen = set()
    for node in nc.keys():
        for edge in G.edges(node):
           ec[edge] = nc[node]
    while not_complete(nc,a):
    #step 1
    
        for n in G.nodes():
            #n not in chosen and 
            if n in nc.keys():
                #step 2
                for edge in G.edges(n):
                    #if edge not in ec.keys():
                    ec[edge] = nc[n]
            #chosen.add(n)
            continue;

    #step 3
        b, max_n = max_colored_degree(ec,nc)
        if b:
            max_color = max(nc.values())
            return nc, max_color
        else:
            color = min_color_available(ec,max_n,a)
            #step 4
            nc[max_n] = color
    max_color = max(nc.values())
    return nc, max_color

def not_complete(nc,a):
    return len(nc.keys()) != a**4

def max_colored_degree(ec,nc):

#goal: find the vertex with the most colored edges
#ec - has a list of edges, let's find the node that shows up the most in ec that isn't colored
#if there is a tie, then we just pick one
    how_many = {}
    if ec == {}:
        return False,(1,1)
    for (n1,n2) in ec.keys():
        if n1 not in nc.keys():
            if n1 not in how_many:
                how_many[n1] = 0
            how_many[n1] = how_many[n1] + 1
        if n2 not in nc.keys():
            if n2 not in how_many:
                how_many[n2] = 0
            how_many[n2] = how_many[n2] + 1
    if how_many == {}:
        return True, -1
    #find maximum value in how_many and return its key, if tie just pick one
    else:
        max_value = max(how_many.values())  # maximum value
        max_keys = [k for k, v in how_many.items() if v == max_value] # getting all keys containing the `maximum`
        return False, max_keys[0]

def min_color_available(ec,max_n,a):
    bad_color = set()
    colors = set([i+1 for i in range(int(a*a))])
    for k in ec.keys():
        if max_n in k:
            bad_color.add(ec[k])
    colors = colors - bad_color
    return min(colors)

# def check_sudoku(nc):
#     pass

if __name__ == "__main__":
    a = 3.0
    G = create_sudoku(a)
    #G = fill_presets(G, [(1,1,1)])
    nc,mc = solver(G,a)
    print(nc,mc)

    # ec = {(1,2):1,(1,3):1,(1,4):1,(3,2):2}
    # nc = {1:1,3:5}
    # print(not_complete(nc,a))
    # max_n = max_colored_degree(ec, nc)
    # print(max_n)
    # print(min_color_available(ec, max_n, a))
