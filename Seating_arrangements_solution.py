#!/usr/bin/env python
# coding: utf-8


from __future__ import print_function 
from ortools.sat.python import cp_model 


guests= ['Jaime', 'Beth', 'Jon', 'Daenerys', 'Cersei', 'Sansa', 'Tyrion'] 


Enemies = {
    'Jaime': ['Jon'], 
    'Beth':[],
    'Jon': ['Jaime','Tyrion'],
    'Daenerys': ['Cersei'],
    'Cersei': ['Daenerys','Sansa'],
    'Sansa': ['Cersei'],
    'Tyrion':['Jon']
}

Friends ={
    'Jaime': ['Cersei'],
    'Beth' : ['Tyrion'],
    'Jon': ['Daenerys'],
    'Daenerys':['Jon'],
    'Cersei': ['Jaime'],
    'Sansa':[],  
    'Tyrion': ['Beth']
}

n_table = 3      #Randomly initializing the table.. Not necessarily 3 tables are required.

#Creating the Model 
model=cp_model.CpModel() 

#Variables
table={} 
for guest in guests: 
    table[guest]= model.NewIntVar(0, n_table, guest + " Table") 
    

#Constraints
for guest in guests: 
    for enemy in Enemies[guest]:
        model.Add(table[guest] != table[enemy])   #Table number shouldn't be same for enemies
    for friend in Friends[guest]: 
        model.Add(table[guest]==table[friend])    #Table number should be same for friends
        

#Calling Solver 
solver = cp_model.CpSolver() 
status = solver.Solve(model)  


#Printing the Solution 
if status == cp_model.FEASIBLE: 
    num_table_requires= 0
    for guest in guests:
        table_num=solver.Value(table[guest])
        if (table_num + 1 > num_table_requires): 
            num_table_requires = table_num + 1
        print (guest + " sits in Table " + str(table_num))
    print ("Total number of table required is " + str(num_table_requires))          
else:
    print (f"Tables {n_table} are not enough for guests") 

