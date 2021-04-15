import pygame
import math
from math import inf
from modules.minimax import evaluate, normalize, wins, get_empty_cells, minimaxWithAB, VOID, COMP, HUMAN
import time
import threading
# Initializing Pygame
pygame.init()

# Screen
WIDTH = 500
ROWS = 5
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("Images/x.svg"), (50, 50))
O_IMAGE = pygame.transform.scale(pygame.image.load("Images/o.svg"), (50, 50))

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)


def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), ROWS)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), ROWS)


def initialize_grid():
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
    if movenum == 0:
        if game_array[2][2][3]:
            iaPlayThis(game_array, 2, 2)
        else:
            iaPlayThis(game_array, 1, 1)
    else:
        start_time = time.time()
        x, y, score = minimaxWithAB(normalize(game_array), True)
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


# Checking if someone has won
def has_won(game_array):
    normal = normalize(game_array)
    if(wins(normal, COMP) or wins(normal, HUMAN)):
        display_message('IA win' if x_turn else 'You win')
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
    win.fill(WHITE)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() //
                 2, y - IMAGE.get_height() // 2))

    pygame.display.update()


def main():
    global x_turn, o_turn, images, draw
    global movenum
    movenum = 0
    images = []
    draw = False

    run = True

    x_turn = True
    o_turn = False

    game_array = initialize_grid()
    print(normalize(game_array))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array)
        render()

        if has_drawn(game_array) or has_won(game_array):
            run = False


while True:
    if __name__ == '__main__':
        main()
