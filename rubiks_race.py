import heapq
from termcolor import colored
from random import choice
from collections import Counter
from reader import read_input_file
from reader import path
from collections import defaultdict

file_name_initial = 'inicial.txt'
file_name_meta = 'meta.txt'

i_3x3 = [6, 7, 8, 11, 12, 13, 16, 17, 18]
    
color_abbreviation = {
        'V': 'green',
        'B': 'white',
        'R': 'red',
        'A': 'yellow',
        'N': 'orange',
        'Z': 'blue',
        '*': 'black'
}

# Class to represent the state of the 8-puzzle
class PuzzleState:
    def __init__(self, board, parent, move, depth, cost):
        self.board = board  # The puzzle board configuration
        self.parent = parent  # Parent state
        self.move = move  # Move to reach this state
        self.depth = depth  # Depth in the search tree
        self.cost = cost  # Cost (depth + heuristic)

    def __lt__(self, other):
        return self.cost < other.cost

def flatten(lst):
    return [item for sublist in lst for item in sublist]

def validate_file_state(file_state, goal, min_size=3):
    # Check it has at least 3 rows and 3 columns
        if len(file_state) < min_size or any(len(row) < min_size for row in file_state):
             raise ValueError(f'The board must have at least {min_size}x{min_size} dimensions')
        
    # Check it has only valid colors
        colors = set(flatten(file_state))
        invalid_colors = colors - set(color_abbreviation.keys())
        if invalid_colors:
            raise ValueError(f'Invalid colors found: {invalid_colors}, must be one of {color_abbreviation.keys()}')
    
        if goal == False:
            # Check color count, each color must have (n*n)-1/6 pieces
            n = len(file_state)
            total_blocks = n*n
            colors = ['V', 'B', 'R', 'A', 'N', 'Z']
            blocks_per_color = (total_blocks - 1) // 6 # Expected quantity of each color

            expected_counts = {color: blocks_per_color for color in colors}
            expected_counts['*'] = 1 #  There is only one black block

            # Count the actual number of blocks of each color
            actual_counts = Counter(color for row in file_state for color in row)

            # Validate the difference between the expected and actual counts
            invalid_counts = {color: actual_counts.get(color, 0) - expected_counts.get(color, 0) 
                            for color in expected_counts if actual_counts.get(color, 0) != expected_counts.get(color, 0)}

            if invalid_counts:
                raise ValueError(f'Invalid color count. Must have {blocks_per_color} blocks per color, and 1 black block.')

def generate_initial_state_from_file(file_name, goal=False):
    file_state = read_input_file(file_name)
    try:
        validate_file_state(file_state, goal)
    except ValueError as e:
        print(e)
        exit(1)

    n = len(file_state)

    grid = [[[color for color in row] for row in file_state]]
    initial_state = flatten(flatten(grid))
    return initial_state

def generate_goal_state_from_file(file_name, goal=True):
    file_state = read_input_file(file_name)
    try:
        validate_file_state(file_state, goal)
    except ValueError as e:
        print(e)
        exit(1)

    n = len(file_state)

    grid = [[[color for color in row] for row in file_state]]
    goal_state = flatten(flatten(grid))
    return goal_state
    
# Function to display the board in a visually appealing format
def print_board(board, size=5):
    print("+" + "---+" * size)
    for row in range(0, size * size, size):
        row_visual = "|"
        for tile in board[row:row + size]:
            if tile == "*":  # Blank tile
                row_visual += f" {colored(' ', 'cyan')} |"
            else:
                row_visual += f" {colored(tile, 'yellow')} |"
        print(row_visual)
        print("+" + "---+" * size)

# Possible moves for the blank tile (up, down, left, right)
moves = {
    'D': -5,  # Move up
    'U': 5,   # Move down
    'R': -1,  # Move left
    'L': 1    # Move right
}

def calculate_goal_positions(goal_state):
    goal_positions = defaultdict(list)
    for i, color in enumerate(goal_state):
        goal_positions[color].append((i // 3 + 1, i % 3 + 1))  # Guarda coordenadas (fila, columna)
    return goal_positions

def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Function to calculate the heuristic (Manhattan distance)
def heuristic(board):
    total_distance = 0
    for i, color in enumerate(board):
        for y,x in [divmod(i, 5)]:
            if i in i_3x3:
                if board[i] != '*' and goal_postions[color]:
                    total_distance += min(manhattan_distance((y,x), pos) for pos in goal_postions[color])
                if color != goal_state[(y-1)*3+(x-1)]:
                    total_distance += 1
    return total_distance

# Function to get the new state after a move
def move_tile(board, move, blank_pos):
    new_board = board[:]
    new_blank_pos = blank_pos + moves[move]
    new_board[blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[blank_pos]
    return new_board

# A* search algorithm
def a_star(start_state, goal_state):
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, PuzzleState(start_state, None, None, 0, heuristic(start_state)))

    while open_list:
        current_state = heapq.heappop(open_list)
        current_state_goal_positions = [current_state.board[i] for i in i_3x3]

        if current_state_goal_positions == goal_state:
            return current_state
        
        closed_list.add(tuple(current_state.board))

        blank_pos = current_state.board.index("*")

        for move in moves:
            if move == 'D' and blank_pos < 5:  # Invalid move up
                continue
            if move == 'U' and blank_pos > 19:  # Invalid move down
                continue
            if move == 'R' and blank_pos % 5 == 0:  # Invalid move left
                continue
            if move == 'L' and blank_pos % 5 == 4:  # Invalid move right
                continue
            new_board = move_tile(current_state.board, move, blank_pos)

            if tuple(new_board) in closed_list:
                continue
            new_state = PuzzleState(new_board, current_state, move, current_state.depth + 1, current_state.depth + 1 + heuristic(new_board))
            heapq.heappush(open_list, new_state)

    return None


# Function to print the solution path
def print_solution(solution):
    path = []
    current = solution
    while current:
        path.append(current)
        current = current.parent
    path.reverse()

    for step in path:
        print(f"Move: {step.move}")
        print_board(step.board)

initial_state = generate_initial_state_from_file(file_name_initial)
goal_state = generate_goal_state_from_file(file_name_meta)
goal_postions = calculate_goal_positions(goal_state)

print_board(initial_state)
print_board(goal_state, 3)

solution = a_star(initial_state, goal_state)

# Print the solution
if solution:
    print(colored("Solution found:", "green"))
    print_solution(solution)
else:
    print(colored("No solution exists.", "red"))

