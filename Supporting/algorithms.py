from copy import deepcopy
from Supporting.constants import Rows, Cols, black, white

# Position is board object
def alpha_beta_algorithm(game, board, depth, max_player, alpha, beta):
    if depth == 0 or board.winner() != None:
        return board.evaluate(), board
    
    if max_player:
        maxEval = float('-inf')
        best_board = None

        # If piece is left without any moves skip players move
        All_boards = get_all_boards(game, board, black)
        if All_boards == []:
            evaluation = alpha_beta_algorithm(game, board, depth - 1, False, alpha, beta)[0]
            maxEval = max(maxEval, evaluation)

            alpha = max(alpha, evaluation)
            if maxEval == evaluation:
                best_board = board

        for board in All_boards:
            evaluation = alpha_beta_algorithm(game, board, depth - 1, False, alpha, beta)[0]
            maxEval = max(maxEval, evaluation)

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            if maxEval == evaluation:
                best_board = board

        return maxEval, best_board

    else:
        minEval = float('inf')
        best_board = None

        All_boards = get_all_boards(game, board, white)
        # If piece is left without any moves skip players move
        if All_boards == []:
            evaluation = alpha_beta_algorithm(game, board, depth - 1, True, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if minEval == evaluation:
                best_board = board

        for board in All_boards:
            evaluation = alpha_beta_algorithm(game, board, depth - 1, True, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if minEval == evaluation:
                best_board = board

        return minEval, best_board

# Returns list of all board states of all moves in a single turn
def get_all_boards(game, board, color):
    Board_States = []
    for movements in position_and_all_moves(game, board, color):
        for position in movements[2]:
            board_clone = deepcopy(board)
            Clone_Board_Movement(game, board_clone, movements, position, color)
            Board_States.append(board_clone)
    return Board_States

# Generates matrix with piece and all it's moves
def position_and_all_moves(game, board, color):
    Positions = []
    for row in range(Rows):
        for col in range(Cols):
            if board.get_piece(row, col) != 0 and (board.piece_movement(row, col, game.jump) != [] and board.get_piece(row, col).color == color):
                Positions.append((row, col, board.piece_movement(row, col, game.jump)))
    return Positions

# Generate movements on deepcopy board
def Clone_Board_Movement(game, board, piece, move, color, jump=False):
    if jump == False:
        # if piece in movement is not empty and is not the same as the turns piece
        if board.get_piece(move[0], move[1]) != 0 and board.get_piece(move[0], move[1]).color == color:
            piece = move

        # If piece exists and movement of piece is a possible move
        elif piece != 0 and move in board.piece_movement(piece[0], piece[1]):

            # Determine king status prior to movement
            Piece_status_Prior = board.get_piece(piece[0], piece[1]).king    
            # move piece
            board.move_piece(piece[0], piece[1], move[0], move[1])

            # if piece movement is not adjacent to the piece, we jumped
            if move not in board.adjacent(piece[0], piece[1]):
                # remove jumped piece
                board.remove_piece(piece[0] + (move[0] - piece[0]) // 2, piece[1] + (move[1] - piece[1]) // 2, True)
                piece = move

                # Determine king status after movement
                Piece_status_Post = board.get_piece(piece[0], piece[1]).king  
                # If piece just became king end turn
                if Piece_status_Post != Piece_status_Prior:
                    return
                
                # populate all new movesments
                move = board.piece_movement(piece[0], piece[1], True)
                # if we can move again recursive
                if move != []:
                    Clone_Board_Movement(game, board, piece, move[0], color, True)

    # in the case we jumped
    if jump == True:
        # If piece exists and movement of piece is a possible move
        if piece != 0 and move in board.piece_movement(piece[0], piece[1], jump):
            Piece_status_Prior = board.get_piece(piece[0], piece[1]).king  
            # move piece
            board.move_piece(piece[0], piece[1], move[0], move[1])
            # remove jumped piece
            board.remove_piece(piece[0] + (move[0] - piece[0]) // 2, piece[1] + (move[1] - piece[1]) // 2, True)

        # Check if we can we move again
        if board.piece_movement(move[0], move[1], game.jump) == []:
            return

        else:
            piece = move
            Piece_status_Post = board.get_piece(piece[0], piece[1]).king  
            if Piece_status_Post != Piece_status_Prior:
                return
            move = board.piece_movement(piece[0], piece[1], True)
            if move != []:
                Clone_Board_Movement(game, board, piece, move[0], color, True)