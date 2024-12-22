import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from parser import Parser
from collections import deque

def print_board(board):
    for row in board:
        print(''.join(row))

def bfs(board, y, x):
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    seen = set()
    queue = deque([(y, x, 0)])
    bottom_pos = (len(board) - 1, len(board[0]) - 1)
    while queue:
        y, x, count = queue.popleft()
        if (y, x) == bottom_pos:
            return count
        if y < 0 or y >= len(board) or x < 0 or x >= len(board[0]):
            continue
        if board[y][x] == '#' or (y, x) in seen:
            continue
        seen.add((y, x))
        for dy, dx in directions:
            queue.append((y + dy, x + dx, count + 1))
    return -1

def populate_board(board, coord):
    board[coord[1]][coord[0]] = '#'
    return board

if __name__ == "__main__":
    coords = Parser(file_path='input.txt').parse_lines(int, delimiter=',')
    board = [['.' for _ in range(71)] for _ in range(71)] # hard coded to 71 but for small example you would set this to 7.
    for i in range(len(coords)):
        board = populate_board(board, coords[i])
        if bfs(board, 0, 0) == -1:
            print("Failed at ", i, 'with coord: ', coords[i])
            break
