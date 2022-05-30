"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math
# from teste import board

X = "X"
O = "O"
EMPTY = None


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
    if (sum(x.count('X') for x in board) + sum(x.count('O') for x in board)) % 2 == 0:
        return 'X'
    else:
        return 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY: 
                actions.add((i, j)) 
    
    if len(actions) > 0: 
        return actions
    else: return 'The Game Is Over'


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board without modifying the original board.
    """
    if board[action[0]][action[1]] == EMPTY: 
        new_board = deepcopy(board)
        new_board[action[0]][action[1]] = player(new_board)
        return new_board
    else: 
        raise Exception()


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontally
    
    for line in board: 
        if line.count('X') == 3: return 'X'
        if line.count('O') == 3: return 'O'

    
    # Vertically
    
    for j in range(3):
        line = []
        for i in range(3):
            line.append(board[i][j])
        if line.count('X') == 3: return 'X'
        if line.count('O') == 3: return 'O'
            
    # # Diagonally
    line = []
    for ij in range(3):
        line.append(board[ij][ij])
    if line.count('X') == 3: return 'X'
    if line.count('O') == 3: return 'O'
    
    # # Diagnolly Inverted
    diag_invert = [(0, 2), (1, 1), (2,0)]
    line = []
    for i, j in diag_invert:
        line.append(board[i][j])
    if line.count('X') == 3: return 'X'
    if line.count('O') == 3: return 'O'

    # If no one is a winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or sum(x.count(EMPTY) for x in board) == 0: 
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Considers the board is on a terminal state.
    """
    if winner(board) == 'X': return 1
    elif winner(board) == 'O': return -1
    else: return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board) == 'X':
        return max_value(board, act=True)
    else: return min_value(board, act=True)

def max_value(board, a = -math.inf, b = +math.inf, act=False):
    """
        Recursivaly return the optimal action for max player. 
    """
    v = -math.inf
    best_action = None
    if terminal(board):
        return utility(board)
    for action in actions(board):
        val_act = min_value(result(board, action), a, b)
        if val_act > v:
            v = val_act
            best_action = action
        if v >= b: 
            return v
        a = max(a, v)
    if act == True:
        return best_action
    else:
        return v

def min_value(board, a = -math.inf, b = +math.inf, act=False):
    v = +math.inf
    best_action = None
    if terminal(board):
        return utility(board)
    for action in actions(board):

        # Value of this action 
        val_act = max_value(result(board, action), a, b)
        if val_act < v:
            v = val_act
            best_action = action
        if v <= a: 
            if act: return best_action
            else: return v
        b = min(b, v)

    if act == True:
        return best_action
    else:
        return v