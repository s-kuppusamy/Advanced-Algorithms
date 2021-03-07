import numpy as np


def pureLit(cnf,i):
    pureLit = []
    clause = cnf[i]
    if clause != []:
        for variable in clause:
            isPL = True
            for clause1 in cnf:
                for variable1 in clause1:
                    if variable1 == (-1*variable):
                        isPL = False   
            if isPL: 
                pureLit.append(variable)
                cnf[i] = []
    return pureLit,cnf

def unitClause(cnf):
    variable = None
    for i in range(len(cnf)):
        clause = cnf[i]
        if len(clause)==1:
            variable = clause[0]
            cnf[i] = []
            for j in range(len(cnf)):
                clause1 = cnf[j]
                for var in clause1:
                    if variable == var:
                        cnf[j] = []
            for k in range(len(cnf)):
                clause2 = cnf[k]
                for var1 in clause2:
                    if (-1*variable)==var1:
                        if len(clause2)==1:
                            cnf[k]=()
                        else:
                            cnf[k].remove(var1)
    return cnf

                
def solveSAT(cnf):
    #checks True condition
    if all(arr == [] for arr in cnf):
        return True 
    #checks False condition
    if any(arr == () for arr in cnf):
        return False
    #checks for pure literals
    for i in range(len(cnf)):
        clause = cnf[i]
        pL,cnf = pureLit(cnf,i)
        if bool(set(pL) & set(clause)):
            cnf[i] = []             
    #checks for unit clauses
    cnf = unitClause(cnf)
    #continues backtracking process
    for clause in cnf:
        if clause != [] and clause != ():
            literal = clause[0]
            break;
    newcnf = cnf
    for i in range(len(newcnf)):
        clause = newcnf[i]
        if any(variable == literal for variable in clause):
            newcnf[i] = []
        for j in range(len(newcnf)):
            clause1 = newcnf[j]
            for variable1 in clause1:
                if variable1 == (-1*literal):
                    if len(clause1)==1:
                        newcnf[j]=()
                    else:
                        newcnf[j].remove(variable1)
    if solveSAT(newcnf) == True:
        return True
    else:
        newcnf = cnf
        for i in range(len(newcnf)):
            clause = newcnf[i]
            if any(variable == (-1*literal) for variable in clause):
                newcnf[i] = []
            for j in range(len(newcnf)):
                clause1 = newcnf[j]
                for variable1 in clause1:
                    if variable1 == (literal):
                        if len(clause1)==1:
                            newcnf[j]=()
                        else:
                            newcnf[j].remove(variable1)
    return solveSAT(newcnf)      
            




                

cnf1 = [[1,2,-3],[-1,-2,3],[-1,2,-3]]
cnf2 = [[1,2,-3],[-1,-2,-3],[-1,2,-3]]
cnf3 = [[1,2,-3],[-1,-2],[1,2]]
cnf4 = [[1,2,-3],[-1,-2],[1,2],[2]]
cnf5 = [[1,2,-3],[-1,-2],[1,2],[2],[-2]]
cnf6 = [[1,2],[-1,-2],[-1,2],[1,-2]]

print("test case 1:")
print(cnf1)
print(solveSAT(cnf1))
print("test case 2:")   
print(cnf2)
print(solveSAT(cnf2)) 
print("test case 3:")  
print(cnf3)
print(solveSAT(cnf3))  
print("test case 4:") 
print(cnf4)
print(solveSAT(cnf4))  
print("test case 5:") 
print(cnf5)
print(solveSAT(cnf5))  
print("test case 6:") 
print(cnf6)
print(solveSAT(cnf6))   

    