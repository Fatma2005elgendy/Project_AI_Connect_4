import time
from board import Board
from connect4_logic import Connect4
from ai_agent import AIAgent

class GameController:
    def __init__(self):
        self.board = Board()
        self.logic = Connect4()
        self.ai = AIAgent(self.logic)
        self.state = self.board.grid
#______________________________________________________________________________________________________________________________

    def human_play(self):
        player = self.logic.current_player(self.state)
        print(f"\nYour turn ({player})")
        while True:
            try:
                col = int(input("Choose column (0-6): "))
                moves = [a for a in self.logic.available_actions(self.state) if a[2]==col]
                if moves:
                    self.state = self.logic.take_action(self.state, moves[0])
                    break
                else:
                    print("Invalid or full column")
            except ValueError:
                print("Enter a number 0-6")

        self.board.grid = self.state
        self.board.display()
#______________________________________________________________________________________________________________________________

    def computer_play(self):
        player = self.logic.current_player(self.state)
        print(f"\nComputer ({player}) is thinking...")
        time.sleep(1)
        move = self.ai.get_best_move(self.state)
        print(f"Computer plays column {move[2]}\n")
        self.state = self.logic.take_action(self.state, move)

        self.board.grid = self.state
        self.board.display()
#______________________________________________________________________________________________________________________________

    def check_winner(self):
        result = self.logic.check_terminal(self.state)
        if result != "Not terminal":
            if result == 100000: print("\n X WINS! ")
            elif result == -100000: print("\n O WINS! ")
            else: print("\n DRAW! ")
            return True
        return False
#______________________________________________________________________________________________________________________________
    def start(self):
        print("   CONNECT 4 GAME     ")
        mode = input("1. Human vs Computer\n2. Computer vs Computer\nSelect mode: ")

        if mode == "1":
            while not self.check_winner():
                self.human_play()
                if self.check_winner(): break
                self.computer_play()
        elif mode == "2":
            while not self.check_winner():
                print("\n>> Computer 1 (X)")
                self.computer_play()
                if self.check_winner(): break
                print("\n>> Computer 2 (O)")
                self.computer_play()
        else:
            print("Invalid choice")
