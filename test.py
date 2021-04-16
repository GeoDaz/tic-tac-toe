from modules.minimax import *
import numpy as np

PYTHONHASHSEED=20

tab = [
    ['o', 'o', 'o','x','o'], 
    ['', 'x', 'x','o','x'], 
    ['', 'o', 'x','x',''], 
    ['x', 'x', 'x','o',''], 
    ['', 'o', 'o','','']
]

columns = np.array(tab).transpose()

#print(tab[0],getScoreOfRow(tab[0], COMP))

for t in getDiagonalsOfBoard(tab):
    print(type(t))