from random import choice as rand_choice
from copy import deepcopy

"""
Agent that makes random moves
"""
class Agent:
    """
    Input: None
    Description: Agent initail variables
    Output: None
    """
    def __init__(self):
        self.piece_worse = {1: 1, 2:3, 3:3, 4:5, 5:9, 6:100}
        self.pos_score = {1: [[22,22,22,22,22,22,22,22],
                              [20,20,20,20,20,20,20,20],
                              [12,12,14,16,16,14,12,12],
                              [11,11,12,15,15,12,11,11],
                              [10,10,10,14,14,10,10,10],
                              [11, 9, 8,10,10, 8, 9,11],
                              [11,12,12, 6, 6,12,12,11],
                              [10,10,10,10,10,10,10,10]],
                          2: [[ 0, 2, 4, 4, 4, 4, 2, 0],
                              [ 2, 6,10,10,10,10, 6, 2],
                              [ 4,10,12,13,13,12,10, 4],
                              [ 4,11,13,14,14,13,11, 4],
                              [ 4,10,13,14,14,13,10, 4],
                              [ 4,11,12,13,13,12,11, 4],
                              [ 2, 6,10,11,11,10, 6, 2],
                              [ 0, 2, 4, 4, 4, 4, 2, 0]],
                          3: [[ 6, 8, 8, 8, 8, 8, 8, 6],
                              [ 8,10,10,10,10,10,10, 8],
                              [ 8,10,11,12,12,11,10, 8],
                              [ 8,11,11,12,12,11,11, 8],
                              [ 8,10,12,12,12,12,10, 8],
                              [ 8,12,12,12,12,12,12, 8],
                              [ 8,11,10,10,10,10,11, 8],
                              [ 6, 8, 8, 8, 8, 8, 8, 6]],
                          4: [[10,10,10,10,10,10,10,10],
                              [11,12,12,12,12,12,12,11],
                              [ 9,10,10,10,10,10,10, 9],
                              [ 9,10,10,10,10,10,10, 9],
                              [ 9,10,10,10,10,10,10, 9],
                              [ 9,10,10,10,10,10,10, 9],
                              [ 9,10,10,10,10,10,10, 9],
                              [10,10,10,11,11,10,10,10]],
                          6: [[ 4, 2, 2, 0, 0, 2, 2, 4],
                              [ 4, 2, 2, 0, 0, 2, 2, 4],
                              [ 4, 2, 2, 0, 0, 2, 2, 4],
                              [ 4, 2, 2, 0, 0, 2, 2, 4],
                              [ 6, 4, 4, 2, 2, 4, 4, 6],
                              [ 8, 6, 6, 6, 6, 6, 6, 8],
                              [14,14,10,10,10,10,14,14],
                              [14,16,12,10,10,12,16,14]],
                          5: [[ 6, 8, 8, 9, 9, 8, 8, 6],
                              [ 8,10,10,10,10,10,10, 8],
                              [ 8,10,11,11,11,11,10, 8],
                              [ 9,10,11,11,11,11,10, 9],
                              [10,10,11,11,11,11,10, 9],
                              [ 8,11,11,11,11,11,10, 8],
                              [ 8,10,11,10,10,10,10, 8],
                              [ 6, 8, 8, 9, 9, 8, 8, 6]]
                        }
    """
    Input: game - Chess object containing the current state
    Description: Main entrance point for Agent to make moves from [This is the function called when playing games]
    Output: tuple of strings representing the curent and next moves for the Agent to make
    """
    def choose_action(self, game):
        # Find and return the best move with searching depth of 3
        return self.get_best_move(game, 3)

    """
    Input: game - Chess object containing the current state
    Description: find all possible antichess moves for current state, if no antichess moves, then return all possible moves
    Output: map of possible moves for current game state
    """
    def find_antimove(self, game):
        # All possible moves
        p_moves = {k:v for k, v in game.possible_board_moves(capture=True).items() if len(v) > 0 and ((k[0].isupper() and game.p_move == 1) or (k[0].islower() and game.p_move == -1))}
        
        # Antichess moves
        antichess_moves = {}
        for key in p_moves:
            for x in p_moves[key]:
                if game.p_move == 1:
                    if game.board[x[1]][x[0]] < 0:
                        if key in antichess_moves:
                            antichess_moves[key].append(x)
                        else:
                            antichess_moves[key] = [x]
                elif game.p_move == -1:
                    if game.board[x[1]][x[0]] > 0:
                        if key in antichess_moves:
                            antichess_moves[key].append(x)
                        else:
                            antichess_moves[key] = [x]
        if len(antichess_moves) == 0:
            return p_moves
        else:
            return antichess_moves

    """
    Input: game - Chess object containing the current state
           depth - intger value representing maximum depth of search tree
           is_maximizing_player - boolean value representing if current player needs max/min score
    Description: calculate the score for current player and game state using minmax algo
    Output: intger value representing score for current player and game state
    """
    def minimax(self, game, depth, is_maximizing_player, alpha, beta):
            # If max depth is reached, evaluate current state and return its score
            if depth == 0:
                return self.evaluate(game)
            
            # Find possible moves
            p_moves = self.find_antimove(game)

            # If it is maximizing player's turn, find the max score 
            if is_maximizing_player:
                best_score = float('-inf')
                for piece, moves in p_moves.items():
                    for move in moves:
                        game_copy = deepcopy(game)
                        game_copy.move(piece, f'{game.x[move[0]]}{game.y[move[1]]}')
                        game_copy.p_move *= -1
                        
                        score = self.minimax(game_copy, depth - 1, False, alpha, beta)
                        best_score = max(best_score, score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
                return best_score

            # Otherwise, find the min score 
            else:
                best_score = float('inf')
                for piece, moves in p_moves.items():
                    for move in moves:
                        game_copy = deepcopy(game)
                        game_copy.move(piece, f'{game.x[move[0]]}{game.y[move[1]]}')
                        game_copy.p_move *= -1
                        
                        score = self.minimax(game_copy, depth - 1, True, alpha, beta)
                        best_score = min(best_score, score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
                return best_score
    
    
    """
    Input: game - Chess object containing the current state
           depth - intger value representing maximum depth of search tree
    Description: calculate the best move for current game state using minmax searching tree
    Output: tuple of strings representing the curent and next best move
    """
    def get_best_move(self, game, depth):
        p_moves = self.find_antimove(game)

        best_moves = []
        best_score = float('-inf')
        for piece, moves in p_moves.items():
            for move in moves:
                game_copy = deepcopy(game)
                game_copy.move(piece, f'{game.x[move[0]]}{game.y[move[1]]}')
                game_copy.p_move *= -1
                    
                score = self.minimax(game_copy, depth, True, float('inf'), - float('inf'))
                if score > best_score:
                    best_score = score
                    best_moves = [[piece, f'{game.x[move[0]]}{game.y[move[1]]}']]
                elif score == best_score:
                    best_moves += [[piece, f'{game.x[move[0]]}{game.y[move[1]]}']]
        b_m = rand_choice(best_moves)
        return b_m[0],b_m[1]

    """
    Input: game - Chess object containing the current state
    Description: calculate the score for current game state using pre-defined pos_score
    Output: intger value representing score for current game state
    """
    def evaluate(self, game):
        score = 0

        for i, row in enumerate(game.board):
            for j, piece in enumerate(row):
                if piece > 0:
                    score += self.pos_score[abs(piece)][i][j]
                    score += self.piece_worse[abs(piece)]
                elif piece < 0:
                    score -= self.pos_score[abs(piece)][7-i][7-j]
                    score -= self.piece_worse[abs(piece)]

        return score * game.p_move
