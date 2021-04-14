from math import inf

HUMAN = 1
COMP = -1
VOID = 0
LEGEND = dict(zip((VOID, HUMAN, COMP), (" ", "X", "O")))

class TicTacToe:
    def __init__(self,nb_cases):
        self.__nb_cases = nb_cases
        self.__board = self.make_board(nb_cases)

    def make_board(self,nb: int = 3):
        return [[0 for j in range(0, nb)] for i in range(0, nb)]
        # return [[0]*nb]*nb // Ne marche, chaque ligne obtient la même id()

    def evaluate(self):
        """
        Perform heuristic evaluation from board.
        Heuristic - allow the computer to discover the solution
        of some problems by itself.
        """
        if self.wins(COMP):
            return COMP
        if self.wins(HUMAN):
            return HUMAN
        return VOID


    def empty_cells(self):
        """Extract the remainder of board"""
        cells = []  # it contains all empty cells

        # Use enumerate for easy indexing
        for i, row in enumerate(self.__board):
            for j, col in enumerate(row):
                if self.__board[i][j] == VOID:
                    cells.append((i, j))

        return cells

    def wins(self,player, nb_win_case: int = 4):
        if nb_win_case > len(self.__board):
            nb_win_case = len(self.__board)

        # version splitté en plusieurs fonction mais moins optimisé
        # return win_row(board, player, nb_win_case) \
        #     or win_col(board, player, nb_win_case) \
        #     or win_diag(board, player, nb_win_case)

        isCol = []
        for x, row in enumerate(self.__board):
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
                    if x + nb_win_case <= len(self.__board):
                        isDiagL = 0
                        isDiagR = 0
                        for i in range(0, nb_win_case):
                            if y + i < len(self.__board) and self.__board[x+i][y+i] == player:
                                isDiagL += 1

                            if y >= i and self.__board[x+i][y-i] == player:
                                isDiagR += 1

                        if isDiagL == nb_win_case or isDiagR == nb_win_case:
                            return True

                else:
                    isRow = 0
                    isCol[y] = 0

        return False

    def game_over(self):
        """Check game over condition"""
        return self.wins(HUMAN) or self.wins(COMP)

    def minimax(self, depth, player):
        # inf/-inf are the initial score for the players
        best = [None, None, inf if player == COMP else -inf]

        if depth == 0 or self.game_over():
            return [None, None, self.evaluate()]
            # return [None, None, evaluate(board) * ( 1 / depth if depth else 1)]

        for cell in self.empty_cells():
            # Fill the empty cells with the player symbols
            x, y = cell[0], cell[1]
            board[x][y] = player
            if self.evaluate() == COMP:
                best = [ x, y, COMP]
                self.__board[x][y] = 0
                break
            score = self.minimax(depth - 1, -player)
            self.__board[x][y] = 0
            score[0], score[1] = x, y

            if player == COMP:
                if score[2] < best[2]:
                    best = score
            elif score[2] > best[2]:
                best = score

        return best

    def minimaxWithAB(self, depth, player, alpha = -inf, beta = inf):
        # inf/-inf are the initial score for the players
        best = [None, None, inf if player == COMP else -inf]

        if depth == 0 or self.game_over():
            return [None, None, self.evaluate()]
            # return [None, None, self.evaluate() * ( 1 / depth if depth else 1)]

        for cell in self.empty_cells():
            # Fill the empty cells with the player symbols
            x, y = cell[0], cell[1]
            self.__board[x][y] = player
            if self.evaluate() == COMP:
                best = [ x, y, COMP]
                self.__board[x][y] = 0
                break
            score = self.minimaxWithAB(depth - 1, -player, alpha, beta)
            self.__board[x][y] = 0
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

    def nb_to_coord(self,move: int):
        for i in range(0, self.__nb_cases):
            for j in range(0, self.__nb_cases):
                if move == ((i * self.__nb_cases) + j + 1):
                    return i, j
        return None


    def human_turn(self):
        remain = self.empty_cells()
        isTurn = True
        print("Your Turn")
        while isTurn:
            try:
                move = int(
                    input(f"Enter your move (1-{self.__nb_cases * self.__nb_cases}) :")
                )
                coord = self.nb_to_coord(move)
                # When the player move is valid
                # print(coord)
                # print(remain)
                if coord in remain:
                    x, y = coord
                    self.__board[x][y] = 1
                    isTurn = False
                else:
                    print("This case is full, try again.")

            # When the player mistype
            except ValueError:
                print(
                    f"Wrong input, please enter (1-{self.__nb_cases * self.__nb_cases})"
                )

        # While-else loop, this code below will run after successful loop.
        else:
            # Clean the terminal, and show the current board
            # clean()
            print(self.render())


    def ai_turn(self):
        print("AI Turn: \n")
        depth = len(self.empty_cells())  # The remaining of empty cells
        # print(self.empty_cells())
        # the optimal move for computer
        row, col, score = self.minimaxWithAB(depth, COMP)
        # print(row, col, score)
        self.__board[row][col] = COMP
        print(self.render())  # Show result board


    def render(self):
        """Render the board board to stdout"""
        pretty_board = [[LEGEND[col] for col in row] for row in self.__board]
        return ("{}\n" * len(pretty_board)).format(*pretty_board)