import pygame
from Supporting.checkers import Game, white, black
import ctypes
from Supporting.algorithms import alpha_beta_algorithm

def main():
    game = Game()
    running = True

    while running:
        # alpha beta algorithm algorithm
        if game.turn == black:
            evaluation, new_board = alpha_beta_algorithm(game, game.board_object, 4, True, alpha=-float('inf'), beta=float('inf'))
            game.ai_move(new_board)

        # check is winner
        if game.board_object.winner() != None:
            if game.turn == white:
                ctypes.windll.user32.MessageBoxW(0, "Black Wins!", "Game Over", 1)
            else:
                ctypes.windll.user32.MessageBoxW(0, "White Wins", "Game Over", 1)
            running = False

        # Determine coordinates of mouse
        X_Pos, Y_Pos = pygame.mouse.get_pos()

        # determine piece in coordinates of mouse
        mouse_pos = game.graphics_object.board_coords(X_Pos, Y_Pos)

        # if player cannot make any moves, change turns
        if game.position_and_all_moves() == []:
            game.end_turn()

        # Define moves of selected piece
        if game.selected_piece != 0:
            game.moves = game.board_object.piece_movement(game.selected_piece[0], game.selected_piece[1], game.jump)

        # Get events from the queue
        for event in pygame.event.get():
            # Check if player closed game
            if event.type == pygame.QUIT:
                running = False 

            # Check if player pressed any mouse key
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.select(mouse_pos)

        game.update()

# Only allows file to be run directly
if __name__ == "__main__":
    main()