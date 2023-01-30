
import numpy as np
#from colorama import just_fix_windows_console

from agent import agent
from game import print_board, place_stone, check_win


# Uncomment if colors are not displayed on Windows.
#just_fix_windows_console()

# The game board.
# 0 means empty, 1 means red and 2 means blue.
board = np.zeros((7, 7), dtype="int8")

# Whether or not a stone is connected to a side.
# 0 means it's not connected to either of the sides of its color.
# 1 means it's connected to the first side and
# 2 means it's connected to the other side.
connections = np.zeros((7, 7), dtype="int8")

## For test
# board = np.array([
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# ])
# connections = np.array([
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0],
# ])


if __name__ == "__main__":

    # 1 is the player (red) and 2 is the agent (blue)
    player = 1 if input("\nDo you want to go first? ").lower() != "n" else 2
    print_board(board)
    game_over = False

    while not game_over:
        if player == 1:
            placed = False
            while not placed:
                inp = input("Enter stone: ").split()
                i, j = int(inp[0]), int(inp[1])
                placed = place_stone(board, connections, player, i, j)
        elif player == 2:
            i, j = agent(board, connections)
            place_stone(board, connections, player, i, j)

        print_board(board, i, j)
        game_over = check_win(board, connections, i, j)
        player ^= 3     # Switch players

    winner = "\033[31;5mRED" if game_over == 1 else "\033[34;5mBLUE"
    print("Winner:", winner, "\033[0m")
