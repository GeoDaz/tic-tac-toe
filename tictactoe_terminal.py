from math import inf
import sys
import os
import time

HUMAN = 1
COMP = -1
VOID = 0
LEGEND = dict(zip((VOID, HUMAN, COMP), (" ", "X", "O")))


def evaluate(board):
    """
    Perform heuristic evaluation from board.
    Heuristic - allow the computer to discover the solution
    of some problems by itself.
    """
    if wins(board, COMP):
        return COMP
    if wins(board, HUMAN):
        return HUMAN
    return VOID


def empty_cells(board):
    """Extract the remainder of board"""
    cells = []  # it contains all empty cells

    # Use enumerate for easy indexing
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == VOID:
                cells.append((i, j))

    return cells


# Row calc example to split wins code
def win_row(board, player, nb_win_case):
    for row in board:
        isRow = 0
        for col in row:
            if col == player:
                isRow += 1
                if isRow == nb_win_case:
                    return True
            # Reset isRow on Void cases
            elif isRow:
                isRow = 0
    return False


# Col calc example to split wins code
def win_col(board, player, nb_win_case):
    isCol = [0 for _ in range(0, len(board))]
    for row in board:
        for y, col in enumerate(row):
            if col == player:
                isCol[y] += 1
                if isCol[y] == nb_win_case:
                    return True
            # Reset isCol[col] on Void cases
            elif isCol[y]:
                isCol[y] = 0

    return False


# Diag calc example to split wins code
def win_diag(board, player, nb_win_case):
    for x, row in enumerate(board):
        if x + nb_win_case > len(board):
            break
        for y, col in enumerate(row):
            # Cherche dans y meme si y + nb_win_case > len(board) car il cherche dans diagonal gauche et droite en un seul for
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


def game_over(board):
    """Check game over condition"""
    return wins(board, HUMAN) or wins(board, COMP)


def clean():
    """Clear system terminal"""
    os_name = sys.platform.lower()
    if os_name.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')


def minimax(board, depth, player):
    # inf/-inf are the initial score for the players
    best = [None, None, inf if player == COMP else -inf]

    if depth == 0 or game_over(board):
        return [None, None, evaluate(board)]
        # return [None, None, evaluate(board) * ( 1 / depth if depth else 1)]

    for cell in empty_cells(board):
        # Fill the empty cells with the player symbols
        x, y = cell[0], cell[1]
        board[x][y] = player
        if evaluate(board) == COMP:
            best = [ x, y, COMP]
            board[x][y] = 0
            break
        score = minimax(board, depth - 1, -player)
        board[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] < best[2]:
                best = score
        elif score[2] > best[2]:
            best = score

    return best

def minimaxWithAB(board, depth, player, alpha = -inf, beta = inf):
    # inf/-inf are the initial score for the players
    best = [None, None, inf if player == COMP else -inf]

    print(player, evaluate(board))

    if depth == 0 or game_over(board):
        return [None, None, evaluate(board)]
        # return [None, None, evaluate(board) * ( 1 / depth if depth else 1)]

    for cell in empty_cells(board):
        # Fill the empty cells with the player symbols
        x, y = cell[0], cell[1]
        board[x][y] = player
        
        # Prevent from using defensive move when IA can win
        if evaluate(board) == COMP:
            best = [x, y, COMP]
            board[x][y] = 0
            break
        
        score = minimaxWithAB(board, depth - 1, -player, alpha, beta)
        board[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
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


# board : [
#     [0,0,0], 0 * 3 + 1 = 1
#     [0,0,0], 1 * 3 + 1 = 4
#     [0,0,0], 2 * 3 + 1 = 7
# ]
def nb_to_coord(move: int, board_length: int):
    for i in range(0, board_length):
        for j in range(0, board_length):
            if move == ((i * board_length) + j + 1):
                return i, j
    return None


def human_turn(board):
    nb_cases = len(board)

    remain = empty_cells(board)
    isTurn = True
    print("Your Turn")
    while isTurn:
        try:
            move = int(
                input(f"Enter your move (1-{nb_cases * nb_cases}) :")
            )
            coord = nb_to_coord(move, nb_cases)
            # When the player move is valid
            if coord in remain:
                x, y = coord
                board[x][y] = 1
                isTurn = False
            else:
                print("This case is full, try again.")

        # When the player mistype
        except ValueError:
            print(
                f"Wrong input, please enter (1-{nb_cases * nb_cases})"
            )

    # While-else loop, this code below will run after successful loop.
    else:
        # Clean the terminal, and show the current board
        # clean()
        print(render(board))


def ai_turn(board):
    print("AI Turn: \n")
    # The remaining of empty cells OR max Depth
    depth = min(len(empty_cells(board)), 7)
    # the optimal move for computer
    row, col, score = minimaxWithAB(board, depth, COMP)
    board[row][col] = COMP
    # Show result board
    print(render(board))  


def render(board):
    """Render the board board to stdout"""
    pretty_board = [[LEGEND[col] for col in row] for row in board]
    return ("{}\n" * len(pretty_board)).format(*pretty_board)


def make_board(nb: int = 3):
    return [[0 for j in range(0, nb)] for i in range(0, nb)]
    # return [[0]*nb]*nb // Ne marche, chaque ligne obtient la même id()


def main():
    print(
        "\nWelcome to Tic Tac Toe.\n"
        "Play against our IA.\n"
    )
    clean()

    nb_cases_ok = False
    while not nb_cases_ok:
        try:
            nb_cases = int(input("Choose the number of cases :"))
            nb_cases_ok = True
        except ValueError:
            print("You should write a number")

    print("Game is ready !\n")
    board = make_board(nb_cases)
    print(render(board), end="\n")

    # Dans le code précédent, on verfiait que l'humain gagnait après avoir fait joué l'IA ce qui est idiot, il faut verfier que l'humain gagne apres avoir joué.
    # Le developpeur devait pensé que son IA était imbattable et n'a pas vérifié ce qu'il se passait si l'humain gagnait.
    while not wins(board, COMP) and len(empty_cells(board)) > 0:
        human_turn(board)
        if len(empty_cells(board)) == 0 or wins(board, HUMAN):
            break
        start_time = time.time()
        ai_turn(board)
        print("--- %s seconds ---" % (time.time() - start_time))

    if wins(board, COMP):
        print("AI wins")
    elif wins(board, HUMAN):
        print("You win")
    else:
        print("It's a Draw. No one wins")


if __name__ == '__main__':
    main()
