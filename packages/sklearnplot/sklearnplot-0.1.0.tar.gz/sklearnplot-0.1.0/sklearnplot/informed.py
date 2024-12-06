import time
import random
import math
from collections import deque
import heapq


def value(node,heurestic_values = None):
    if heurestic_values == None:
        x = str(node)
        y = 0
        for i in  x:
            y += ord(i)

        return y
    else:
        return heurestic_values[node]

def hill_climbing(graph,start,heurestic_values=None):
    start_time = time.time()

    current = start
    while True:
        neighbors = graph.get(current,[])
        next_node = None
        highest_value = value(current,heurestic_values)
        for neighbour, weight in neighbors:
            if value(neighbour,heurestic_values) > highest_value:
                next_node = neighbour
                highest_value = value(neighbour,heurestic_values)


        if next_node is None or value(next_node,heurestic_values) <= value(current,heurestic_values):
            end_time = time.time()
            time_elapsed = end_time - start_time
            print(f"Time Elapsed: {time_elapsed}")
            return current
        
        current = next_node
        
def simulated_annealing(graph,start,heuristic_values = None,T = 1000.0, alpha = 0.9):
    #  T is initial temperature and alpha is cooling rate.
    start_time = time.time()
    current = start
    T_min = 1e-8
    while T> T_min:
        neighbors = graph.get(current,[])
        if not neighbors:
            break
        neighbor , weight  = random.choice(neighbors)
        delta = value(neighbor,heuristic_values) - value(current,heuristic_values)
        if delta > 0:
            current = neighbor
        else:
            p =math.exp(delta/T)
            if random.random() < p:
                current = neighbor

        T *= alpha

    end_time = time.time()
    time_elapsed = end_time - start_time
    print(f"Time Elapsed: {time_elapsed}")
    return current

def reconstruct_path(parent_map, current_node, total_cost):
    path = []
    while current_node:
        path.append(current_node)
        current_node = parent_map[current_node]
    path.reverse()
    print(f"Path: {path}")
    print(f"Total cost: {total_cost}")

def a_star(graph, heurestic_values, start, goal):
    open_list = {start: 0}
    closed_list = set()
    g_score = {start: 0}
    parent_map = {start: None}
    start_time = time.time()

    while open_list:
        current_node = min(open_list, key=lambda n: open_list[n])
        
        if current_node == goal:
            end_time = time.time()
            total_time = end_time - start_time
            print(f"Time taken to complete {total_time}")
            return reconstruct_path(parent_map, current_node, g_score[current_node])
        
        del open_list[current_node]
        closed_list.add(current_node)
        
        for neighbor, cost in graph[current_node]:
            if neighbor in closed_list:
                continue
            
            tentative_g_score = g_score[current_node] + cost

            if neighbor not in open_list or tentative_g_score < g_score.get(neighbor, float('inf')):
                parent_map[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heurestic_values[neighbor]
                open_list[neighbor] = f_score
                
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Time taken to complete {total_time}")
    
    return None


def a_star_8puzzle():
    # Define the goal state
    GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))  # 0 represents the blank tile

    # Helper function to locate the position of the blank tile (0)
    def find_blank(board):
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 0:
                    return i, j

    # Heuristic: Number of misplaced tiles
    def heuristic(state, goal=GOAL_STATE):
        misplaced = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0 and state[i][j] != goal[i][j]:
                    misplaced += 1
        return misplaced

    # Generate neighbors by sliding the blank tile (0)
    def get_neighbors(state):
        neighbors = []
        i, j = find_blank(state)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for di, dj in directions:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in state]
                new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
                neighbors.append(tuple(tuple(row) for row in new_state))
        return neighbors

    # Reconstruct the path from start to goal
    def reconstruct_path(came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    # A* Search for 8-puzzle problem
    def a_star_puzzle(start):
        frontier = [(0, start)]  # List instead of heap (priority, state)
        came_from = {}
        cost_so_far = {start: 0}

        while frontier:
            # Sort frontier by priority (lowest priority first) and pop the first element
            frontier.sort(key=lambda x: x[0])
            _, current = frontier.pop(0)

            if current == GOAL_STATE:
                return reconstruct_path(came_from, current), cost_so_far[current]

            for neighbor in get_neighbors(current):
                new_cost = cost_so_far[current] + 1  # Every move has a cost of 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor)
                    frontier.append((priority, neighbor))
                    came_from[neighbor] = current

        return None  # If no solution found
    
    
def hill_climbing_8queens(n):
    def calculate_conflicts(board):
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_neighbors(board):
        neighbors = []
        for row in range(n):
            for col in range(n):
                if col != board[row]:
                    neighbor = board[:]
                    neighbor[row] = col
                    neighbors.append(neighbor)
        return neighbors

    board = [random.randint(0, n - 1) for _ in range(n)]
    while True:
        current_conflicts = calculate_conflicts(board)
        if current_conflicts == 0:
            return board
        neighbors = get_neighbors(board)
        board = min(neighbors, key=calculate_conflicts)
        
def dfs_n_queens(n):
    solutions = []
    stack = [[]]

    while stack:
        state = stack.pop()
        row = len(state)
        if row == n:
            solutions.append(state)
            continue

        for col in range(n-1, -1, -1):  # Reverse order for stack
            if is_safe(state, row, col):
                stack.append(state + [col])
    return solutions


def bfs_n_queens(n):
    queue = deque()
    queue.append([])
    solutions = []

    while queue:
        state = queue.popleft()
        row = len(state)
        if row == n:
            solutions.append(state)
            continue

        for col in range(n):
            if is_safe(state, row, col):
                queue.append(state + [col])
    return solutions

def is_safe(state, row, col):
    for r, c in enumerate(state):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def hill_8queens():
    def hill_climbing_n_queens(n):
        current = random_state(n)
        while True:
            conflicts = calculate_conflicts(current)
            if conflicts == 0:
                return current
            neighbor = get_best_neighbor(current)
            neighbor_conflicts = calculate_conflicts(neighbor)
            if neighbor_conflicts >= conflicts:
                # Stuck at local maximum
                current = random_state(n)
            else:
                current = neighbor

    def random_state(n):
        return [random.randint(0, n - 1) for _ in range(n)]

    def calculate_conflicts(state):
        conflicts = 0
        n = len(state)
        for i in range(n):
            for j in range(i + 1, n):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_best_neighbor(state):
        n = len(state)
        min_conflicts = float('inf')
        best_state = state[:]
        for row in range(n):
            original_col = state[row]
            for col in range(n):
                if col != original_col:
                    state[row] = col
                    conflicts = calculate_conflicts(state)
                    if conflicts < min_conflicts:
                        min_conflicts = conflicts
                        best_state = state[:]
            state[row] = original_col
        return best_state


def astar_8queens():
    def a_star_n_queens(n):
        heap = []
        heapq.heappush(heap, (0, []))
        solutions = []

        while heap:
            f, state = heapq.heappop(heap)
            row = len(state)
            if row == n:
                solutions.append(state)
                continue

            for col in range(n):
                if is_safe(state, row, col):
                    new_state = state + [col]
                    g = len(new_state)
                    h = heuristic(new_state, n)
                    heapq.heappush(heap, (g + h, new_state))
        return solutions

    def heuristic(state, n):
        # Number of conflicts
        conflicts = 0
        row = len(state) - 1
        col = state[-1]
        for r in range(row):
            c = state[r]
            if c == col or abs(c - col) == abs(r - row):
                conflicts += 1
        return conflicts