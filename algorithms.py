import time
from collections import deque
import heapq

def reconstruct_path(current_node, draw_func):
    """Backtracks from Target to Start to draw the final path."""
    path = []
    while current_node.parent is not None:
        path.append(current_node)
        current_node.state = "PATH"
        current_node = current_node.parent
        draw_func()
    return path

def bfs(draw_func, grid, start, end):
    """Breadth-First Search"""
    queue = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == end:
            reconstruct_path(end, draw_func)
            return True

        for neighbor in current.get_neighbors(grid):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                neighbor.state = "FRONTIER"
                queue.append(neighbor)
        
        if current != start:
            current.state = "EXPLORED"

        draw_func()
    return False

def dfs(draw_func, grid, start, end):
    """Depth-First Search"""
    stack = [start]
    visited = set()

    while stack:
        current = stack.pop()

        if current == end:
            reconstruct_path(end, draw_func)
            return True

        if current not in visited:
            visited.add(current)
            if current != start:
                current.state = "EXPLORED"
            
            draw_func() 

            neighbors = current.get_neighbors(grid)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    neighbor.parent = current
                    neighbor.state = "FRONTIER"
                    stack.append(neighbor)
    return False

def ucs(draw_func, grid, start, end):
    """Uniform Cost Search"""
    count = 0
    pq = [(0, count, start)]
    cost_so_far = {start: 0}
    start.parent = None

    while pq:
        current_cost, _, current = heapq.heappop(pq)

        if current == end:
            reconstruct_path(end, draw_func)
            return True

        current.state = "EXPLORED"
        if current == start: current.state = "START"
        if current == end: current.state = "TARGET"
        draw_func()

        for neighbor in current.get_neighbors(grid):
            is_diagonal = (neighbor.row != current.row) and (neighbor.col != current.col)
            move_cost = 1.4 if is_diagonal else 1.0
            new_cost = current_cost + move_cost

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                neighbor.parent = current
                neighbor.state = "FRONTIER"
                count += 1
                heapq.heappush(pq, (new_cost, count, neighbor))     
    return False

def dls_iterative(draw_func, grid, start, end, limit):
    """Helper for IDDFS: DFS with a depth limit."""
    stack = [(start, 0)]
    
    # Reset parents for fresh run
    for row in grid:
        for node in row:
            if node.state not in ["WALL", "START", "TARGET"]:
                node.state = "EMPTY"
            node.parent = None

    while stack:
        current, depth = stack.pop()

        if current == end:
            reconstruct_path(end, draw_func)
            return True
        
        if depth >= limit:
            continue

        current.state = "EXPLORED"
        if current == start: current.state = "START"
        if current == end: current.state = "TARGET"
        draw_func()

        neighbors = current.get_neighbors(grid)
        for neighbor in reversed(neighbors):
            if neighbor != current.parent: 
                neighbor.parent = current
                neighbor.state = "FRONTIER"
                stack.append((neighbor, depth + 1))
    return False

def iddfs(draw_func, grid, start, end):
    """Iterative Deepening DFS"""
    max_depth = len(grid) * len(grid[0])
    for limit in range(1, max_depth):
        if dls_iterative(draw_func, grid, start, end, limit):
            return True
    return False

def bidirectional_search(draw_func, grid, start, end):
    """Bidirectional Search"""
    q_start = deque([start])
    q_end = deque([end])
    
    visited_start = {start: None}
    visited_end = {end: None}

    start.state = "FRONTIER"
    end.state = "FRONTIER"

    while q_start and q_end:
        # --- Expand from Start ---
        if q_start:
            curr_s = q_start.popleft()
            if curr_s in visited_end:
                connect_paths(curr_s, visited_start, visited_end, draw_func)
                return True
            for neighbor in curr_s.get_neighbors(grid):
                if neighbor not in visited_start:
                    visited_start[neighbor] = curr_s
                    neighbor.state = "FRONTIER"
                    q_start.append(neighbor)
            curr_s.state = "EXPLORED"
            draw_func()

        # --- Expand from End ---
        if q_end:
            curr_e = q_end.popleft()
            if curr_e in visited_start:
                connect_paths(curr_e, visited_start, visited_end, draw_func)
                return True
            for neighbor in curr_e.get_neighbors(grid):
                if neighbor not in visited_end:
                    visited_end[neighbor] = curr_e
                    neighbor.state = "FRONTIER"
                    q_end.append(neighbor)
            curr_e.state = "EXPLORED"
            draw_func()

    return False

def connect_paths(meeting_node, visited_start, visited_end, draw_func):
    """Helper to draw the path when two frontiers meet."""
    # 1. Trace back from meeting point to Start
    curr = meeting_node
    while curr:
        curr.state = "PATH"
        draw_func()
        curr = visited_start[curr]
    
    # 2. Trace back from meeting point to End
    curr = meeting_node
    while curr:
        curr.state = "PATH"
        draw_func()
        curr = visited_end[curr]