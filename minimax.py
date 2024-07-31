import tkinter as tk
from tkinter import messagebox
import math

# Initialize the board and other variables
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'

def print_board():
    for row in board:
        print(row)
    print()

def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    return [player, player, player] in win_conditions

def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 10 - depth
    if check_winner(board, 'X'):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[r][c] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[r][c] = ' '
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -math.inf
    move = (-1, -1)
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = 'O'
                score = minimax(board, 0, False)
                board[r][c] = ' '
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

def on_button_click(row, col):
    global current_player
    if board[row][col] == ' ' and current_player == 'X':
        board[row][col] = 'X'
        buttons[row][col].config(text='X')
        if check_winner(board, 'X'):
            messagebox.showinfo("Game Over", "Player X wins!")
            play_again()
        elif is_full(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            play_again()
        else:
            current_player = 'O'
            ai_move()

def ai_move():
    row, col = best_move(board)
    board[row][col] = 'O'
    buttons[row][col].config(text='O')
    if check_winner(board, 'O'):
        messagebox.showinfo("Game Over", "AI wins!")
        play_again()
    elif is_full(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        play_again()
    else:
        global current_player
        current_player = 'X'

def reset_board():
    global board, current_player
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text=' ')

def play_again():
    if messagebox.askyesno("Play Again", "Do you want to play again?"):
        reset_board()
    else:
        root.quit()

# Create the main window
root = tk.Tk()
root.title("Tic Tac Toe")

# Create buttons for the Tic Tac Toe board
buttons = [[None for _ in range(3)] for _ in range(3)]
for r in range(3):
    for c in range(3):
        button = tk.Button(root, text=' ', font=('Arial', 40), width=5, height=2,
                           command=lambda r=r, c=c: on_button_click(r, c))
        button.grid(row=r, column=c)
        buttons[r][c] = button

root.mainloop()
