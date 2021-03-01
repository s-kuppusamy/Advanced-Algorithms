import numpy as np
import pdb

def simplex(coeff,obj,val):

#STEP 1: Set Up Initial Augmented Matrix    
    numslack = len(coeff)  #slack variables
    numinvar = len(coeff[0]) #number initial variables
    #coeff is a 2D array, and len() finds the number of rows
    I = np.identity(numslack)
    augm = np.hstack((coeff,I))
    obj = np.hstack((obj,np.zeros((1,numslack))))
    zcol = np.vstack((np.zeros((numslack,1)),[-1]))
    augm = np.vstack((augm,obj))
    augm = np.hstack((augm,zcol))
    val = np.vstack((val,[0])) #add zero for the objective function final value
    augm = np.hstack((augm,val))

#STEP 2: Define initial basis set and non-basis set, where the basis set consists of the slack variables
    nb = []
    b = []
    i = 0
    while i < numinvar:
        nb.append(i)
        i += 1
    while i < numinvar+numslack:
        b.append(i)
        i += 1
    #define variables for the number of rows and number of columns in augm
    rows = len(augm)
    colns = len(augm[0])
    
    cur_var = 0
    while np.any(augm[rows-1,:colns]>0):
    #STEP 3: Arbitrarily pick an element from the non-basis set to swap with an element in the basis set. M
    # choose the value that has the lowest upper bound
        upbound = 10000000000000000000000000000000000000 #pick really big number so at least one of them is less than it 
        i = 0
        while i < len(b):
            if augm[i,cur_var]!=0 and np.abs((augm[i,colns-1]/augm[i,cur_var])) < upbound:
                upbound = np.abs((augm[i,colns-1]/augm[i,cur_var]))
                switch_index = i
            i += 1
        #update b and nb
        nb[cur_var] = b[switch_index]
        b[switch_index] = cur_var 

    #STEP 4: Convert the matrix into reduced form such that in the column associated with the cur_var, all elements are 0 
    #except for that in the row corresponding to switch_index using matrix transformations

    #first action: make the element in coln cur_var and row switch_index 1. To do this divide all elements in row switch_index 
    # by the value at that location
        if augm[i,cur_var]!=0: 
            augm[switch_index,:colns] = augm[switch_index,:colns]/augm[switch_index,cur_var]
    #next step: make all values in cur_var coln other row switch_index 0. To do this, value of each row other than 
    # row switch_index v - v*value of row switch_index 
        i = 0
        while i < rows:
            if i != switch_index:
                factor = augm[i,cur_var]
                augm[i,:colns] = augm[i,:colns] - factor*augm[switch_index,:colns]
            i += 1

    #now we have to repeat this whole process until all the elements in the bottom row are <= 0. We increment cur_val each time
    #it is not. 
        cur_var += 1
    
    #finally, we need to calculate the value of the objective function and the value of the basis set variables
    soln = []
    opt_val = 0
    i = 0
    while i < len(b):
        soln = augm[0:rows-1, colns-1] 
        i += 1
    opt_val = -1 * augm[rows-1, colns-1]
    return soln,opt_val,b

#now we call the function with whatever matrix we'd like to input

#test case
#c = [[4,6],[1,0.8]]
#o = [[5,6]]
#v = [[138],[24]]

#test case
#c = [[3,8],[2,7]]
#o = [[60,200]]
#v = [[6],[5]]


#problem 
c = [[1,1,1],[5,3,0],[0,9,2]]
o = [[8,-6,4]]
v = [[12],[20],[15]]
print(simplex(c,o,v))
