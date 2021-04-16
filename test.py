from modules.minimax import *
import numpy as np

PYTHONHASHSEED=20

tab = [
    ['', '', '','',''], 
    ['', 'o', 'x','x',''], 
    ['', '', 'x','',''], 
    ['', 'o', 'o','x',''], 
    ['', '', '','','']
]

columns = np.array(tab).transpose()

print(minimaxWithAB(tab, True, 6))
