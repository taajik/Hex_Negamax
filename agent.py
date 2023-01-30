
import numpy as np

from game import place_stone, check_win, get_neighbors


def get_group(board, i, j, group, size):
    """Given a stone in coordinates [i, j], find all stones
    that are connected to it; constituting a group.

    Size of this group specifies the start and end
    of its width or height, depending on the color.
    """

    # Either width or height. The other one doesn't matter.
    s = i if board[i, j] == 1 else j
    # Find minimum
    if s < size[0]:
        size[0] = s
    # Find maximum
    if s > size[1]:
        size[1] = s

    group.append((i, j))
    for ni, nj in get_neighbors(board, i, j):
        if (ni, nj) not in group:
            get_group(board, ni, nj, group, size)


def heuristic_for_color(board, player):
    """Given a board, calculate the heuristic value for only one color.

    Heuristic value is calculated based on the lengths of groups for a color.
    It is the result of concatenating the lengths
    of top four longest groups (if exist).

    For example if the color blue has three groups with the following length:
    [1, 3, 1]
    The heuristic value will be: 3110
    """

    seen = set()
    lengths = []
    for i in range(7):
        for j in range(7):
            # If this stone is not in one of the groups that have been seen:
            if board[i, j] == player and (i, j) not in seen:

                # Result of 'get_group' will be saved in these arrays:
                group = []
                size = [7, -1]
                get_group(board, i, j, group, size)
                lengths.append(str(size[1] - size[0] + 1))
                seen = seen.union(group)

    # Calculate the heuristic value
    lengths.sort(reverse=True)
    return int("".join(lengths)[:4].ljust(4, "0"))


# def heuristic_for_color(board, player):
#     """Heuristic function based on the length of longest group."""
#     seen = set()
#     max_length = 0
#
#     for i in range(7):
#         for j in range(7):
#             if board[i, j] == player and (i, j) not in seen:
#                 group = []
#                 size = [7, -1]
#                 get_group(board, i, j, group, size)
#
#                 length = size[1] - size[0] + 1
#                 if length > max_length:
#                     max_length = length
#                 seen = seen.union(group)
#
#     return max_length


def negamax(board, connections, player, alpha, beta, depth):
    """The Negamax algorithm with alpha-beta pruning.

    Note: The heuristic value is equal to the difference of calling
    the 'heuristic_for_color' function for both colors.
    """

    best_value = -np.inf
    best_move = ()
    if depth <= 0:
        # Heuristic value for the opponent
        opp_value = heuristic_for_color(board, player^3)

    for i in range(7):
        for j in range(7):
            if board[i, j] == 0:
                # Trial move with stone in [i, j]
                board_c = board.copy()
                connections_c = connections.copy()
                place_stone(board_c, connections_c, player, i, j)

                if check_win(board_c, connections_c, i, j):
                    return 20000, (i, j)
                if depth <= 0:
                    # The heuristic value
                    value = heuristic_for_color(board_c, player) - opp_value
                else:
                    value = -negamax(board_c, connections_c, player^3,
                                     -beta, -alpha, depth-1)[0]

                if value > best_value:
                    best_value = value
                    best_move = (i, j)
                alpha = max(alpha, value)
                if beta <= alpha:
                    # Prune
                    return best_value, best_move

    return best_value, best_move


def agent(board, connections):
    """The AI agent.

    Given a board, it will choose a move by
    running the Negamax algorithm with the specified depth.
    """

    return negamax(board, connections, 2, -10000, 10000, 3)[1]
