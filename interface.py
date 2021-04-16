from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Combobox
from TicTacToe import TicTacToe
import sys
import os
import time
from TicTacToe import TicTacToe, HUMAN, COMP
from threading import Thread

btn_dict = {}
others_btn = {}
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
    if len(tictactoe.empty_cells()) > 0 and not tictactoe.game_over() and tictactoe.turn == HUMAN:
        if not tictactoe.human_turn(case) :
            return None
        cord_x, cord_y = case
        btn_dict[cord_y][cord_x]['image'] = cross
        btn_dict[cord_y][cord_x]['fg'] = "black"
        btn_dict[cord_y][cord_x]['width'] = "25px"
        btn_dict[cord_y][cord_x]['height'] = "25px"
        #btn_dict[cord_y][cord_x]['font'] = 'Helvetica 20'
        if tictactoe.wins(HUMAN):
            end_game()
            string_var.set("\nYou win !")
        else:
            thread = Thread(target=ai_turn_gui, args=(tictactoe, string_var,))
            thread.start()


def ai_turn_gui(tictactoe, string_var):
    print("thread started")
    time.sleep(0.3)
    if len(tictactoe.empty_cells()) > 0:
        start_time = time.time()
        cord_x, cord_y = tictactoe.ai_turn()
        duration_time = time.time() - start_time
        selected_btn = btn_dict[cord_y][cord_x]
        # if duration_time < 10:
        #     selected_btn.after(1000, selected_btn.config(text='o',state='disabled'))
        # else:
        selected_btn['image'] = circle
        #selected_btn['font'] = 'Helvetica 20'
        btn_dict[cord_y][cord_x]['width'] = "50px"
        btn_dict[cord_y][cord_x]['height'] = "50px"
        selected_btn['fg'] = "black"
        if tictactoe.wins(COMP):
            end_game()
            string_var.set("\nIA wins !")
        else:
            string_var.set("\nIt's your turn !")
    else:
        end_game()
        string_var.set("\nIt's a Draw. No one wins...")


def create_board(nb_cases, window, tictactoe, string_var):
    for cord_y in range(0, nb_cases):
        btn_dict[cord_y] = {}
        for cord_x in range(nb_cases):
            idx = cord_x * nb_cases + cord_y + 1
            frames_list[idx] = (Frame(window, width = 100, height = 100))
            frames_list[idx].propagate(False)
            frames_list[idx].grid(row = cord_x+1, column = cord_y)
            btn = Button(frames_list[idx],text=idx,fg='dim gray',bg='white',font=('Helvetica 15'),command=lambda case=(cord_x, cord_y): play(case, tictactoe, string_var))
            btn_dict[cord_y][cord_x] = btn
            btn.pack(expand=True,fill=BOTH)


def restart(nb_cases, window, string_var):
    for index in frames_list:
        frames_list[index].destroy()
    others_btn['restart'].destroy()
    others_btn['quit'].destroy()
    
    string_var.set('')
    define_grid(window, string_var)

def create_grid(event, window, string_var, grid_msg, grid_cb):
    nb_cases = int(grid_cb.get())
    grid_msg.destroy()
    grid_cb.destroy()
    tictactoe = TicTacToe(nb_cases)

    string_var.set("Let's play !")
    create_board(nb_cases, window, tictactoe, string_var)

    others_btn['restart'] = Button(window,text="Restart",width=10,command=lambda: restart(nb_cases, window, string_var))
    others_btn['restart'].grid(row=len(btn_dict)+2,column=0)
    others_btn['quit'] = Button(window,text="Quit",width=10,command=window.quit)
    others_btn['quit'].grid(row=len(btn_dict)+2,column=nb_cases-1)


def define_grid(window, string_var):
    grid_msg = Label(text="Please, choose the number of cases :")
    grid_msg.grid(row=1,column=0)

    # define default value for combobox
    dim_select = StringVar()
    # dim_select.set(3)

    # create combobox
    grid_cb = Combobox(window, textvariable=dim_select)
    grid_cb['values'] = (3, 5, 7)
    grid_cb['state'] = 'readonly'  # normal
    grid_cb.grid(row=1,column=1)

    grid_cb.bind('<<ComboboxSelected>>', lambda e: create_grid(e, window, string_var, grid_msg, grid_cb))

def main():
    # Open window
    window = Tk()
    global circle
    global cross
    global frames_list
    frames_list = {}
    circle = PhotoImage(file = "circle.png").zoom(2).subsample(20)
    cross = PhotoImage(file = "cross.png").zoom(2).subsample(20)

    window.title("Tic Tac Toe")

    string_var = StringVar()
    string_var.set("Welcome !")
    welcome = Label(window,textvariable=string_var).grid(row=0,columnspan=2)

    define_grid(window, string_var)
    
    window.mainloop()


if __name__ == '__main__':
    main()
