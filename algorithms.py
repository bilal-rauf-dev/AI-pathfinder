import time
from collections import deque

def reconstruct_path(current_node, draw_func):
    """Backtracks from Target to Start to draw the final path."""
    path = []
    while current_node.parent is not None:
        path.append(current_node)
        current_node.state = "PATH"
        current_node = current_node.parent
        draw_func() # Update GUI to show path forming
    return path

def bfs(draw_func, grid, start, end):
    """Breadth-First Search"""
    count = 0
    queue = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == end:
            reconstruct_path(end, draw_func)
            return True

        # strict movement order neighbors
        for neighbor in current.get_neighbors(grid, len(grid), len(grid[0])):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                neighbor.state = "FRONTIER"
                queue.append(neighbor)
        
        # Mark current as explored (after checking neighbors)
        if current != start:
            current.state = "EXPLORED"

        draw_func() # Animation step
        # time.sleep(0.02) # Uncomment to slow down

    return False # Path not found

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

            # Get neighbors
            neighbors = current.get_neighbors(grid, len(grid), len(grid[0]))
            
            # IMPORTANT: For DFS (Stack), we must reverse the neighbors list 
            # so that when we pop, we process them in the correct Clockwise order.
            # (Last In, First Out)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    neighbor.parent = current
                    neighbor.state = "FRONTIER"
                    stack.append(neighbor)
    
    return False