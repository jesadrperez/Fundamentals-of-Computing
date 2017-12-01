"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided


# http://www.codeskulptor.org/#user43_9NyDWLU25X_29.py

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    '''
    Plays a game with next player to move and current board by making random moves,
    alternating between players. 
    '''
    while True:
        move = random.choice(board.get_empty_squares())
        board.move(move[0], move[1], player)
#        print board
    
        if board.check_win() is not None:
#            print board.check_win()
            return
    
        player = provided.switch_player(player)
        move = random.choice(board.get_empty_squares())
        board.move(move[0], move[1], player)
#        print board
    
        if board.check_win() is not None:
#            print board.check_win()
            return             

def mc_update_scores(scores, board, player):
    '''
    Takes a scores grid, with the same dim as a completed TTT board,
    and which player to be scored then scores the completed board and 
    updated the scores grid. Nothing is returned.
    '''
#    print board
#    print "board.check_win()", str(board.check_win())
    if board.check_win() == provided.DRAW:
        #print scores 
        return
    elif board.check_win() == player:
        multi = -1
    else:
        multi = 1
        
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == player:
                scores[row][col] -= SCORE_CURRENT*multi
                continue
            elif board.square(row, col) == provided.EMPTY:
                continue
            else:
                scores[row][col] += SCORE_OTHER*multi
    #print scores

def get_best_move(board, scores):
    '''
    This function takes a current board and a grid of scores. 
    The function should find all of the empty squares with 
    the maximum score and randomly return one of them as a 
    (row, column) tuple. It is an error to call this function 
    with a board that has no empty squares (there is no possible 
    next move), so your function may do whatever it wants in 
    that case. The case where the board is full will not be tested.
    '''
    
    empty_squares = board.get_empty_squares()
#    print empty_squares
    best_score = None
    if len(empty_squares) > 0:
        for square in empty_squares:
#            print scores[square[0]][square[1]]
            if scores[square[0]][square[1]] > best_score:                
                best_score = scores[square[0]][square[1]] 
#        print "best_score", str(best_score)
        best_squares = []
        for square in empty_squares:
            if scores[square[0]][square[1]] == best_score:
                best_squares.append(square)
#        print best_squares
        return random.choice(best_squares)
    

def mc_move(board, player, trails):
    '''
    Takes the current board, the machine player,
    and number of trails to run a Monte Carlo simulation on
    for the best move on the current board. Returns a tuple 
    of (row, column) with the best move.
    '''
    
    scores = make_scores(board)  
    dummy_trails = 1
    
    while dummy_trails <= trails:
        clone_board = board.clone()
        mc_trial(clone_board, player)
        mc_update_scores(scores, clone_board, provided.PLAYERX)
        dummy_trails += 1
#    print scores
    
    return get_best_move(board, scores)            
    
def make_scores(board):
    '''
    Takes a board and makes a list of lists with 
    the same dimensions as the Tic-Tac-Toe board.
    This list is returned.
    '''
    return [[0 for dummy_col in range(board.get_dim())]
        for dummy_row in range(board.get_dim())]

 
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
