import math
import random

class AIAgent:
    def _init_(self, game_logic):
        self.game = game_logic
#__________________________________________


    def evaluate_window(self, window, piece):
        score = 0
        opp = "O" if piece == "X" else "X"

        if window.count(piece) == 4: score += 1000000
        elif window.count(piece) == 3 and window.count("") == 1: score += 1000
        elif window.count(piece) == 2 and window.count("") == 2: score += 10
        if window.count(opp) == 3 and window.count("") == 1: score -= 60000
        elif window.count(opp) == 4: score -= 1000000

        return score
#__________________________________________

    def evaluate_board(self, state, piece):
        score = 0
        rows, cols = len(state), len(state[0])

        score += [state[r][cols//2] for r in range(rows)].count(piece) * 100

        for r in range(rows):
            for c in range(cols-3):
                score += self.evaluate_window(state[r][c:c+4], piece)

        for c in range(cols):
            col = [state[r][c] for r in range(rows)]
            for r in range(rows-3):
                score += self.evaluate_window(col[r:r+4], piece)

        for r in range(rows-3):
            for c in range(cols-3):
                score += self.evaluate_window([state[r+i][c+i] for i in range(4)], piece)

        for r in range(3, rows):
            for c in range(cols-3):
                score += self.evaluate_window([state[r-i][c+i] for i in range(4)], piece)

        return score
#__________________________________________

    def MinMax(self, state, depth, alpha, beta, maximizing):
        result = self.game.check_terminal(state)
        if result != "Not terminal": return result
        if depth == 0: return self.evaluate_board(state, "X")

        actions = self.game.available_actions(state)

        if maximizing:
            value = -math.inf
            for a in actions:
                value = max(value, self.MinMax(self.game.take_action(state, a), depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta: break
            return value
        else:
            value = math.inf
            for a in actions:
                value = min(value, self.MinMax(self.game.take_action(state, a), depth-1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta: break
            return value
#__________________________________________

    def get_best_move(self, state, depth=5):
        player = self.game.current_player(state)
        best_val = -math.inf if player == "X" else math.inf
        best = []

        for a in self.game.available_actions(state):
            val = self.MinMax(self.game.take_action(state, a), depth, -math.inf, math.inf, player != "X")
            if (player == "X" and val > best_val) or (player == "O" and val < best_val):
                best_val, best = val, [a]
            elif val == best_val:
                best.append(a)

        return random.choice(best)
