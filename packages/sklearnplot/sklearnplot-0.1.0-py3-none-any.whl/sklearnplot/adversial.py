import math

def is_board_full(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] is None:
                return False
            
    return True

adajacent_win_positions = [[(0,1),(0,2)],[(1,0),(2,0)],[(1,1),(2,2)]]


def check_winner(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            x = board[i][j]
            if x is None:
                continue
            for combination in adajacent_win_positions:
                i1 = i+combination[0][0]
                i2 = i+combination[1][0]
                j1 = j+combination[0][1]
                j2 = j+combination[1][1]
                if i1 >= len(board) or i2 >= len(board) or j1>=len(board[0]) or j2>=len(board[0]):
                    continue
                if board[i1][j1] == x and board[i2][j2] == x:
                    return x
                
    return None


def minimax_pruning(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == 'X':
        return 100 - depth, 0, alpha, beta
    elif winner == 'O': 
        return -100 + depth, 0, alpha, beta
    elif is_board_full(board):
        return 0, 0, alpha, beta
    
    if is_maximizing:
        best_score = -math.inf
        point = None
        for i in range(5):
            for j in range(5):
                if board[i][j] is None:
                    board[i][j] = 'X'
                    score, _, temp_alpha, temp_beta = minimax_pruning(board, depth + 1, False, alpha, beta)
                    # alpha = max(alpha, temp_alpha)
                    # beta = min(beta,temp_beta)
                    board[i][j] = None
                    if score > best_score:
                        if is_maximizing:
                            point = [i,j]
                    best_score = max(best_score, score)
                    if score >= beta:
                        if point == None:
                            point=[i,j]
                        return best_score, point, alpha, beta
                    alpha = max(alpha, best_score)
                    
        return best_score, point, alpha, beta
    else:
        best_score = math.inf
        point = None
        for i in range(5):
            for j in range(5):
                if board[i][j] is None:
                    board[i][j] = 'O'
                    score, _, temp_alpha, temp_beta = minimax_pruning(board, depth+ 1, True, alpha, beta)
                    # alpha = max(alpha, temp_alpha)
                    # beta = min(beta,temp_beta)
                    board[i][j] = None
                    best_score = (min(best_score,score))
                    if score < best_score:
                        if not is_maximizing:
                            point = [i,j]
                    # if beta <= alpha:
                    if score <= alpha:
                        if point == None:
                            point=[i,j]
                        return best_score, point, alpha, beta
                    beta = min(beta,best_score)

        return best_score, point, alpha, beta
    

def find_possible_winning_moves_X(board):
    count = {'X' : 0,
             'O' : 0
    }

    for i in range(len(board)):
        for j in range(len(board[0])):
            x = board[i][j]
            if x is None:
                continue
            for combination in adajacent_win_positions:
                i1 = i+combination[0][0]
                i2 = i+combination[1][0]
                j1 = j+combination[0][1]
                j2 = j+combination[1][1]
                if i1 >= len(board) or i2 >= len(board) or j1>=len(board[0]) or j2>=len(board[0]):
                    continue
                if board[i1][j1] == x and board[i2][j2] != x:
                    count[x] += 1
                
    return count

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    
    if winner == 'X':  # Maximizer won
        return 1
    elif winner == 'O':  # Minimizer won
        return -1
    elif is_board_full(board):  # Tie
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'X'  # Try X in this spot
                    score = minimax(board, depth + 1, False)
                    board[i][j] = None  # Undo the move
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'O'  # Try O in this spot
                    score = minimax(board, depth + 1, True)
                    board[i][j] = None  # Undo the move
                    best_score = min(best_score, score)
        return best_score

# Function to find the best move for the current player
def find_best_move(board):
    best_move = None
    best_score = -math.inf

    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = 'X'  # Maximizing player (X)
                score = minimax(board, 0, False)
                board[i][j] = None  # Undo the move
                
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    return best_move