import numpy as np
import pygame
import math
from math import inf
import time
import threading
import pickle
# Initializing Pygame
pygame.init()

# Screen
WIDTH = 500
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("images/x.svg"), (50, 50))
O_IMAGE = pygame.transform.scale(pygame.image.load("images/o.svg"), (50, 50))

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)

###################################

COMP = "o"
HUMAN = "x"
VOID = ""
SCORE = 50


def evaluate(board, player):
    if len(board) == 3:
        if wins(board, COMP):
            return 10000
        if wins(board, HUMAN):
            return -10000
        return 0
    else:
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
    start = -(len(arr)-4)
    end = len(arr) - 3
    diags = []
    for offset in range(start, end):
        diag = [row[i+offset]
                for i, row in enumerate(arr) if 0 <= i+offset < len(row)]
        diags.append(diag)
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

    if countPlayer == 4:
        score += 100
    elif countPlayer == 3 and countVoid == 1:
        score += 10
    elif countPlayer == 2 and countVoid == 2:
        score += 5

    countPlayer = row.count(playerEnemy)
    if countPlayer == 4:
        score -= 98
    elif countPlayer == 3 and countVoid == 1:
        score -= 8
    elif countPlayer == 2 and countVoid == 2:
        score -= 4

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


def minimaxWithAB(board, isMax, depth, alpha=-inf, beta=inf):
    alpha_org = alpha
    # Transpostion tabel look up {"[[]][][][]": [[1,1,1], "TRASTS"]}
    if len(board) > 3:
        if str(board) in TRANSPOSITION_TABLE:
            tt_entry = TRANSPOSITION_TABLE[str(board)]
            if tt_entry[1] == 'LOWERCASE':
                if tt_entry[0][2] >= beta:
                    return tt_entry[0]
                alpha = max(alpha, tt_entry[0][2])
            if tt_entry[1] == 'UPPERCASE':
                if tt_entry[0][2] <= alpha:
                    return tt_entry[0]
                beta = min(beta, tt_entry[0][2])
            if tt_entry[1] == 'EXACT':
                return tt_entry[0]

    best = [None, None, -inf if isMax else inf]
    player = COMP if isMax else HUMAN

    isTerminal = isTerminalNode(board)

    if depth == 0 or isTerminal:
        if isTerminal:
            if wins(board, COMP):
                return [None, None, 10000 + (depth+1)]
            elif wins(board, HUMAN):
                return [None, None, -10000 - depth]
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

    if len(board) > 3:
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
###################################


def draw_grid():
    global ROWS
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap
        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), ROWS)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), ROWS)


def initialize_grid():
    global ROWS
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing the array
    game_array = [[VOID for j in range(0, ROWS)] for i in range(0, ROWS)]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = (x, y, VOID, True)

    return game_array


def click(game_array):
    global x_turn, o_turn, images
    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < WIDTH // ROWS // 2 and can_play:
                if x_turn:  # If it's X's turn
                    images.append((x, y, X_IMAGE))
                    game_array[i][j] = (x, y, HUMAN, False)
                    x_turn = False
                    o_turn = True
                    thread = threading.Thread(
                        target=alphaBetaThread, args=(game_array,))
                    thread.start()


def checkGameState(game_array):
    if not has_won(game_array):
        has_drawn(game_array)


def alphaBetaThread(game_array):
    global movenum
    start_time = time.time()
    normalizedGame = normalize(game_array)
    numEmptyCells = len(empty_cells(normalizedGame))
    depth = 4 if len(game_array) > 3 else numEmptyCells
    x, y, score = minimaxWithAB(
        normalizedGame, 
        True, 
        min(depth, numEmptyCells)
    )
    print(x, y, score)
    print("--- %s seconds ---" % (time.time() - start_time))
    iaPlayThis(game_array, x, y)
    movenum += 1


def iaPlayThis(game_array, row, col):
    global x_turn, o_turn
    x, y, char, can_play = game_array[row][col]
    images.append((x, y, O_IMAGE))
    game_array[row][col] = (x, y, COMP, False)
    x_turn = True
    o_turn = False
    storeTransTableInFile()


def storeTransTableInFile():
    a_file = open("transp_table.pkl", "wb")
    pickle.dump(TRANSPOSITION_TABLE, a_file)
    a_file.close()


def loadStransTableFromFile():
    try:
        a_file = open("transp_table.pkl", "rb")
        tt = pickle.load(a_file)
        a_file.close()
        return tt
    except:
        return {}

# Checking if someone has won


def has_won(game_array):
    normal = normalize(game_array)
    if(wins(normal, COMP) or wins(normal, HUMAN)):
        display_message((COMP if x_turn else HUMAN) + " has won!")
        return True
    return False


def has_drawn(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == VOID:
                return False
    display_message("It's a draw!")
    return True


def display_message(content):
    pygame.time.delay(2000)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) //
             2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render():
    global menu
    if not menu:
        win.fill(WHITE)
        draw_grid()
        # Drawing X's and O's
        for image in images:
            x, y, IMAGE = image
            win.blit(IMAGE, (x - IMAGE.get_width() //
                     2, y - IMAGE.get_height() // 2))
    else:
        win.fill(WHITE)
        draw_menu()
    pygame.display.update()


def draw_menu():
    x = 0
    y = 0
    w1, h1 = 140, 40
    x1, y1 = (WIDTH/2)-w1/2, (WIDTH/2)-h1/2
    x2, y2 = (WIDTH/2)-w1/2, (WIDTH/2 - 100)-h1/2
    x3, y3 = (WIDTH/2)-w1/2, (WIDTH/2 + 100)-h1/2
    smallfont = pygame.font.SysFont('Corbel', 35)
    text1 = smallfont.render('3x3', True, BLACK)
    text2 = smallfont.render('5x5', True, BLACK)
    text3 = smallfont.render('7x7', True, BLACK)

    pygame.draw.rect(win, (255, 0, 0), [x1, y1, 140, 40])
    pygame.draw.rect(win, (255, 0, 0), [x2, y2, 140, 40])
    pygame.draw.rect(win, (255, 0, 0), [x3, y3, 140, 40])
    win.blit(text1, ((WIDTH/2)-20, (WIDTH/2 - 100)-20))
    win.blit(text2, ((WIDTH/2)-20, (WIDTH/2)-20))
    win.blit(text3, ((WIDTH/2)-20, (WIDTH/2 + 100)-20))


def renderMenu():
    win.fill(WHITE)
    draw_menu()
    pygame.display.update()


def main():
    global x_turn, o_turn, images, draw
    global movenum, menu, ROWS
    ROWS = 3
    movenum = 0
    images = []
    draw = False
    menu = True
    run = True
    x_turn = True
    o_turn = False
    game_array = []

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                storeTransTableInFile()
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu:
                    mouse = pygame.mouse.get_pos()
                    if (WIDTH/2)-70 <= mouse[0] <= (WIDTH/2)+70 and (WIDTH/2)-20 <= mouse[1] <= (WIDTH/2)+20:
                        print("clicked 5x5")
                        ROWS = 5
                        game_array = initialize_grid()
                        menu = False
                    elif (WIDTH/2)-70 <= mouse[0] <= (WIDTH/2)+70 and (WIDTH/2 - 100)-20 <= mouse[1] <= (WIDTH/2 - 100)+20:
                        print("clicked 3x3")
                        ROWS = 3
                        game_array = initialize_grid()
                        menu = False
                    elif (WIDTH/2)-70 <= mouse[0] <= (WIDTH/2)+70 and (WIDTH/2 + 100)-20 <= mouse[1] <= (WIDTH/2 + 100)+20:
                        print("clicked 7x7")
                        ROWS = 7
                        game_array = initialize_grid()
                        menu = False
                else:
                    click(game_array)

        render()

        if len(game_array) > 0 and (has_drawn(game_array) or has_won(game_array)):
            run = False
            for col in normalize(game_array):
                print(col)


TRANSPOSITION_TABLE = loadStransTableFromFile()

while True:
    if __name__ == '__main__':
        main()
