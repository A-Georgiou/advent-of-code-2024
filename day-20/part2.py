import os
import sys
from collections import deque, defaultdict
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from parser import Parser

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

def manhattan_distance(y1, x1, y2, x2):
    return abs(y2 - y1) + abs(x2 - x1)

def find_reachable_points(board, start_y, start_x, max_steps):
    height, width = len(board), len(board[0])
    reachable = defaultdict(lambda: float('inf'))
    queue = deque([(start_y, start_x, 0)])
    seen = set()
    
    while queue:
        y, x, steps = queue.popleft()
        
        if isinstance(board[y][x], int) and (y, x) != (start_y, start_x):
            reachable[(y, x)] = min(reachable[(y, x)], steps)
            
        if steps >= max_steps:
            continue
            
        for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_y, new_x = y + dy, x + dx
            new_steps = steps + 1
            if not (0 <= new_y < height and 0 <= new_x < width):
                continue
            state = (new_y, new_x, new_steps)
            if state in seen:
                continue
                
            seen.add(state)
            queue.append((new_y, new_x, new_steps))
    
    return {k: v for k, v in reachable.items() if v <= max_steps}

def get_normal_distance(board, start_y, start_x, end_y, end_x):
    if not isinstance(board[start_y][start_x], int) or not isinstance(board[end_y][end_x], int):
        return float('inf')
    return abs(board[end_y][end_x] - board[start_y][start_x])

def find_cheats(board, max_cheat_steps=20):
    cheats = defaultdict(int)
    height, width = len(board), len(board[0])
    seen_pairs = set()
    
    for i in range(height):
        for j in range(width):
            if not isinstance(board[i][j], int):
                continue
            
            reachable = find_reachable_points(board, i, j, max_cheat_steps)
            
            for (end_y, end_x), cheat_steps in reachable.items():
                normal_dist = get_normal_distance(board, i, j, end_y, end_x)
                if normal_dist == float('inf'):
                    continue
                
                pair = tuple(sorted([(i, j), (end_y, end_x)]))
                if pair in seen_pairs:
                    continue
                
                time_saved = normal_dist - cheat_steps
                if time_saved > 0:
                    cheats[time_saved] += 1
                    seen_pairs.add(pair)
    return cheats

if __name__ == "__main__":
    board = Parser(file_path='input.txt').parse_lines(list, flatten=True)
    start = find_start(board)
    end = find_end(board)
    board = initialise_counts(board, start[0], start[1], end[0], end[1])
    cheat_savings = find_cheats(board)
    result = sum(count for time_saved, count in cheat_savings.items() 
              if time_saved >= min_time_saved)
    print("Number of cheats saving ≥100 picoseconds:", result)