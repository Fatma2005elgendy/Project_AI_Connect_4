from flask import Flask, render_template, request, jsonify
from game_engine import Connect4, AIAgent

app = Flask(__name__)

game_logic = Connect4()
ai_agent = AIAgent(game_logic)
current_grid = [["" for _ in range(7)] for _ in range(6)]

# تم حذف history لأنه كان مستخدم للـ Undo فقط

def check_game_over(grid):
    result = game_logic.check_terminal(grid)
    winner = None
    coords = []
    
    if result != "Not terminal":
        if result >= 100000: winner = "X"
        elif result <= -100000: winner = "O"
        elif result == 0: winner = "Draw"
        
        if winner in ["X", "O"]:
            coords = game_logic.get_winning_coords(grid)
            
    return winner, coords

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/human_move', methods=['POST'])
def human_move():
    global current_grid
    data = request.get_json()
    col = data['col']
    
    valid_actions = game_logic.available_actions(current_grid)
    chosen_action = next((a for a in valid_actions if a[2] == col), None)
    
    if not chosen_action: return jsonify({'error': 'Invalid column'}), 400
    
    current_grid = game_logic.take_action(current_grid, chosen_action)
    winner, win_coords = check_game_over(current_grid)
    
    return jsonify({'grid': current_grid, 'winner': winner, 'win_coords': win_coords})

@app.route('/ai_auto_move', methods=['POST'])
def ai_auto_move():
    global current_grid
    
    # العمق 4 للسرعة
    best_action = ai_agent.get_best_move(current_grid, depth=4)
    player = "Unknown"
    
    if best_action:
        current_grid = game_logic.take_action(current_grid, best_action)
        player = best_action[0]

    winner, win_coords = check_game_over(current_grid)
    return jsonify({'grid': current_grid, 'winner': winner, 'player': player, 'win_coords': win_coords})

@app.route('/reset', methods=['POST'])
def reset_game():
    global current_grid
    current_grid = [["" for _ in range(7)] for _ in range(6)]
    return jsonify({'grid': current_grid})

if __name__ == "__main__":
    app.run(debug=True, port=5000)