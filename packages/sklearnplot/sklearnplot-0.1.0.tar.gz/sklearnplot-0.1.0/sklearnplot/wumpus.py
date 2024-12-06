import numpy as np

# Constants for the game
PIT = -1000
WUMPUS = -1000
GOLD = 1000
BREEZE = -10
STENCH = -10
STEP_COST = -1

# Symbols for display
SYMBOLS = {
    PIT: 'P',
    WUMPUS: 'W',
    GOLD: 'G',
    BREEZE: 'B',
    STENCH: 'S',
    0: '.'
}

# Function to add breeze around a pit
def add_breeze(score_grid, symbol_grid, x, y, n):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and symbol_grid[nx][ny] == '.':
            score_grid[nx][ny] = BREEZE
            symbol_grid[nx][ny] = 'B'

# Function to add stench around Wumpus
def add_stench(score_grid, symbol_grid, x, y, n):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and symbol_grid[nx][ny] == '.':
            score_grid[nx][ny] = STENCH
            symbol_grid[nx][ny] = 'S'

# Function to print the symbol matrix
def print_symbol_grid(symbol_grid, agent_position=None):
    n = len(symbol_grid)
    for i in range(n):
        row_str = ""
        for j in range(n):
            if agent_position == (i, j):
                row_str += ' A '  # Show the agent
            else:
                row_str += f' {symbol_grid[i][j]} '
        print(row_str)

# Function to print the score matrix
def print_score_grid(score_grid, agent_position=None):
    n = len(score_grid)
    for i in range(n):
        row_str = ""
        for j in range(n):
            if agent_position == (i, j):
                row_str += ' A '  # Show the agent
            else:
                row_str += f' {score_grid[i][j]:>4} '  # Show the score
        print(row_str)

# Initialize the game world
def initialize_wumpus_world(n):
    score_grid = np.zeros((n, n), dtype=int)
    symbol_grid = np.full((n, n), '.')  # Initialize the symbol grid with dots

    # Place pits, Wumpus, and gold at predefined positions
    pits = [(2, 2), (4, 1)]
    wumpus_position = (1, 4)
    gold_position = (3, 3)

    # Add pits and breezes
    for pit in pits:
        score_grid[pit] = PIT
        symbol_grid[pit] = 'P'
        add_breeze(score_grid, symbol_grid, pit[0], pit[1], n)

    # Add Wumpus and stench
    score_grid[wumpus_position] = WUMPUS
    symbol_grid[wumpus_position] = 'W'
    add_stench(score_grid, symbol_grid, wumpus_position[0], wumpus_position[1], n)

    # Add Gold
    score_grid[gold_position] = GOLD
    symbol_grid[gold_position] = 'G'

    return score_grid, symbol_grid

# Function to simulate agent movement
def move_agent(score_grid, symbol_grid, start, goal):
    n = len(score_grid)
    current_position = start
    score = 0

    while current_position != goal:
        x, y = current_position
        print(f"Agent at {current_position}, Current score: {score}")

        # Calculate penalties based on the current cell immediately upon arrival
        if score_grid[x][y] == BREEZE:
            print("Agent feels a breeze (-10)")
            score += BREEZE
        elif score_grid[x][y] == STENCH:
            print("Agent smells stench (-10)")
            score += STENCH

        # Check for pit or Wumpus immediately upon arrival
        if score_grid[x][y] == PIT or score_grid[x][y] == WUMPUS:
            score += score_grid[x][y]
            print(f"Game Over! Fell into {'Pit' if score_grid[x][y] == PIT else 'Wumpus'}. Final Score: {score}")
            return score

        # Simple movement logic towards the goal
        if x < goal[0]:
            x += 1
        elif y < goal[1]:
            y += 1

        current_position = (x, y)
        score += STEP_COST  # Apply step cost after moving

    # Reached the gold
    score += GOLD
    print(f"Gold found at {current_position}! Final Score: {score}")
    return score

# # Main execution
# if _name_ == "_main_":
#     n = 5  # Grid size (5x5)

#     # Initialize the Wumpus world with score and symbol grids
#     score_grid, symbol_grid = initialize_wumpus_world(n)

#     # Print the initial Wumpus world grids
#     start_position = (0, 0)
#     print("Initial Wumpus World Symbol Grid:")
#     print_symbol_grid(symbol_grid, agent_position=start_position)

#     # Define the goal (gold position)
#     gold_position = (3, 3)  # You can choose different or random positions

#     # Simulate the agent's movement and calculate the final score
#     final_score = move_agent(score_grid, symbol_grid, start_position, gold_position)

#     # Print the final score
#     print(f"\nFinal Score: {final_score}")