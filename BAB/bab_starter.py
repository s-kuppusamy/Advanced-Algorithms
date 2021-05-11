import picos as pic
from picos import RealVariable
from copy import deepcopy
from heapq import *
import heapq as hq
import numpy as np
import itertools
import math
counter = itertools.count() 

class BBTreeNode():
    def __init__(self, vars = [], constraints = [], objective='', prob=None):
        self.vars = vars
        self.constraints = constraints
        self.objective = objective
        self.prob = prob

    def __deepcopy__(self, memo):
        '''
        Deepcopies the picos problem
        This overrides the system's deepcopy method bc it doesn't work on classes by itself
        '''
        newprob = pic.Problem.clone(self.prob)
        return BBTreeNode(self.vars, newprob.constraints, self.objective, newprob)
    
    def buildProblem(self):
        '''
        Bulids the initial Picos problem
        '''
        prob=pic.Problem()
   
        prob.add_list_of_constraints(self.constraints)    
        
        prob.set_objective('max', self.objective)
        self.prob = prob
        return self.prob

    def is_integral(self):
        '''
        Checks if all variables (excluding the one we're maxing) are integers
        '''
        for v in self.vars[:-1]:
            if v.value == None or abs(round(v.value) - float(v.value)) > 1e-4 :
                return False
        return True

    def branch_floor(self, branch_var):
        '''
        Makes a child where xi <= floor(xi)
        '''
        n1 = deepcopy(self)
        n1.prob.add_constraint( branch_var <= math.floor(branch_var.value) ) # add in the new binary constraint

        return n1

    def branch_ceil(self, branch_var):
        '''
        Makes a child where xi >= ceiling(xi)
        '''
        n2 = deepcopy(self)
        n2.prob.add_constraint( branch_var >= math.ceil(branch_var.value) ) # add in the new binary constraint
        return n2


    def bbsolve(self):
        '''
        Use the branch and bound method to solve an integer program
        This function should return:
            return bestres, bestnode_vars

        where bestres = value of the maximized objective function
              bestnode_vars = the list of variables that create bestres
        '''

        # these lines build up the initial problem and adds it to a heap
        root = self
        res = root.buildProblem().solve(solver='cvxopt')
        heap = [(res, next(counter), root)]
        bestres = -1e20 # a small arbitrary initial best objective value
        bestnode_vars = root.vars # initialize bestnode_vars to the root vars

        #So I wasn't really able to figure out fully how to implement This. Here is a combination of some pseudocode/thought process
       
        # Overall Algorithm Overview:
            #you see what the result of the current iteration is, LP relaxing at each stage and solving
            #if it's an integer, you like stop that iteration there
            #else you break it into ceil and floor halves & redo the whole process of solving
            #you iterate through all "done" parts to find the one with the best obj value

        #Implementation/Pseudocode:

        #WHILE LOOP: until each branch reaches an integer or is determine not feasible/not valuable, keep iterating
        
            #check whether values in res of current branch are integers or not
            if (root.is_integral()):
                if (res >= bestres):
                    bestres = res
                    bestnode_vars = root.vars

            else: #else if it is not already all integers
                if (res >= bestres): #only proceed down a path if there is a better z-value
                    #for each variable, if any one is not an integer, whichever one you run into first, branch out into the floor and ceil
                    for v in root.vars[:-1]: 
                        # can check if the variable is an int by seeing if round of the var is within tiny threshold of the float version of int)
                        if v.value == None or abs(round(v.value) - float(v.value)) > 1e-4:
                            floor = root.branch_floor(v)
                            ceil = root.branch_ceil(v)
                            # The next step is to use build problem and solve to find the res of floor and ceil
                            
                            floor_res = floor.buildProblem().solve(solver='cvxopt')
                            ceil_res = ceil.buildProblem().solve(solver='cvxopt')
                            #Unsure how to implement, but if these don't return a solution, need to have check to say it's infeasible and quit that path and move to another/the next branch 

                            # Then you repeat lines 95-here on floor and ceil
                            #Now, I didn't know how to actually "store" this for both floor and ceil to "keep them in the running"
                            #My instinct from here was to recursively call the function with floor and ceil as root
                            #but that would cause issues one 1- storage as I mentioned and 2- resetting the best_res & best_vars (not desired)
                            #So per conversation with CA, one option is to a while loop instead where you keep iterating until each
                            #branches reaches an integer or is determined infeasible (noted in line 92)
                            #yet, I still don't know how to store these multiple res/root pairs -- do you add them to the heap? How? What does the heap look like? It won't let me print in a readable format.
                            #another thought was to pick floor or ceil, go all the way down that path until you hit an integer or infeasible 
                            #and then return back up the last place you branched coming all the way back up, but again still don't know how to store
                            #and also for the while loop, didn't quite know how to set up that while loop

        return bestres, bestnode_vars


     

 


