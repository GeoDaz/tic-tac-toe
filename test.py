from modules.minimax import getDiagonalsOfBoard, VOID, boardScore, COMP, HUMAN, checkTripleAndTwoVoid, getScoreOfRow, evaluate
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

print(boardScore(tab, COMP))