"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
import random

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """ 
    
    if board.check_win() == None:
        move_list = []
        for empty_square in board.get_empty_squares():         
            board_clone = board.clone()
            board_clone.move(empty_square[0], empty_square[1], player)        
            score, dummy_move = mm_move(board_clone, provided.switch_player(player))            
            
            if score * SCORES[player] == 1:
                return score, empty_square
            else:
                move_list.append((score*SCORES[player], empty_square))
                
        max_score = max(move_list)[0]        
        best_moves = [score for score in move_list if score[0] == max_score]
        best_move = random.choice(best_moves)
        return best_move[0]*SCORES[player], best_move[1]
    else:
        return SCORES[board.check_win()], (-1, -1)        

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#board = provided.TTTBoard(3, False,
#    [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO],
#     [provided.PLAYERO, provided.PLAYERX, provided.PLAYERX],
#     [provided.PLAYERX, provided.PLAYERO, provided.PLAYERO]])
#print 'Draw'
#print board
#print mm_move(board, provided.PLAYERX)
#print 
#
#board = provided.TTTBoard(3, False,
#    [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO],
#     [provided.EMPTY, provided.PLAYERX, provided.PLAYERX],
#     [provided.PLAYERO, provided.EMPTY, provided.PLAYERX]])
#print 'PLAYERX Wins'
#print board
#print mm_move(board, provided.PLAYERX)
#print
#
#board = provided.TTTBoard(3, False,
#    [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO],
#     [provided.EMPTY, provided.PLAYERO, provided.PLAYERX],
#     [provided.PLAYERO, provided.EMPTY, provided.PLAYERX]])
#print 'PLAYERO Wins'
#print board
#print mm_move(board, provided.PLAYERX)
#print 

#board = provided.TTTBoard(3, False,
#    [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO],
#     [provided.EMPTY, provided.PLAYERO, provided.PLAYERX],
#     [provided.EMPTY, provided.EMPTY, provided.PLAYERX]])
#print 'Game in progress'
#print board
#print mm_move(board, provided.PLAYERX)

#board = provided.TTTBoard(3, False, 
#                          [[provided.PLAYERX, provided.EMPTY, provided.EMPTY],
#                           [provided.PLAYERO, provided.PLAYERO, provided.EMPTY],
#                           [provided.EMPTY, provided.PLAYERX, provided.EMPTY]])
#print 'Game in progress'
#print board
#print mm_move(board, provided.PLAYERX)
