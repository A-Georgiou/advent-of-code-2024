import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from parser import Parser
from collections import deque

def print_board(board):
    for row in board:
        print(' '.join([str(x) for x in row]))

def initialise_counts(board, start_y, start_x, end_y, end_x):
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    seen = set()
    queue = deque([(start_y, start_x, 0)])
    board[start_y][start_x] = 0
    bottom_pos = (len(board) - 1, len(board[0]) - 1)
    while queue:
        y, x, count = queue.popleft()
        if (y, x) == (end_y, end_x):
            board[y][x] = count
            return board
        if y < 0 or y >= len(board) or x < 0 or x >= len(board[0]):
            continue
        if board[y][x] == '#' or (y, x) in seen:
            continue
        seen.add((y, x))
        board[y][x] = count
        for dy, dx in directions:
            queue.append((y + dy, x + dx, count + 1))
    return board

def cheat_iter(board):
    cheat_map = {}
    directions = [[0, 2], [2, 0], [0, -2], [-2, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if type(board[i][j]) == int:
                curr_val = board[i][j]
                for dy, dx in directions:
                    new_y, new_x = i + dy, j + dx
                    if new_y < 0 or new_y >= len(board) or new_x < 0 or new_x >= len(board[0]):
                        continue
                    if type(board[new_y][new_x]) == int:
                        next_val = board[new_y][new_x]
                        diff = next_val - curr_val
                        if diff > 0:
                            if diff not in cheat_map:
                                cheat_map[diff] = []
                            cheat_map[diff].append([curr_val, next_val])
    return cheat_map

def find_start(board):
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 'S':
                return (i, j)
def find_end(board):
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 'E':
                return (i, j)

if __name__ == "__main__":
    board = Parser(file_path='input.txt').parse_lines(list, flatten=True)
    start = find_start(board)
    end = find_end(board)
    board = initialise_counts(board, start[0], start[1], end[0], end[1])
    count = 0
    for key, value in cheat_iter(board).items():
        if key-2 >= 100:
            count += len(value)
    print("Cheats that save over 100 picosends:", count)

    