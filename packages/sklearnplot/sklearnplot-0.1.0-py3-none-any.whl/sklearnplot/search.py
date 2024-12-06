import time

def bfs(graph,start,goal):
    start_time  = time.time()
    result = []
    paths = []
    visited = set()
    queue = [(start,[start])]
    total_paths = 0

    while queue:
        current_node, path = queue.pop(0)
        if current_node == goal:
            paths.append(path)
            total_paths +=1 
        if current_node not in visited:
            result.append(current_node)
            visited.add(current_node)
            for neighbour in graph[current_node]:
                if neighbour[0] not in visited:
                    queue.append((neighbour[0], path+[neighbour[0]]))

    end_time = time.time()

    time_elapsed = end_time - start_time
    return result, total_paths , time_elapsed, paths

def dfs(graph,start,goal):
    start_time = time.time()
    result = []
    paths = []
    visited = set()
    stack = [(start,[start])]
    total_paths = 0
    while stack:
        current_node, path = stack.pop()
        if current_node == goal:
                paths.append(path)
                total_paths += 1
        if current_node not in visited:
            result.append(current_node)
            visited.add(current_node)
            for neighbour in reversed(list(graph[current_node])):
                if neighbour[0] not in visited:
                    stack.append((neighbour[0], path+[neighbour[0]]))


    end_time = time.time()
    time_elapsed = end_time - start_time
    return result, total_paths , time_elapsed, paths

def ucs(graph,start,goal):
    start_time = time.time()
    visited = set()
    queue = [(start,[start])]
    paths = []
    weights = [0]
    cost = float('inf')
    total_paths = 0

    while queue:
        current_node,path = queue.pop(weights.index(min(weights)))
        current_weight = weights.pop(weights.index(min(weights)))
        # print(current_node,current_weight)
        if current_node == goal:
            paths.append(path)
            cost = min(cost,current_weight)
            total_paths += 1
        else:
            visited.add(current_node)
            # print("neighbousr",graph[current_node])
            for neighbour in graph[current_node]:
                if neighbour[0] not in visited:
                    queue.append((neighbour[0], path+[neighbour[0]]))
                    weights.append(neighbour[1] + current_weight)

    end_time = time.time()
    time_elapsed = end_time - start_time
    return cost,total_paths , time_elapsed, paths

def bidirectional_bfs(graph, start, goal):
    start_time = time.time()
    if start == goal:
        end_time = time.time()

        time_elapsed = end_time - start_time
        print(f"Time Elapsed: {time_elapsed}")
        return [start]

    queue_forward = [start]
    queue_backward = [goal]


    visited_forward = {start}
    visited_backward = {goal}


    parent_forward = {start: None}
    parent_backward = {goal: None}


    while queue_forward and queue_backward:
    # Forward BFS step
        if queue_forward:
            current_forward = queue_forward.pop(0)
            for neighbor in graph[current_forward]:
                neighbor = neighbor[0]
                if neighbor not in visited_forward:
                    visited_forward.add(neighbor)
                    parent_forward[neighbor] = current_forward
                    queue_forward.append(neighbor)
                if neighbor in visited_backward:
                    end_time = time.time()
                    time_elapsed = end_time - start_time
                    # print(f"Time Elapsed: {time_elapsed}")
                    return construct_path(parent_forward, parent_backward, neighbor), time_elapsed

    # Backward BFS step
        if queue_backward:
            current_backward = queue_backward.pop(0)
            for neighbor in graph[current_backward]:
                neighbor = neighbor[0]
                if neighbor not in visited_backward:
                    visited_backward.add(neighbor)
                    parent_backward[neighbor] = current_backward
                    queue_backward.append(neighbor)
                if neighbor in visited_forward: # Meeting point
                    end_time = time.time()
                    time_elapsed = end_time - start_time
                    # print(f"Time Elapsed: {time_elapsed}")s
                    return construct_path(parent_forward, parent_backward, neighbor), time_elapsed
                
    end_time = time.time()
    time_elapsed = end_time - start_time
    # print(f"Time Elapsed: {time_elapsed}")

    return None , time_elapsed

def construct_path(parent_forward, parent_backward, meet_node):
    path_forward = []
    meet_node_temp = meet_node
    while meet_node_temp is not None:
        path_forward.append(meet_node_temp)  
        meet_node_temp = parent_forward[meet_node_temp]
        path_forward.reverse()

    path_backward = []
    meet_node = parent_backward[meet_node]
    while meet_node is not None:
        path_backward.append(meet_node)
        meet_node = parent_backward[meet_node]

    return path_forward + path_backward

def depth_limited_search(graph,start,goal,limit):
    start_time = time.time()
    result = []
    paths = []
    visited = set()
    stack = [(start,[start],0)]
    total_paths = 0
    while stack:
        current_node, path, current_depth = stack.pop()
        if current_node == goal:
            paths.append(path)
            total_paths += 1
        if current_node not in visited:
            result.append(current_node)
            visited.add(current_node)
            if current_depth < limit:
                for neighbour in reversed(list(graph[current_node])):
                    if neighbour[0] not in visited:
                        stack.append((neighbour[0],path+[neighbour[0]],current_depth+1))

    end_time = time.time()
    time_elapsed = end_time - start_time

    return result, total_paths, time_elapsed, paths

