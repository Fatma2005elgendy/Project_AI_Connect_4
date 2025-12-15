import math
import random

# ==========================================
# CLASS 1: BOARD
# ==========================================
class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.grid = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append("")
            self.grid.append(row)

# ==========================================
# CLASS 2: CONNECT4 LOGIC
# ==========================================
class Connect4:
    def __init__(self):
        pass

    def current_player(self, state):
        count_X = sum(row.count("X") for row in state)
        count_O = sum(row.count("O") for row in state)
        return 'X' if count_X == count_O else 'O'

    def available_actions(self, current_state):
        actions = []
        player = self.current_player(current_state)
        rows = len(current_state)
        cols = len(current_state[0])

        for col in range(cols):
            if current_state[0][col] == "":
                for row in range(rows - 1, -1, -1):
                    if current_state[row][col] == "":
                        actions.append((player, row, col))
                        break
        
        random.shuffle(actions)
        actions.sort(key=lambda x: abs(x[2] - 3))
        return actions

    def take_action(self, current_state, action):
        # List Slicing (أسرع طريقة لنسخ القائمة)
        new_state = [row[:] for row in current_state]
        player, row, col = action
        new_state[row][col] = player
        return new_state

    # === 1. دالة الذكاء الاصطناعي (أرقام فقط) ===
    def check_terminal(self, current_state):
        rows = len(current_state)
        cols = len(current_state[0])

        # فحص الفوز الأفقي
        for r in range(rows):
            for c in range(cols - 3):
                p = current_state[r][c]
                if p != "" and p == current_state[r][c+1] == current_state[r][c+2] == current_state[r][c+3]:
                    return 100000000 if p == "X" else -100000000
        
        # فحص الفوز العمودي
        for r in range(rows - 3):
            for c in range(cols):
                p = current_state[r][c]
                if p != "" and p == current_state[r+1][c] == current_state[r+2][c] == current_state[r+3][c]:
                    return 100000000 if p == "X" else -100000000

        # فحص الفوز القطري (موجب)
        for r in range(rows - 3):
            for c in range(cols - 3):
                p = current_state[r][c]
                if p != "" and p == current_state[r+1][c+1] == current_state[r+2][c+2] == current_state[r+3][c+3]:
                    return 100000000 if p == "X" else -100000000

        # فحص الفوز القطري (سالب)
        for r in range(3, rows):
            for c in range(cols - 3):
                p = current_state[r][c]
                if p != "" and p == current_state[r-1][c+1] == current_state[r-2][c+2] == current_state[r-3][c+3]:
                    return 100000000 if p == "X" else -100000000
        
        # فحص التعادل
        if all(cell != "" for row in current_state for cell in row):
            return 0
            
        return "Not terminal"

    # === 2. دالة الواجهة (إحداثيات فقط) ===
    def get_winning_coords(self, current_state):
        rows = len(current_state)
        cols = len(current_state[0])
        
        for r in range(rows):
            for c in range(cols):
                if current_state[r][c] == "": continue
                p = current_state[r][c]
                # Horizontal
                if c+3 < cols and p == current_state[r][c+1] == current_state[r][c+2] == current_state[r][c+3]:
                    return [[r,c], [r,c+1], [r,c+2], [r,c+3]]
                # Vertical
                if r+3 < rows and p == current_state[r+1][c] == current_state[r+2][c] == current_state[r+3][c]:
                    return [[r,c], [r+1,c], [r+2,c], [r+3,c]]
                # Diagonal Pos
                if r+3 < rows and c+3 < cols and p == current_state[r+1][c+1] == current_state[r+2][c+2] == current_state[r+3][c+3]:
                    return [[r,c], [r+1,c+1], [r+2,c+2], [r+3,c+3]]
                # Diagonal Neg
                if r-3 >= 0 and c+3 < cols and p == current_state[r-1][c+1] == current_state[r-2][c+2] == current_state[r-3][c+3]:
                    return [[r,c], [r-1,c+1], [r-2,c+2], [r-3,c+3]]
        return []

# ==========================================
# CLASS 3: AI_AGENT (PYTHONIC & OPTIMIZED)
# ==========================================
class AIAgent:
    def __init__(self, game_logic):
        self.game = game_logic

    def evaluate_window(self, window, piece):
        score = 0
        opp = "O" if piece == "X" else "X"

        if window.count(piece) == 4: score += 1000000
        elif window.count(piece) == 3 and window.count("") == 1: score += 1000
        elif window.count(piece) == 2 and window.count("") == 2: score += 10
        
        if window.count(opp) == 3 and window.count("") == 1: score -= 60000
        elif window.count(opp) == 4: score -= 1000000

        return score

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

    def MinMax(self, state, depth, alpha, beta, maximizing):
        result = self.game.check_terminal(state)
        # هنا المقارنة آمنة لأن result رقم أو سترينج، مش Tuple
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

    def get_best_move(self, state, depth=4):
        player = self.game.current_player(state)
        best_val = -math.inf if player == "X" else math.inf
        best = []

        actions = self.game.available_actions(state)
        if not actions: return None

        for a in actions:
            val = self.MinMax(self.game.take_action(state, a), depth, -math.inf, math.inf, player != "X")
            if (player == "X" and val > best_val) or (player == "O" and val < best_val):
                best_val, best = val, [a]
            elif val == best_val:
                best.append(a)
        
        if not best: return random.choice(actions)
        return random.choice(best)