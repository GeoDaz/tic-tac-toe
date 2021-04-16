from tkinter import * 
from TicTacToe import TicTacToe
import sys
import os
import time
from TicTacToe import TicTacToe, HUMAN, COMP, LEGEND

btn_dict = {}
label = None


def clean():
    """Clear system terminal"""
    os_name = sys.platform.lower()
    if os_name.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def end_game():
    for row in btn_dict:
        for col in btn_dict[row]:
            btn_dict[row][col]["state"] = 'disabled'

def play(case, tictactoe, string_var):
    if len(tictactoe.empty_cells()) > 0 and not tictactoe.game_over():
        tictactoe.human_turn(case)
        cord_x, cord_y = case
        btn_dict[cord_y][cord_x]['text'] = "x"
        btn_dict[cord_y][cord_x]['state'] = 'disabled'
        if tictactoe.wins(HUMAN):
            end_game()
            string_var.set("You win !")
        elif len(tictactoe.empty_cells()) > 0:
            start_time = time.time()
            cord_x, cord_y = tictactoe.ai_turn()
            duration_time = time.time() - start_time
            selected_btn = btn_dict[cord_y][cord_x]
            # if duration_time < 10:
            #     selected_btn.after(1000, selected_btn.config(text='o',state='disabled'))
            # else:
            selected_btn['state'] = 'disabled'
            selected_btn['text'] = "o"
            if tictactoe.wins(COMP):
                end_game()
                string_var.set("IA wins !")
        else:
            end_game()
            string_var.set("It's a Draw. No one wins...")

def create_board(nb_cases, window, tictactoe, string_var):
    for cord_y in range(0, nb_cases):
        btn_dict[cord_y] = {}
        for cord_x in range(nb_cases):
            idx = cord_x * nb_cases + cord_y + 1
            btn = Button(window,text=idx,width=10,height=5,command=lambda case=(cord_x, cord_y): play(case, tictactoe, string_var))
            btn.grid(row=cord_x+1,column=cord_y)
            btn_dict[cord_y][cord_x] = btn

def restart(nb_cases, window, tictactoe, string_var):
    for row in btn_dict:
        for col in btn_dict[row]:
            btn_dict[row][col].destroy()
    tictactoe = TicTacToe(nb_cases)
    create_board(nb_cases, window, tictactoe, string_var)
    string_var.set("Welcome ! Let's play !")

def main():
    # Setting game
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

    tictactoe = TicTacToe(nb_cases)
    print(tictactoe.render(), end="\n")
    print("Game is ready !\n")

    # Open window
    window = Tk()
    window.title("Tic Tac Toe")
    
    string_var=StringVar()
    string_var.set("Welcome ! Let's play !")
    create_board(nb_cases, window, tictactoe, string_var)
    Label(window,textvariable=string_var).grid(row=len(btn_dict)+1,columnspan=len(btn_dict))

    Button(window,text="Restart",width=10,command=lambda: restart(nb_cases, window, tictactoe, string_var)).grid(row=len(btn_dict)+2,column=0)
    Button(window,text="Quit",width=10,command=window.quit).grid(row=len(btn_dict)+2,column=2)

    window.mainloop()


if __name__ == '__main__':
    main()