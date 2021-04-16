from math import inf
import numpy as np
import pickle
import time

COMP = "O"
HUMAN = "X"
VOID = ""
SCORE = 50
UPPERCASE = "UPPERCASE"
LOWERCASE = "LOWERCASE"
EXACT = "EXACT"
STORAGE_FILE = "transp_table.pkl"


class TicTacToe:
    def __init__(self, nb_cases):
        self.__nb_cases = nb_cases
        self.__board = self.make_board(nb_cases)
        self.__board_length = len(self.__board)
        self.__trans_table = self.loadStransTableFromFile()
        self.turn = HUMAN

    def make_board(self, nb: int = 3):
        return [[VOID for j in range(0, nb)] for i in range(0, nb)]
        # return [[VOID]*nb]*nb // Ne marche, chaque ligne obtient la même id()

    def evaluate(self, player):
        if self.__board_length == 3:
            if self.wins(COMP):
                return 250
            if self.wins(HUMAN):
                return -250
            return 0
        else:
            return self.boardScore(player)

    def empty_cells(self):
        cells = []

        for i, row in enumerate(self.__board):
            for j, col in enumerate(row):
                if self.__board[i][j] == VOID:
                    cells.append((i, j))

        return cells

    def getDiagonalsOfBoard(self):
        diagArray = []
        npArr = np.array(self.__board)
        diagArray += self.getDiagonalsRight(npArr)
        npArr = np.fliplr(npArr)
        diagArray += self.getDiagonalsRight(npArr)
        return diagArray

    def getDiagonalsRight(self, arr):
        diags = []
        newArr = arr
        diags.append(np.diagonal(newArr).tolist())
        newArr = np.delete(newArr, 0, 0)
        diags.append(np.diagonal(newArr).tolist())
        flipped = np.transpose(arr)
        newArr = np.delete(flipped, 0, 0)
        diags.append(np.diagonal(newArr).tolist())

        return diags

    def getDiagonalsRight(self, arr):
        start = -(len(arr)-4)
        end = len(arr) - 3
        diags = []
        for offset in range(start, end):
            diags.append([
                row[i+offset] for i, row in enumerate(arr) if 0 <= i+offset < len(row)
            ])
        return diags

    def checkTripleAndTwoVoid(self, row, player):
        playerEnemy = COMP if player == HUMAN else HUMAN
        score = 0
        for i in range(len(row)-4):
            if (
                row[i] == VOID
                and row[i+1] == player
                and row[i+2] == player
                and row[i+3] == player
                and row[i+4] == VOID
            ):
                score += 30

            if (
                row[i] == VOID
                and row[i+1] == playerEnemy
                and row[i+2] == playerEnemy
                and row[i+3] == playerEnemy
                and row[i+4] == VOID
            ):
                score -= 28
        return score

    def getScoreOfRow(self, row, player):
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

    def boardScore(self, player, nb_win_case: int = 4):
        if nb_win_case > self.__board_length:
            nb_win_case = self.__board_length

        score = 0
        # Horizontal Score
        for r in range(0, self.__board_length):
            row = self.__board[r]
            score += self.checkTripleAndTwoVoid(row, player)
            for c in range(len(row)-3):
                window = row[c:c+4]
                score += self.getScoreOfRow(window, player)
        # Vertical Score
        columns = np.array(self.__board).transpose().tolist()
        for r in range(0, len(columns)):
            col = columns[r]
            score += self.checkTripleAndTwoVoid(col, player)
            for c in range(len(col)-3):
                window = col[c:c+4]
                score += self.getScoreOfRow(window, player)
        # Diagonal Score
        diags = self.getDiagonalsOfBoard()
        for r in range(0, len(diags)):
            diag = diags[r]
            score += self.checkTripleAndTwoVoid(diag, player)
            for c in range(len(diag)-3):
                window = diag[c:c+4]
                score += self.getScoreOfRow(window, player)

        return score

    def wins(self, player, nb_win_case: int = 4):
        if nb_win_case > self.__board_length:
            nb_win_case = self.__board_length

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
                    if x + nb_win_case <= self.__board_length:
                        isDiagL = 0
                        isDiagR = 0
                        for i in range(0, nb_win_case):
                            if y + i < self.__board_length and self.__board[x+i][y+i] == player:
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
        return self.wins(COMP) \
            or self.wins(HUMAN) \
            or len(self.empty_cells()) == 0

    def minimaxWithAB(self, depth, isMax, alpha=-inf, beta=inf):
        alpha_org = alpha

        if str(self.__board) in self.__trans_table:
            tt_entry = self.__trans_table[str(self.__board)]
            if tt_entry[1] == LOWERCASE:
                if tt_entry[0][2] >= beta:
                    return tt_entry[0]
                alpha = max(alpha, tt_entry[0][2])
            if tt_entry[1] == UPPERCASE:
                if tt_entry[0][2] <= alpha:
                    return tt_entry[0]
                beta = min(beta, tt_entry[0][2])
            if tt_entry[1] == EXACT:
                return tt_entry[0]

        best = [None, None, -inf if isMax else inf]
        player = COMP if isMax else HUMAN

        if self.game_over():
            if self.wins(COMP):
                return [None, None, inf - depth]
            elif self.wins(HUMAN):
                return [None, None, -inf + depth]
            else:
                return [None, None, 0]
        elif depth == 0:
            return [None, None, self.evaluate(COMP)]

        for cell in self.empty_cells():
            x, y = cell[0], cell[1]
            self.__board[x][y] = COMP if isMax else HUMAN
            score = self.minimaxWithAB(
                depth - 1,
                not isMax,
                alpha,
                beta
            )
            self.__board[x][y] = VOID
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

        self.update_trans_table(alpha, beta, best)
        return best

    def update_trans_table(self, alpha, beta, best):
        if best[2] <= alpha:
            flag = UPPERCASE
        elif best[2] >= beta:
            flag = LOWERCASE
        else:
            flag = EXACT

        self.__trans_table[str(self.__board)] = [best, flag]

    def storeTransTableInFile(self):
        a_file = open(STORAGE_FILE, "wb")
        pickle.dump(self.__trans_table, a_file)
        a_file.close()

    def loadStransTableFromFile(self):
        try:
            a_file = open(STORAGE_FILE, "rb")
            tt = pickle.load(a_file)
            a_file.close()
            print("table , ", len(tt))
            return tt
        except:
            return {}

    def human_turn(self, cord_case):
        remain = self.empty_cells()
        print("\nYour Turn")
        if cord_case in remain:
            x, y = cord_case
            self.__board[x][y] = HUMAN
            self.turn = COMP
        else:
            print("This case is full, try again.")
        print(self.render())

        # While-else loop, this code below will run after successful loop.
        # Clean the terminal, and show the current board
        # clean()

    def ai_turn(self):
        print("\nAI Turn:")
        start_time = time.time()
        numEmptyCells = len(self.empty_cells())
        depth = 6 if self.__board_length > 3 else numEmptyCells
        # the optimal move for computer
        row, col, score = self.minimaxWithAB(min(depth, numEmptyCells), True)
        # print(row, col, score)
        self.__board[row][col] = COMP
        print("--- %s seconds ---" % (time.time() - start_time))
        print(self.render())  # Show result board
        self.storeTransTableInFile()
        self.turn = HUMAN
        return (row, col)

    def render(self):
        """Render the board board to stdout"""
        return ("{}\n" * self.__board_length).format(*self.__board)
