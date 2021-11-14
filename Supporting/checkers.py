import pygame
from .constants import Rows, Cols, Crown, Background, Khaki, black, white, marron, Width, Height

class Game:
    def __init__(self):
        self.graphics_object = Graphics()
        self.board_object = Board()
        self.turn = white
        # Define piece which is selected
        self.selected_piece = 0
        # Check if jumping is possible
        self.jump = False
        # List of all possible moves
        self.moves = []

    def ai_move(self,board):
        self.board_object = board
        self.end_turn()

    def update(self):
        self.graphics_object.draw_board(self.board_object, self.moves)

    # Change turns
    def end_turn(self):
        if self.turn == white:
            self.turn = black
        else:
            self.turn = white

        self.selected_piece = 0
        self.moves = []
        self.jump = False

    # Generates array with all moves
    def position_and_all_moves(self):
        Positions = []
        for row in range(Rows):
            for col in range(Cols):
                if self.board_object.get_piece(row, col) != 0 and (self.board_object.piece_movement(row, col, self.jump) != [] and self.board_object.get_piece(row, col).color == self.turn):
                    Positions.append(self.board_object.piece_movement(row, col, self.jump))
        return Positions

    # Select a piece 
    def select(self, mouse_pos):
        # if piece cannot make any moves, change turns
        if self.board_object.piece_movement == []:
            self.end_turn

        # Check movement of pieces 
        if self.jump == False:
            # Define selected piece
            if self.board_object.get_piece(mouse_pos[0], mouse_pos[1]) != 0 and self.board_object.get_piece(mouse_pos[0], mouse_pos[1]).color == self.turn:
                self.selected_piece = mouse_pos

            # if we select a valid move, then move piece
            elif self.selected_piece != 0 and mouse_pos in self.board_object.piece_movement(self.selected_piece[0], self.selected_piece[1]):
                # Determine king status prior to movement
                Piece_status_Prior = self.board_object.get_piece(self.selected_piece[0], self.selected_piece[1]).king
                # Move piece selected to mouse position
                self.board_object.move_piece(self.selected_piece[0], self.selected_piece[1], mouse_pos[0], mouse_pos[1])

                # Check if piece was a jump
                if mouse_pos not in self.board_object.adjacent(self.selected_piece[0], self.selected_piece[1]):
                    self.jump = True
                    # remove jumped piece
                    self.board_object.remove_piece(self.selected_piece[0] + (mouse_pos[0] - self.selected_piece[0]) // 2, self.selected_piece[1] + (mouse_pos[1] - self.selected_piece[1]) // 2, self.jump)
                    self.selected_piece = mouse_pos
                    # Determine king status after movement
                    Piece_status_Post = self.board_object.get_piece(self.selected_piece[0], self.selected_piece[1]).king
                    # If piece just became king end turn
                    if Piece_status_Post != Piece_status_Prior:
                        self.end_turn()
                else:
                    self.end_turn()

        # Check double jumps
        if self.jump == True:
            if self.selected_piece != 0 and mouse_pos in self.board_object.piece_movement(self.selected_piece[0], self.selected_piece[1], self.jump):
                Piece_status_Prior = self.board_object.get_piece(self.selected_piece[0], self.selected_piece[1]).king
                self.board_object.move_piece(self.selected_piece[0], self.selected_piece[1], mouse_pos[0], mouse_pos[1])
                self.board_object.remove_piece(self.selected_piece[0] + (mouse_pos[0] - self.selected_piece[0]) // 2, self.selected_piece[1] + (mouse_pos[1] - self.selected_piece[1]) // 2, self.jump)
                self.selected_piece = mouse_pos
                Piece_status_Post = self.board_object.get_piece(self.selected_piece[0], self.selected_piece[1]).king
                # If piece just became king end turn
                if Piece_status_Post != Piece_status_Prior:
                    self.end_turn()

            if self.board_object.piece_movement(mouse_pos[0], mouse_pos[1], self.jump) == []:
                self.end_turn()

class Graphics:
    def __init__(self):
        # Define window
        self.win = pygame.display.set_mode((Width, Height))
        pygame.init()
        # Update caption
        pygame.display.set_caption("Checkers")
        # Run game at stable 60 FPS
        pygame.time.Clock().tick(60)
        #Define Size of Squares
        self.Square_size = Width//Cols

    def draw_board(self, Board, moves):
        # Add background to Board
        self.win.blit(Background, (0,0))

        # Draw the board in the centre of the window 
        for row in range(Rows):
            for col in range(Cols):
                if (row + (1 - col % 2)) % 2 == 0:
                    pygame.draw.rect(self.win, marron, [(row * self.Square_size), self.Square_size * col, self.Square_size, self.Square_size])

        # Draw pieces on the board
        for row in range(Rows):
            for col in range(Cols):
                piece = Board.get_piece(row, col)
                if piece != 0:
                    # Define Radius of pieces, .35 is weight
                    radius = self.Square_size * .35
                    # How large we want outline of pieces, 0.02 is weight
                    OUTLINE = self.Square_size * 0.02
                    # Draw Outline
                    pygame.draw.circle(self.win, black, (self.Square_size * col + self.Square_size // 2, self.Square_size * row + self.Square_size // 2), radius + OUTLINE)
                    # Draw pieces
                    pygame.draw.circle(self.win, piece.color, (self.Square_size * col + self.Square_size // 2, self.Square_size * row + self.Square_size // 2), radius)
                    # Add Crown Img to Piece if King
                    if piece.king:
                        self.win.blit(Crown, (self.Square_size * col + self.Square_size // 2 - Crown.get_width()//2, self.Square_size * row + self.Square_size // 2 - Crown.get_height()//2))

        # # Draw all moves
        for move in moves: # process all moves
            # Define Radius of pieces, .35 is weight
            radius = self.Square_size * .35
            # Draw pieces
            pygame.draw.circle(self.win, Khaki, (self.Square_size * move[1] + self.Square_size // 2, self.Square_size * move[0] + self.Square_size // 2), radius)

        # Update Display of the game
        pygame.display.update()
        pygame.display.flip()

    # Used to determine piece coordinates using floor division
    def board_coords(self, X_Pos, Y_Pos):
        return (Y_Pos // self.Square_size, X_Pos // self.Square_size)

class Board():
    def __init__(self):
        # List of all pieces on the board in a matrix
        self.board = self.create_board()
        # Count of how many pieces each player has
        self.black_piece = self.white_piece = 12
        # Count of how many kings each player has
        self.black_kings = self.white_kings = 0

    # Create Pieces on Board
    def create_board(self):
        # Define empty matrix of pieces
        board = [[None] * 8 for i in range(8)]
        for row in range(Rows):
            for col in range(Cols):
                # Below determines which squares have pieces
                if (row + (1 - col % 2)) % 2 == 0:
                    # Draw pieces for player 1
                    if row < 3:
                        board[row][col] = (Piece(black, row, col))
                    # Draw pieces for player 2
                    elif row > 4:
                        board[row][col] = (Piece(white, row, col))
                    # Adds empty piece in all other locations 
                    else:
                        board[row][col] = 0
                else:
                    board[row][col] = 0

        return board

    # Give piece object 
    def get_piece(self, row, col):
        return self.board[row][col]

    # Define coordinates around a piece
    def potential_movement(self, dir, row, col):
        if dir == "forward_left":
            return (row - 1, col - 1)
        elif dir == "forward_right":
            return (row - 1, col + 1)
        elif dir == "backward_left":
            return (row + 1, col - 1)
        elif dir == "backward_right":
            return (row + 1, col + 1)
        else:
            return 0

    # Get all coordinates around piece
    def adjacent(self, row, col):
        return [self.potential_movement("forward_left", row, col), self.potential_movement("forward_right", row, col),
                self.potential_movement("backward_left", row, col),self.potential_movement("backward_right", row, col)]

    # Is coordinate on the board
    def on_board(self, row, col):
        if row < 0 or col < 0 or row > 7 or col > 7:
            return False
        else:
            return True

    # Define all possible movement of piece
    def piece_movement(self, row, col, jump = False):
        piece_movement = []

        # If an empty piece is selected return empty moves
        if self.get_piece(row, col) == 0:
            return []

        # Get all moves of selected piece
        if self.get_piece(row, col).king == False:
            if self.get_piece(row, col).color == white:
                All_Moves = [self.potential_movement("forward_left", row, col), self.potential_movement("forward_right", row, col)]
            elif self.get_piece(row, col).color == black:
                All_Moves = [self.potential_movement("backward_left", row, col), self.potential_movement("backward_right", row, col)]
        else:
            All_Moves = self.adjacent(row, col)

        # Populate moves from all potential moves
        for move in All_Moves:
            if jump == False:
                if self.on_board(move[0], move[1]):
                    # Checks if spot is empty
                    if self.get_piece(move[0], move[1]) == 0:
                        piece_movement.append(move)
                    # Check if jump move is a valid move
                    elif self.on_board(move[0]*2 - row, move[1]*2 - col):
                        # Checks if the spot that is not empty can be jumped
                        if self.get_piece(move[0]*2 - row, move[1]*2 - col) == 0 and self.get_piece(move[0], move[1]).color != self.get_piece(row, col).color and self.on_board(move[0]*2 - row, move[1]*2 - col):
                            piece_movement.append((move[0]*2 - row, move[1]*2 - col))

            else:
                # Check if move is valid move
                if self.on_board(move[0], move[1]) and self.get_piece(move[0], move[1]) != 0:
                    # Check if jump move is a valid move
                    if self.on_board(move[0]*2 - row, move[1]*2 - col):
                        # Checks if the spot that is not empty can be jumped
                        if self.get_piece(move[0], move[1]).color != self.get_piece(row, col).color and self.on_board(move[0]*2 - row, move[1]*2 - col) and self.get_piece(move[0]*2 - row, move[1]*2 - col) == 0:
                            piece_movement.append((move[0]*2 - row, move[1]*2 - col))

        return piece_movement

    # Function to move piece
    def move_piece(self, SP_X, SP_Y, MP_X, MP_Y):
        self.board[MP_X][MP_Y] = self.board[SP_X][SP_Y]

        # remove selected piece
        self.remove_piece(SP_X, SP_Y, False)

        # check if MP location is king location
        self.make_king(MP_X, MP_Y)


    # Remove a piece from board
    def remove_piece(self, row, col, jump):
        if jump:
            if self.get_piece(row, col).color == black:
                self.black_piece -= 1
                if self.get_piece(row, col).king == True:
                    self.black_kings -= 1
            else:
                self.white_piece -= 1
                if self.get_piece(row, col).king == True:
                    self.white_kings -= 1
        
        self.board[row][col] = 0

    # Define board parameters to make king piece
    def make_king(self, row, col):
        # if movement piece not already a king
        if self.get_piece(row, col).king == False:
            if self.get_piece(row, col).color == white and row == 0:
                self.get_piece(row, col).make_king()
                self.white_kings += 1

            elif self.get_piece(row, col).color == black and row == 7:
                self.get_piece(row, col).make_king()
                self.black_kings += 1

    # Define winner
    def winner(self):
        if self.black_piece <= 0:
            return black
        elif self.white_piece <= 0:
            return white

        return None

    # evaluation function
    def evaluate(self):
        # Note that the higher the multiple against king pieces the more likely the AI will prevent opponent from getting king pieces and work towards getting king piece
        return self.black_piece - self.white_piece + ((self.black_kings - self.white_kings)*0.5)

class Piece:
    def __init__(self, color, row, col, king = False):
        self.color = color
        self.king = king
        self.row = row
        self.col = col

    # Make King variable
    def make_king(self):
        self.king = True