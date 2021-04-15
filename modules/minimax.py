from math import inf
import numpy as np
from functools import reduce

COMP = "o"
HUMAN = "x"
VOID = ""
SCORE = 50


def evaluate(board, player):
    if len(board) == 3:
        if wins(board, COMP):
            return 250
        if wins(board, HUMAN):
            return -250
        return 0
    else:
        return boardScore(board, player)


def get_empty_cells(board):
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
    diags.append(np.diagonal(newArr))
    newArr = np.delete(newArr, 0, 0)
    diags.append(np.diagonal(newArr))
    flipped = np.transpose(arr)
    newArr = np.delete(flipped, 0, 0)
    diags.append(np.diagonal(newArr))

    return diags


def checkTripleAndTwoVoid(row, i, player):
    return i < len(row) - 4 \
        and row[i] == VOID \
        and row[i+1] == player \
        and row[i+2] == player \
        and row[i+3] == player \
        and row[i+4] == VOID


def getScoreOfRow(row, player):
    score = 0
    for i in range(0, len(row)-3):
        countVoid = 0
        countPlayer = 0
        for el in row[i: i+4]:
            if el == VOID:
                countVoid += 1
            elif el == player:
                countPlayer += 1
        if countPlayer == 4:
            return 5*SCORE
        if checkTripleAndTwoVoid(row, i, player):
            score = max(score, 4*SCORE)
        if countPlayer == 3 and countVoid == 1:
            score = max(score, 3*SCORE)
        if countPlayer == 2 and countVoid == 2:
            score = max(score, 2*SCORE)
    return score


def boardScore(board, player, nb_win_case: int = 4):
    if nb_win_case > len(board):
        nb_win_case = len(board)

    multiplier = 1 if player == COMP else -1
    score = 0

    # ROWS
    for i in range(0, len(board)):
        score = max(score, getScoreOfRow(board[i], player))
        if score == 5*SCORE:
            return 5*SCORE*multiplier

    # COLUMNS
    columns = np.array(board).transpose()
    for i in range(0, len(columns)):
        score = max(score, getScoreOfRow(columns[i], player))
        if score == 5*SCORE:
            return 5*SCORE*multiplier

    # DIGONALS
    diags = getDiagonalsOfBoard(board)
    for i in range(0, len(diags)):
        score = max(score, getScoreOfRow(diags[i], player))
        if score == 5*SCORE:
            return 5*SCORE*multiplier

    return score*multiplier


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


def reduceDiagonals(board, board_len, diagonals, i, j, k):
    if i > k and j > k:
        diagonals.append(board[i - k][j - k])
    elif i + k < board_len and j + k < board_len:
        diagonals.append(board[i + k][j + k])
    elif i > k and j + k < board_len:
        diagonals.append(board[i - k][j + k])
    elif i + k < board_len and j > k:
        diagonals.append(board[i + k][j - k])
    return diagonals


def getCaseDiagonals(board, board_len, i, j):
    return reduce(
        lambda diagonals, k: reduceDiagonals(
            board, board_len, diagonals, i, j, k
        ),
        range(0, 4),
        []
    )


def predict_moves(board, nb_win_case: int = 4):
    board_length = len(board)

    if nb_win_case > board_length:
        nb_win_case = board_length

    cells = []
    columns = np.array(board).transpose()
    flat_board = np.array(board).flatten()

    for i in range(0, board_length):
        for j in range(0, board_length):
            if board[i][j] == VOID and (
                HUMAN not in flat_board or (
                    HUMAN in board[i][j - nb_win_case: j - nb_win_case]
                    or HUMAN in columns[i][j - nb_win_case: j + nb_win_case]
                    or HUMAN in getCaseDiagonals(board, board_length, i, j)
                )
            ):
                cells.append((i, j))

    return cells

# b, len(get_empty_cells(b)),


def minimaxWithAB(board, isMax, depth=0, alpha=-inf, beta=inf):
    best = [None, None, -inf if isMax else inf]
    player = COMP if isMax else HUMAN
    evaluation = evaluate(board, player)

    empty_cells = get_empty_cells(board)

    if evaluation == 5*SCORE:
        return [None, None, evaluation - depth]
    if evaluation == -5*SCORE:
        return [None, None, evaluation + depth]
    if len(empty_cells) == 0:
        return [None, None, evaluation]
    if depth == 6:
        return [None, None, evaluation]

    possible_moves = predict_moves(board)

    if depth == 0:
        print(possible_moves)
        print(empty_cells)

    for cell in (possible_moves if len(possible_moves) else empty_cells):
        x, y = cell[0], cell[1]
        board[x][y] = COMP if isMax else HUMAN
        score = minimaxWithAB(board, not isMax, depth + 1, alpha, beta)
        board[x][y] = VOID
        score[0], score[1] = x, y

        if not isMax:
            if score[2] < best[2]:
                best = score
            if best[2] <= alpha:
                return best
            if best[2] < beta:
                beta = best[2]
        else:
            if score[2] > best[2]:
                best = score
            if best[2] >= beta:
                return best
            if best[2] > alpha:
                alpha = best[2]
    return best


# specific funtion
def normalize(board):
    return [[x[2] for x in row] for row in board]
