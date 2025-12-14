import copy
import random

class Connect4:
    def __init__(self):
        pass

    ################################################# CURRENT PLATER ##################################################
    def current_player(self, state):
        x = sum(r.count("X") for r in state)
        o = sum(r.count("O") for r in state)
        return "X" if x == o else "O"


    ################################################# available_actions ###########################################
    def available_actions(self, state):
        actions = []
        player = self.current_player(state)
        rows, cols = len(state), len(state[0])

        for c in range(cols):
            if state[0][c] == "":                          
                for r in range(rows-1, -1, -1):           
                    if state[r][c] == "":
                        actions.append((player, r, c))
                        break

        random.shuffle(actions)                               # هلغبط ترتيبهم عشوائيا 
        actions.sort(key=lambda a: abs(a[2] - 3))             # هرتب الاكشنز بناءا علي مدي قربها للعمود الاوسط  
        return actions


    ############################################################ take_action #########################################################
    def take_action(self, state, action):
        new_state = copy.deepcopy(state)   
        p, r, c = action
        new_state[r][c] = p
        return new_state


    ######################################################  check_terminal  ###########################################################
    def check_terminal(self, state):
        rows, cols = len(state), len(state[0])

        def win(p):
            for r in range(rows):                                             # الفوز الافقي 
                for c in range(cols-3):
                    if all(state[r][c+i] == p for i in range(4)): return True

            for c in range(cols):                                             # الفوز الرأسي
                for r in range(rows-3):
                    if all(state[r+i][c] == p for i in range(4)): return True

            for r in range(rows-3):                                           # الفوز القطري من فوق شمال لتحت يمين 
                for c in range(cols-3):
                    if all(state[r+i][c+i] == p for i in range(4)): return True

            for r in range(3, rows):                                          # الفوز القطري من تحت شمال لفوق يمين
                for c in range(cols-3):
                    if all(state[r-i][c+i] == p for i in range(4)): return True
            return False

        if win("X"): return 100000
        if win("O"): return -100000
        if all(cell != "" for row in state for cell in row): return 0
        return "Not terminal"
