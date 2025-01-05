from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

GRID_SIZE = 9


# Helper functions for solving and generating Sudoku
def is_valid(board, num, row, col):
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(GRID_SIZE)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


def find_empty(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                return i, j
    return None


def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False


def generate_puzzle(difficulty):
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

    # Fill diagonal 3x3 grids
    for i in range(0, GRID_SIZE, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for j in range(3):
            for k in range(3):
                board[i + j][i + k] = nums.pop()

    # Solve the board
    solve_sudoku(board)

    # Remove numbers based on difficulty
    cells_to_remove = {"Easy": 30, "Medium": 40, "Hard": 50}.get(difficulty, 30)
    while cells_to_remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            cells_to_remove -= 1

    return board


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    board = data.get("board", [])
    if solve_sudoku(board):
        return jsonify({"success": True, "board": board})
    return jsonify({"success": False, "message": "No solution exists"})


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    difficulty = data.get("difficulty", "Easy")
    board = generate_puzzle(difficulty)
    return jsonify({"board": board})


if __name__ == "__main__":
    app.run(debug=True)