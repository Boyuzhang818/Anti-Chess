from chess import Chess
from agent import Agent
from copy import deepcopy
import sys

# total arguments
n = len(sys.argv)

if n != 2:
    print("Invalid command-line argument!")
    sys.exit()
else:
    p_type = [0, 0]
    arg = sys.argv[1]
    if arg == "white":
        p_type[0] = 1
        w_bot = Agent()
    else:
        p_type[1] = 1
        b_bot = Agent()

# print('''****************************
#   Welcome to Console Chess
# ****************************
# White = Upper Case
# Black = Lower Case
# P,p = Pawn
# N,n = Knight
# B,b = Bishop
# R,r = Rook
# Q,q = Queen
# K,k = King
# When asked where you want to moves please use the following cordinate system:
# a8 b8 c8 d8 e8 f8 g8 h8
# a7 b7 c7 d7 e7 f7 g7 h7
# a6 b6 c6 d6 e6 f6 g6 h6
# a5 b5 c5 d5 e5 f5 g5 h5
# a4 b4 c4 d4 e4 f4 g4 h4
# a3 b3 c3 d3 e3 f3 g3 h3
# a2 b2 c2 d2 e2 f2 g2 h2
# a1 b1 c1 d1 e1 f1 g1 h1''')

chess_game = Chess()

while True:
    # if chess_game.p_move == 1:
    #     print('\nWhites Turn\n')
    # else:
    #     print('\nBlacks Turn\n')
    # chess_game.display()

    # User move (read from user input)
    if (chess_game.p_move == 1 and p_type[0] == 0) or (chess_game.p_move == -1 and p_type[1] == 0):
        next_move = input('')
        cur = next_move[:2]
        next = next_move[2:4]

        # If user's pawn is able to promote, read the last character for user's chocie
        if len(next_move) == 5:
            promote = next_move[-1].lower()

    # Agent move
    else:
        if chess_game.p_move == 1:
            cur, next = w_bot.choose_action(chess_game)
        else:
            cur, next = b_bot.choose_action(chess_game)

        game_copy = deepcopy(chess_game)
        agent_promote = ""
        if game_copy.move(cur, next) == True:
            if (p_type[0] == 1 and game_copy.p_move == 1) or (p_type[1] == 1 and game_copy.p_move == -1):
                state = game_copy.check_state(game_copy.EPD_hash())
                if state == 'PP':
                    agent_promote = "q"

        ##print('Agent generated move:')
        print(cur.lower() + next.lower() + agent_promote)

    valid = False
    if chess_game.move(cur, next) == False:
        print('Invalid move')
    else:
        valid = True
    if (p_type[0] == 1 and chess_game.p_move == 1) or (p_type[1] == 1 and chess_game.p_move == -1):
        state = chess_game.check_state(chess_game.EPD_hash())
        if state == '50M' or state == '3F':
            state = [0, 1, 0]  # Auto tie
        elif state == 'PP':
            chess_game.pawn_promotion(n_part='Q')  # Auto queen
        if state != [0, 1, 0]:
            state = chess_game.is_end()
    else:
        state = chess_game.is_end()
        if state == [0, 0, 0]:
            if chess_game.check_state(chess_game.EPD_hash()) == 'PP':
                chess_game.pawn_promotion(n_part=promote)   # Pawn promotion
    if sum(state) > 0:
        print('\n*********************\n      GAME OVER\n*********************\n')
        chess_game.display()
        print('Game Log:\n---------\n')
        print(f'INITIAL POSITION = {chess_game.init_pos}')
        print(f'MOVES = {chess_game.log}')
        print('\nGame Result:\n------------\n')
        if state == [0, 0, 1]:
            print('BLACK WINS')
        elif state == [1, 0, 0]:
            print('WHITE WINS')
        else:
            print('TIE GAME')
        break
    if valid == True:
        chess_game.p_move = chess_game.p_move * (-1)
