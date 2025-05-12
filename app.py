from flask import Flask, request, jsonify
from flask import abort
import itertools

app = Flask(__name__)

BOARD_ROWS = 6
BOARD_COLS = 7
EMPTY = 0
BLUE_PLAYER = 1
RED_PLAYER = 2

# Validate the board shape before starting
def is_valid_board_shape(board):
    # Make sure it has the number of rows and columns predefined above
    return isinstance(board, list) and len(board) == BOARD_ROWS and all(isinstance(row, list) and len(row) == BOARD_COLS for row in board)

# See how many pieces each player has
def count_pieces(board):
    flat = list(itertools.chain.from_iterable(board))

    return flat.count(BLUE_PLAYER), flat.count(RED_PLAYER)

def find_winner(board):
    # Define direction of winning pieces
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    winners = []

    for board_row in range(BOARD_ROWS):
        for board_col in range(BOARD_COLS):
            # Check which player is in the spot
            player = board[board_row][board_col]
            if player == EMPTY:
                continue
            for row, col in directions:
                coordinates = [(board_row + i*row, board_col + i*col) for i in range(4)]
                if all(0 <= x < BOARD_ROWS and 0 <= y < BOARD_COLS and board[x][y] == player for x, y in coordinates):
                    winners.append({'player': player, 'coordinates': coordinates})
    return winners

def has_floating_piece(board):
    for col in range(BOARD_COLS):
        found_empty = False
        for row in range(BOARD_ROWS-1, -1, -1):
            if board[row][col] == EMPTY:
                found_empty = True
            elif found_empty:
                return True
    return False

@app.route("/evaluate_board_state", methods=["POST"])
def evaluate_board_state():
    data = request.get_json()
    
    if not data or 'board' not in data:
        return jsonify({"error": "Missing 'board' field in request"}), 400

    board = data['board']

    if not is_valid_board_shape(board):
        return jsonify({"error": "Invalid board shape. Board has to be 6 rows of 7 columns."}), 400

    blue_count, red_count = count_pieces(board)
    if blue_count < red_count or blue_count - red_count > 1:
        return jsonify({"error": "Invalid number of pieces: Blue player must have the same or one more piece than Red player."}), 422

    if has_floating_piece(board):
        return jsonify({"error": "Invalid board state: A piece is floating above an empty space."}), 422

    winners = find_winner(board)

    if len(winners) > 1:
        return jsonify({"error": "Invalid board: Multiple winners can't happen."}), 400
    elif len(winners) == 1:
        winner = winners[0]
        return jsonify({
            "status": "win",
            "winner": "Blue!" if winner['player'] == BLUE_PLAYER else "Red!",
            "winning_coordinates": winner["coordinates"]
        })

    if all(cell != EMPTY for row in board for cell in row):
        return jsonify({"status": "stalemate"})

    player_next_turn = "Blue" if blue_count == red_count else "Red"

    return jsonify({
        "status": "in_progress",
        "player_next_turn": player_next_turn
    })

if __name__ == '__main__':
    app.run()
