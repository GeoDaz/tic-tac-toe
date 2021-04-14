import sys
import os
import time
from TicTacToe import TicTacToe, HUMAN, COMP, LEGEND

def clean():
    """Clear system terminal"""
    os_name = sys.platform.lower()
    if os_name.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')


# board : [
#     [0,0,0], 0 * 3 + 1 = 1
#     [0,0,0], 1 * 3 + 1 = 4
#     [0,0,0], 2 * 3 + 1 = 7
# ]

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
    tictactoe = TicTacToe(nb_cases)
    print(tictactoe.render(), end="\n")

    # Dans le code précédent, on verfiait que l'humain gagnait après avoir fait joué l'IA ce qui est idiot, il faut verfier que l'humain gagne apres avoir joué.
    # Le developpeur devait pensé que son IA était imbattable et n'a pas vérifié ce qu'il se passait si l'humain gagnait.
    while not tictactoe.wins(COMP) and len(tictactoe.empty_cells()) > 0:
        tictactoe.human_turn()
        if len(tictactoe.empty_cells()) == 0 or tictactoe.wins(HUMAN):
            break
        start_time = time.time()
        tictactoe.ai_turn()
        print("--- %s seconds ---" % (time.time() - start_time))

    if tictactoe.wins(COMP):
        print("AI wins")
    elif tictactoe.wins(HUMAN):
        print("You win")
    else:
        print("It's a Draw. No one wins")


if __name__ == '__main__':
    main()
