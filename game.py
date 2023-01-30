
def print_board(board, li=0, lj=0):
    """Print the game board.

    The arguments 'li' and 'lj' are used to provide
    the coordinates of the last stone that was placed on the board.
    """

    print("\033c\n")
    print("    \033[31m0 1 2 3 4 5 6\033[0m")
    if board[li, lj] == 2:
        # It is set to 3 to denote that it's a new blue stone.
        # It'll be fixed after printing.
        board[li, lj] = 3

    for i in range(7):
        print(f"{' '*i} \033[34m{i}\033[0m  ", end="")

        for j in range(7):
            if board[i, j] == 1:      # Red
                print("\033[31mO\033[0m ", end="")
            elif board[i, j] == 2:      # Blue
                print("\033[34mO\033[0m ", end="")
            elif board[i, j] == 3:      # newly placed Blue
                print("\033[34mC\033[0m ", end="")
                board[i, j] = 2     # not new anymore
            else:
                print("- ", end="")
        print(f" \033[34m{i}\033[0m ")

    print(" "*10, "\033[31m0 1 2 3 4 5 6\033[0m")
    print("_"*30, "\n")


def get_neighbors(board, i, j):
    """Return a list of same colored neighbors of a stone in [i, j]."""
    neighbors = []
    cells = [(i, j-1), (i, j+1), (i-1, j), (i+1, j), (i-1, j+1), (i+1, j-1)]
    # For all six cells around this one:
    for ni, nj in cells:
        # If it's not out of the borders and has a stone with the same color:
        if 0 <= ni < 7 and 0 <= nj < 7 and board[ni, nj] == board[i, j]:
            neighbors.append((ni, nj))
    return neighbors


def check_win(board, connections, i, j):
    """Check if the game is over after placing a stone in [i, j]."""
    # The side that this stone is connected to:
    side = connections[i, j]
    for ni, nj in get_neighbors(board, i, j):
        # If the stone has a connected neighbor:
        if connections[ni, nj]:
            # If the stone is also connected to the other side:
            if side and side != connections[ni, nj]:
                return board[i, j]      # return the winner
            side = connections[ni, nj]
    return 0


def update_connectivity(board, connections, i, j):
    """Update the connectivity status of this stone."""
    neighbors = get_neighbors(board, i, j)

    # Connected through its neighbors:
    for ni, nj in neighbors:
        if connections[ni, nj]:
            connections[i, j] = connections[ni, nj]
            break

    # Directly connected to a side:
    if board[i, j] == 1:
        # A red stone could be connected to the top or bottom row.
        if i == 0:
            connections[i, j] = 1
        elif i == 6:
            connections[i, j] = 2
    elif board[i, j] == 2:
        # A blue stone could be connected to the left or right column.
        if j == 0:
            connections[i, j] = 1
        elif j == 6:
            connections[i, j] = 2

    # If this stone is updated, also update all of its neighbors.
    if connections[i, j]:
        for ni, nj in neighbors:
            # A neighbor that already has a value doesn't need to be updated.
            if not connections[ni, nj]:
                update_connectivity(board, connections, ni, nj)


def place_stone(board, connections, player, i, j):
    """Place a stone in coordinate [i, j] of the board.

    Returns whether the stone was placed successfully or not.
    """

    # If the input is invalid (out of borders or already filled):
    if i < 0 or i > 6 or j < 0 or j > 6 or board[i, j] != 0:
        return False
    board[i, j] = player
    update_connectivity(board, connections, i, j)
    return True
