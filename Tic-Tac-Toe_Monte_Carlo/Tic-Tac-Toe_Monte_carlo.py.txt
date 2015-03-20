# http://www.codeskulptor.org/#user39_c7SktIcIFoaIpNm.py
# http://www.codeskulptor.org/#user39_YKXKppMRiv_35.py

"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100       # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """plays a game randomly in the given board"""
    while board.check_win() == None:
        position = random.choice(board.get_empty_squares())
        board.move(position[0], position[1], player)
        player = provided.switch_player(player)
        
    
def mc_update_scores(scores, board, player): 
    "update scores "
    winner = board.check_win()
    # if player wins update score grid accordingly
    if winner == player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] += (-SCORE_OTHER)
                else:
                    scores[row][col] += 0
        return scores
               
    
    # if opponent wins update score grid accordingly
    elif winner == provided.switch_player(player):
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] += (-SCORE_CURRENT)
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] += SCORE_OTHER
                elif board.square(row, col) == provided.EMPTY:
                    scores[row][col] += 0
        return scores
    
        

def get_best_move(board, scores):
    "returns best move in (row, col) tuple"
    best_move = []
    best_move_positions = {}
    if len(board.get_empty_squares()) > 0:
        for position in board.get_empty_squares():
            best_move_positions[position] = scores[position[0]][position[1]]
        print best_move_positions
        max_value = max(best_move_positions.values())
        print "max_value: ", max_value
        best_move = [key for key,value in best_move_positions.items() if value == max_value][0]
        print best_move
        return best_move
        

def mc_move(board, player, trials): 
    "find machine move using Monte Carlo simulation"
    scores = [([0] * board.get_dim()) for dummycol in range(board.get_dim())]    
    for _ in range(trials):
        clone_board = board.clone()
        mc_trial(clone_board, player)
        mc_update_scores(scores, clone_board, player)
        print "scores: ", scores
    return get_best_move(board, scores)
    

my_board = provided.TTTBoard(3)
scores = [([0] * my_board.get_dim()) for dummycol in range(my_board.get_dim())]
clone_board = my_board.clone()
next_move = mc_move(clone_board, provided.PLAYERX, 100)
my_board.move(next_move[0], next_move[1], provided.PLAYERX )
print my_board


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

