# Checkers Game

A fully functioning checkers game made in python 3 with detailed commentary. Base game implements Minimax algorithm with alpha-beta pruning. 
Two player option available if you comment out the AI section in main.py file (line 12 - 14). Game has the following rules:

- White player always opens the game.
- Non-king pieces always move diagonally and forward.
- A piece making a non-capturing move may move only one square.
- A piece can capture another piece in a straight diagonal line if the landing location is empty and defined on the board. 
- A piece can make additional jumps if as per above comment rules.
- When a piece is captured, it is removed from the board.
- Players are not required to make captures when they are present. Similarily, players are not required to make additional captures. 
- When a piece reaches the furthest row, it is crowned and becomes a king.
- Kings are limited to moving diagonally but can move both forward and backward.
- Kings may combine jumps in several directions (forward and backward) on the same turn.
- If a piece is jumped and the jumping piece becomes a king, it cannot make additional moves. 
- A player wins the game when all the opponent pieces are captured.
- In the case where a player cannot make additional moves, their turn is skipped. 

## How to run game
- Download all files from github
- pip install pygame
- run main.py file

## Minimax with Alpha-Beta Pruning

I used Minimax algorithm with alpha-beta pruning to develop an AI player. 
Amazing explaination below on:

https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague

## Visualization of the game board

<p align="center">
  <img src="https://user-images.githubusercontent.com/88753168/141701806-a567e20a-c614-4d34-9518-40ae00850396.png">
</p>

# Potential Improvements I am thinking of implementing at a later date

- Menu feature to implement difficulty. To increase/decrease difficulty now update k value in main.py file for alpha_beta_algorithm.
- Menu feature to implement two player. To implement this now please comment out AI section in main.py file (line 12 - 14).
- Algorithm does not account for all possible second jumps available only the first one. Please refer to line 107 and 130 in algorithm.py (Move[0]).
- Improve evaluation function, currently using: black_piece - white_piece + ((black_kings - white_kings)*0.5).
- Implement AI for both pieces, currently only AI impmeneted for black_pieces.
- Add random function for who starts the game.
- Need to incorporate stalemate feature, specifically in the case where both players cannot make any more moves. Currently leads to an endless loop.

# Feedback
- Any feedback would be greatly appreciated. Please send me an email at amancheema6793@gmail.com
