from math import inf
import numpy as np

COMP = "o"
HUMAN = "x"
VOID = ""
SCORE = 50
TRANSPOSITION_TABLE = {}
def evaluate(board, player):
    if len(board) == 3:
        if wins(board, COMP):
            return 250
        if wins(board, HUMAN):
            return -250
        return 0
    else :
        return boardScore(board, player)


def empty_cells(board):
    cells = []  

    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == VOID:
                cells.append((i, j))
    return cells


def getDiagonalsOfBoard(b):
    diagArray = []
    npArr = np.array(b)
    diagArray += getDiagonalsRight(npArr)
    npArr = np.fliplr(npArr)
    diagArray += getDiagonalsRight(npArr)
    return diagArray
    

def getDiagonalsRight(arr):
    diags = []
    newArr = arr
    diags.append(np.diagonal(newArr).tolist())
    newArr = np.delete(newArr, 0,0)
    diags.append(np.diagonal(newArr).tolist())
    flipped = np.transpose(arr)
    newArr = np.delete(flipped, 0,0)
    diags.append(np.diagonal(newArr).tolist())

    return diags

def checkTripleAndTwoVoid(row, player):
    playerEnemy = COMP if player == HUMAN else HUMAN
    score = 0
    for i in range(len(row)-4):
        if (row[i] == VOID and row[i+1] == player and row[i+2] == player and row[i+3] == player and row[i+4] == VOID):
            score += 30
        
        if (row[i] == VOID and row[i+1] == playerEnemy and row[i+2] == playerEnemy and row[i+3] == playerEnemy and row[i+4] == VOID):
            score -= 28
    return score

def getScoreOfRow(row, player):
    playerEnemy = COMP if player == HUMAN else HUMAN
    score = 0

    countPlayer = row.count(player)
    countVoid = row.count(VOID)

    if countPlayer == 4: score += 100
    elif countPlayer == 3 and countVoid == 1: score +=10
    elif countPlayer == 2 and countVoid == 2:  score +=5

    countPlayer = row.count(playerEnemy)
    if countPlayer == 4: score -= 98
    elif countPlayer == 3 and countVoid == 1: score -=8
    elif countPlayer == 2 and countVoid == 2:  score -=4

    return score

def boardScore(board, player, nb_win_case: int = 4):
    if nb_win_case > len(board):
        nb_win_case = len(board) 

    score = 0
    # Horizontal Score
    for r in range(0, len(board)):
        row = board[r]
        score += checkTripleAndTwoVoid(row, player)
        for c in range(len(row)-3):
            window = row[c:c+4]
            score += getScoreOfRow(window, player)
    # Vertical Score
    columns = np.array(board).transpose().tolist()
    for r in range(0, len(columns)):
        col = columns[r]
        score += checkTripleAndTwoVoid(col, player)
        for c in range(len(col)-3):
            window = col[c:c+4]
            score += getScoreOfRow(window, player)
    # Diagonal Score
    diags = getDiagonalsOfBoard(board)
    for r in range(0, len(diags)):
        diag = diags[r]
        score += checkTripleAndTwoVoid(diag, player)
        for c in range(len(diag)-3):
            window = diag[c:c+4]
            score += getScoreOfRow(window, player)
    
    return score



def wins(board, player, nb_win_case: int = 4):
    if nb_win_case > len(board):
        nb_win_case = len(board)

    isCol = []
    for x, row in enumerate(board):
        isRow = 0
        for y, col in enumerate(row):
            # Init cols on first row
            if x == 0:
                isCol.append(0)

            if col == player:
                # Check row
                isRow += 1
                if isRow == nb_win_case:
                    return True

                # Check cols
                isCol[y] += 1
                if isCol[y] == nb_win_case:
                    return True

                # Check digonals
                if x + nb_win_case <= len(board):
                    isDiagL = 0
                    isDiagR = 0
                    for i in range(0, nb_win_case):
                        if y + i < len(board) and board[x+i][y+i] == player:
                            isDiagL += 1

                        if y >= i and board[x+i][y-i] == player:
                            isDiagR += 1

                    if isDiagL == nb_win_case or isDiagR == nb_win_case:
                        return True

            else:
                isRow = 0
                isCol[y] = 0

    return False

def isTerminalNode(board):
    return wins(board, COMP) or wins(board, HUMAN) or len(empty_cells(board)) == 0

# b, len(empty_cells(b)), 
def minimaxWithAB(board, isMax, depth, alpha = -inf, beta = inf):
    alpha_org = alpha
    # Transpostion tabel look up {"[[]][][][]": [[1,1,1], "TRASTS"]}
    if str(board) in TRANSPOSITION_TABLE:
        tt_entry = TRANSPOSITION_TABLE[str(board)]
        if tt_entry[1] == 'LOWERCASE':
            if tt_entry[0][2] >= beta: return tt_entry[0]
            alpha = max(alpha, tt_entry[0][2])
        if tt_entry[1] == 'UPPERCASE':
            if tt_entry[0][2] <= alpha: return tt_entry[0]
            beta = min(beta, tt_entry[0][2])
        if tt_entry[1] == 'EXACT':
            return tt_entry[0]
        
    best = [None, None, -inf if isMax else inf]
    player = COMP if isMax else HUMAN

    isTerminal = isTerminalNode(board)

    if depth == 0 or isTerminal:
        if isTerminal:
            if wins(board, COMP):
                return [None, None, 10000 - depth]
            elif wins(board, HUMAN):
                return [None, None, -10000 + depth]
            else:
                return [None, None, 0]
        else:
            return [None, None, evaluate(board, COMP)]


    for cell in empty_cells(board):
        x, y = cell[0], cell[1]
        board[x][y] = COMP if isMax else HUMAN
        score = minimaxWithAB(board, not isMax, depth - 1, alpha, beta)
        board[x][y] = VOID
        score[0], score[1] = x, y

        if not isMax:
            if score[2] < best[2]:
                best = score
            if best[2] < beta:
                beta = best[2]
            if beta <= alpha:
                break
        else:
            if score[2] > best[2]:
                best = score
            if best[2] > alpha:
                alpha = best[2]
            if alpha >= beta:
                break
  
    store(TRANSPOSITION_TABLE, board, alpha, beta, best)
    return best

def store(table, board, alpha, beta, best):
    if best[2] <= alpha:
        flag = 'UPPERCASE'
    elif best[2] >= beta:
        flag = 'LOWERCASE'
    else:
        flag = 'EXACT'

    table[str(board)] = [best, flag]


# specific funtion
def normalize(board):
    return [[x[2] for x in row] for row in board]