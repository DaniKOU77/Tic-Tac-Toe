import tkinter as tk
from tkinter import messagebox
import math
import random
import time

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe with AI")
        self.root.configure(bg="#222222") 
        self.stats = {"wins": 0, "losses": 0, "draws": 0}
        self.board = []
        self.buttons = []
        self.player_symbol = "X"
        self.computer_symbol = "O"
        self.difficulty = "Medium"  

        self.loading_screen()

    def loading_screen(self):
        self.clear_window()

        loading_label = tk.Label(self.root, text="Welcome to Tic-Tac-Toe with AI", font=("Courier New", 16), bg="#222222", fg="#00ff00")
        loading_label.pack(pady=30)

        for i in range(1, 101):
            loading_label.config(text=f"Loading... {i}%")
            self.root.update()
            time.sleep(0.05)

        loading_label.destroy()
        self.game_ui()

    def game_ui(self):
        self.clear_window()

       
        title = tk.Label(self.root, text="Tic-Tac-Toe with AI", font=("Roboto", 24), bg="#222222", fg="#eeeeee")
        title.pack(pady=10)
        stats_label = tk.Label(
            self.root,
            text=f"Wins: {self.stats['wins']} | Losses: {self.stats['losses']} | Draws: {self.stats['draws']}",
            font=("Roboto", 14),
            bg="#222222",
            fg="#cccccc",
        )
        stats_label.pack(pady=5)

        
        self.difficulty_buttons()

      
        self.board = [" " for _ in range(9)]
        self.buttons = []
        board_frame = tk.Frame(self.root, bg="#222222")
        board_frame.pack(pady=20)

        for row in range(3):
            for col in range(3):
                idx = row * 3 + col
                btn = tk.Button(
                    board_frame,
                    text=" ",
                    font=("Roboto", 20),
                    height=2,
                    width=5,
                    bg="#333333",  
                    fg="#ffffff",  
                    command=lambda idx=idx: self.player_move(idx),
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                self.buttons.append(btn)

       
        button_frame = tk.Frame(self.root, bg="#222222")
        button_frame.pack(pady=10)

        restart_btn = tk.Button(button_frame, text="Restart", font=("Roboto", 14), bg="#ff0000", fg="#ffffff", command=self.restart_game)
        restart_btn.pack(side="left", padx=5)

        quit_btn = tk.Button(button_frame, text="Quit", font=("Roboto", 14), bg="#ff0000", fg="#ffffff", command=self.root.quit)
        quit_btn.pack(side="left", padx=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def difficulty_buttons(self):
        difficulty_frame = tk.Frame(self.root, bg="#222222")
        difficulty_frame.pack()

        def set_difficulty(level):
            self.difficulty = level
            messagebox.showinfo("Difficulty Set", f"Difficulty set to {level}!")

        for level in ["Easy", "Medium", "Hard"]:
            btn = tk.Button(
                difficulty_frame,
                text=level,
                font=("Roboto", 12),
                bg="#333333",
                fg="#cccccc",
                command=lambda level=level: set_difficulty(level),
            )
            btn.pack(side="left", padx=5)

    def restart_game(self):
        self.board = [" " for _ in range(9)]
        self.create_game_ui()

    def player_move(self, index):
        if self.board[index] == " ":
            self.board[index] = self.player_symbol
            self.update_button(index, self.player_symbol)
            if self.check_winner(self.player_symbol):
                self.stats["wins"] += 1
                self.end_game("Congratulations! You win!")
                return
            if self.is_draw():
                self.stats["draws"] += 1
                self.end_game("It's a draw!")
                return
            self.computer_turn()

    def computer_turn(self):
        index = self.get_computer_move()
        self.board[index] = self.computer_symbol
        self.update_button(index, self.computer_symbol)
        if self.check_winner(self.computer_symbol):
            self.stats["losses"] += 1
            self.end_game("Oh no! The computer wins!")
        elif self.is_draw():
            self.stats["draws"] += 1
            self.end_game("It's a draw!")

    def get_computer_move(self):
        if self.difficulty == "Easy":
            return self.random_move()
        elif self.difficulty == "Medium":
            return self.random_move() if random.random() < 0.5 else self.best_move()
        else:  # Hard
            return self.best_move()

    def random_move(self):
        return random.choice([i for i, spot in enumerate(self.board) if spot == " "])

    def best_move(self):
        best_score = -math.inf
        move = None
        for i in range(len(self.board)):
            if self.board[i] == " ":
                self.board[i] = self.computer_symbol
                score = self.minimax(False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def minimax(self, is_maximizing):
        if self.check_winner(self.computer_symbol):
            return 1
        if self.check_winner(self.player_symbol):
            return -1
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(len(self.board)):
                if self.board[i] == " ":
                    self.board[i] = self.computer_symbol
                    score = self.minimax(False)
                    self.board[i] = " "
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for i in range(len(self.board)):
                if self.board[i] == " ":
                    self.board[i] = self.player_symbol
                    score = self.minimax(True)
                    self.board[i] = " "
                    best_score = min(best_score, score)
            return best_score

    def update_button(self, index, symbol):
        self.buttons[index].config(text=symbol, state=tk.DISABLED)

    def check_winner(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6],  
        ]
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False

    def is_draw(self):
        return all(space != " " for space in self.board)

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.restart_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()