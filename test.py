from modules.minimax import getDiagonalsOfBoard, VOID, boardScore, COMP, HUMAN, checkTripleAndTwoVoid, getScoreOfRow, evaluate
import numpy as np

tab = [
    ['o', 'o', '','','o'], 
    ['', '', '','',''], 
    ['', 'x', 'x','x',''], 
    ['', '', 'x','',''], 
    ['', '', '','','']
]

columns = np.array(tab).transpose()

#print(tab[0],getScoreOfRow(tab[0], COMP))

print(evaluate(tab, HUMAN))