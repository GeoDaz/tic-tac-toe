from math import inf
COMP = -1
HUMAN = 1
VOID = ''

def evaluate(board):
    if wins(board, "o"):
        return 150
    if wins(board, "x"):
        return -150
    return 0


def empty_cells(board):
    cells = []  

    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == '':
                cells.append((i, j))

    return cells


def win_row(board, player, nb_win_case):
    for row in board:
        isRow = 0
        for col in row:
            if col == player:
                isRow += 1
                if isRow == nb_win_case:
                    return True
            elif isRow:
                isRow = 0
    return False


def win_col(board, player, nb_win_case):
    isCol = [0 for _ in range(0, len(board))]
    for row in board:
        for y, col in enumerate(row):
            if col == player:
                isCol[y] += 1
                if isCol[y] == nb_win_case:
                    return True
            elif isCol[y]:
                isCol[y] = 0

    return False


def win_diag(board, player, nb_win_case):
    for x, row in enumerate(board):
        if x + nb_win_case > len(board):
            break
        for y, col in enumerate(row):
            if col == player:
                isDiagL = 0
                isDiagR = 0
                for i in range(0, nb_win_case):
                    if y + i < len(board) and board[x+i][y+i] == player:
                        isDiagL += 1
                    if y >= i and board[x+i][y-i] == player:
                        isDiagR += 1

                if isDiagL == nb_win_case or isDiagR == nb_win_case:
                    return True


def wins(board, player, nb_win_case: int = 4):
    if nb_win_case > len(board):
        nb_win_case = len(board)

    # version splitté en plusieurs fonction mais moins optimisé
    # return win_row(board, player, nb_win_case) \
    #     or win_col(board, player, nb_win_case) \
    #     or win_diag(board, player, nb_win_case)

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


def alphaBeta(b, depth, isMax, alpha, beta):
    best = -1000 if isMax else 1000
    score = evaluate(b)

    if score == 150:
        return score - depth
    if score == -150:
        return score + depth
    if len(empty_cells(b)) == 0:
        return score
    
    for cell in empty_cells(b):
        x, y = cell
        b[x][y]="o" if isMax else "x"
        
        if isMax:
            best = max(best, alphaBeta(b, depth+1, not isMax, alpha, beta))
            alpha = max(alpha, best)
            b[x][y]=""
            if best >= beta:
                return best
        else:
            best = min(best, alphaBeta(b, depth+1, not isMax, alpha, beta))
            beta = min(best, beta)
            b[x][y]=""
            if best <= alpha:
                return best
    return best


def findBestMove(b):
    bestVal = -inf
    bestMove = (-1,-1)

    for cell in empty_cells(b):
        x, y = cell[0], cell[1]
        b[x][y] = "o"

        moveVal = alphaBeta(b, 0, False, -1000, 1000)

        b[x][y] = ""

        if moveVal > bestVal:
            bestMove = (x,y)
            bestVal = moveVal

    return bestMove


# specific funtion
def normalize(board):
    return [[x[2] for x in row] for row in board]