import copy
import random

X = "X"
O = "O"
EMPTY = None
best_maximizing_score = float("-inf")
best_minimizing_score = float("inf")
best_actions = {}

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return "game over"
    
    num_x = sum(row.count(X) for row in board)
    num_o = sum(row.count(O) for row in board)

    if num_x == num_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                action = (i, j)  # Create a tuple representing the coordinates
                possible_actions.add(action)
    return possible_actions

    
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Create a deepcopy of the board to avoid modifying the original
    result_board = copy.deepcopy(board)
    
    # Get the next player's symbol
    next_player = player(board)

    # Check if the action is valid
    if action not in actions(board):
        return board
    
    # Make the move by placing the player's symbol at the action's position
    result_board[action[0]][action[1]] = next_player
    
    return result_board


def winner(board):
    # Check rows
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != EMPTY:
            return row[0]

    # Check columns
    for col in range(len(board[0])):
        if all(board[row][col] == board[0][col] and board[row][col] != EMPTY for row in range(len(board))):
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not winner(board):
        # Check if all cells are filled
        for row in board:
            if EMPTY in row:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        return 0
    return None

def maximizing(board):
    if terminal(board):
        return None, utility(board)

    best_move = None
    best_score = float("-inf")
    for action in actions(board):
        new_board = result(board, action)
        _, score = minimizing(new_board)
        if score > best_score:
            best_score = score
            best_move = action
    return best_move, best_score
    
def minimizing(board):
    if terminal(board):
        return None, utility(board)

    best_move = None
    best_score = float("inf")
    for action in actions(board):
        new_board = result(board, action)
        _, score = maximizing(new_board)
        if score < best_score:
            best_score = score
            best_move = action
    return best_move, best_score

def minimax(board):
    if terminal(board):
        return None
    if player(board) == X:
        best_move, _ = maximizing(board)
    else:
        best_move, _ = minimizing(board)
    return best_move

def print_board(board):
    for row in board:
        formatted_row = ["X" if cell == X else "O" if cell == O else " " for cell in row]
        print(" | ".join(formatted_row))
        print("---------")

def main():
    global best_actions
    board = initial_state()
    print("Welcome to Tic-Tac-Toe!")
    choice = input("Do you want to start as X? (y/n): ").lower()
    
    if choice == 'n':
        print("AI is thinking...")
        # If the player chooses to start as O, let AI play first
        best_actions = {}
        move = minimax(board)
        board = result(board, move)
    else:
        print("AI is thinking...")
        # If the player chooses to start as X, randomly select AI's first move
        best_actions = {}
        move = random.choice(list(actions(board)))
        board = result(board, move)

    while not terminal(board):
        print_board(board)
        while True:
            move = input("Enter your move (row,column): ")
            try:
                row, col = map(int, move.split(','))
                if board[row][col] == EMPTY:
                    board = result(board, (row, col))
                    break
                else:
                    print("That position is already taken. Try again.")
            except ValueError:
                print("Invalid input. Please enter two integers separated by a comma.")
            except IndexError:
                print("Invalid input. Please enter row and column values between 0 and 2.")
        
        print("AI is thinking...")
        best_actions = {}
        move = minimax(board)
        board = result(board, move)

    print_board(board)
    if winner(board):
        print(f"{winner(board)} wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()
