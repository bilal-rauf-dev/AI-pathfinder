import tkinter as tk
import time
import heapq
import random
from collections import deque

# --- IMPORT ALGORITHMS ---
try:
    from algorithms import bfs, dfs, ucs, dls_iterative, iddfs, bidirectional_search
except ImportError:
    print("Error: Could not import algorithms. Make sure 'algorithms.py' exists.")

# --- CONFIGURATION ---
ROWS, COLS = 20, 20
CELL_SIZE = 30
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# --- COLORS ---
COLOR_EMPTY = "white"
COLOR_WALL = "black"
COLOR_START = "green"
COLOR_TARGET = "blue"
COLOR_FRONTIER = "yellow"
COLOR_EXPLORED = "red"
COLOR_PATH = "purple"

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = "EMPTY"  # States: EMPTY, WALL, START, TARGET, FRONTIER, EXPLORED, PATH
        self.parent = None
        self.cost = float('inf')

    def get_pos(self):
        return self.row, self.col

    def get_neighbors(self, grid):
        """
        Returns neighbors in strict clockwise order.
        Takes ONLY 'grid' as argument (rows/cols derived from grid len).
        """
        neighbors = []
        directions = [
            (-1, 0), (-1, 1), (0, 1), (1, 1), 
            (1, 0), (1, -1), (0, -1), (-1, -1)
        ]

        for dr, dc in directions:
            new_r, new_c = self.row + dr, self.col + dc
            if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]):
                neighbor = grid[new_r][new_c]
                if neighbor.state != "WALL":
                    neighbors.append(neighbor)
        return neighbors

class PathfinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GOOD PERFORMANCE TIME APP")
        
        # 1. Setup Canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        # 2. Initialize Grid
        self.grid = [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]
        
        # 3. Setup Start and Target
        self.start_node = self.grid[0][0]
        self.start_node.state = "START"
        self.target_node = self.grid[ROWS-1][COLS-1]
        self.target_node.state = "TARGET"
        
        # 4. Draw initial grid
        self.draw_grid()
        
        # 5. Bind Inputs
        self.canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("<Key>", self.handle_keypress)
        self.root.focus_set()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                node = self.grid[r][c]
                color = COLOR_EMPTY
                if node.state == "WALL": color = COLOR_WALL
                elif node.state == "START": color = COLOR_START
                elif node.state == "TARGET": color = COLOR_TARGET
                elif node.state == "FRONTIER": color = COLOR_FRONTIER
                elif node.state == "EXPLORED": color = COLOR_EXPLORED
                elif node.state == "PATH": color = COLOR_PATH
                
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def update_gui(self):
        self.draw_grid()
        self.root.update()
        # time.sleep(0.02) 

    def reset_grid(self):
        for r in range(ROWS):
            for c in range(COLS):
                node = self.grid[r][c]
                if node.state in ["FRONTIER", "EXPLORED", "PATH"]:
                    node.state = "EMPTY"
                    node.parent = None
                    node.cost = float('inf')
        self.draw_grid()

    def handle_click(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            node = self.grid[row][col]
            if node.state == "EMPTY":
                node.state = "WALL"
            elif node.state == "WALL":
                node.state = "EMPTY"
            self.draw_grid()

    def handle_keypress(self, event):
        print(f"Key pressed: {event.char}")
        
        if event.char in "123456r":
            self.reset_grid()

        if event.char == '1':
            bfs(self.update_gui, self.grid, self.start_node, self.target_node)
        elif event.char == '2':
            dfs(self.update_gui, self.grid, self.start_node, self.target_node)
        elif event.char == '3':
            ucs(self.update_gui, self.grid, self.start_node, self.target_node)
        elif event.char == '4':
            dls_iterative(self.update_gui, self.grid, self.start_node, self.target_node, limit=20)
        elif event.char == '5':
            iddfs(self.update_gui, self.grid, self.start_node, self.target_node)
        elif event.char == '6':
            bidirectional_search(self.update_gui, self.grid, self.start_node, self.target_node)
        elif event.char == 'r':
            self.reset_grid()
        elif event.char == 'd':
            self.run_dynamic_movement()

    def reset_keep_walls(self):
        for r in range(ROWS):
            for c in range(COLS):
                node = self.grid[r][c]
                if node.state in ["FRONTIER", "EXPLORED", "PATH"]:
                    node.state = "EMPTY"
                    node.parent = None
                    node.cost = float('inf')
        self.start_node.state = "START"
        self.target_node.state = "TARGET"
        self.draw_grid()

    def run_dynamic_movement(self):
        """
        Moves the agent along the path. 
        If blocked, it re-plans and continues WITHOUT recursion.
        """
        # We loop until we reach the target or get stuck
        while self.start_node != self.target_node:
            
            # 1. Reconstruct current path from Target -> Start
            path = []
            curr = self.target_node
            
            # Safety check: If no path exists, stop
            if not curr.parent and curr != self.start_node:
                print("❌ No path to target!")
                return

            while curr:
                path.append(curr)
                curr = curr.parent
            path.reverse() # Now it is Start -> Target

            # If path is just [Start], we are stuck or done
            if len(path) <= 1:
                break

            print(f"Path found. Length: {len(path)}")

            # 2. Move along the path
            # We iterate through the path, but if we break (due to wall), 
            # the outer 'while' loop triggers a re-plan.
            path_blocked = False
            
            for i in range(len(path) - 1): # -1 because we look ahead
                current_node = path[i]
                next_node = path[i+1]

                # --- Random Obstacle Event ---
                if random.random() < 0.3:  
                    rx, ry = random.randint(0, ROWS-1), random.randint(0, COLS-1)
                    random_node = self.grid[rx][ry]
                    valid_states = ["EMPTY", "EXPLORED", "FRONTIER", "PATH"]
                    
                    if random_node.state in valid_states and random_node != self.start_node and random_node != self.target_node:
                        random_node.state = "WALL"
                        self.draw_grid()
                        self.root.update()

                # --- Check if Next Step is Blocked ---
                if next_node.state == "WALL":
                    print("⚠️ PATH BLOCKED! Re-planning...")
                    
                    # Update Start Node to current position
                    self.start_node = current_node 
                    self.start_node.state = "START"

                    # Clear invalid path visuals
                    self.reset_keep_walls()

                    # Re-run Search
                    from algorithms import bfs
                    found = bfs(self.update_gui, self.grid, self.start_node, self.target_node)
                    
                    if found:
                        print("✅ New path found! Resuming...")
                        path_blocked = True
                        break # Break the for-loop, let outer while-loop handle new path
                    else:
                        print("❌ Stuck! No path possible.")
                        return

                # --- Move Agent ---
                if current_node != self.target_node:
                    current_node.state = "EXPLORED" # Mark trail
                
                # Update Start Node pointer as we move
                self.start_node = next_node 
                self.start_node.state = "START"
                
                self.draw_grid()
                self.root.update()
                time.sleep(0.1)
                
                # If we reached target, exit everything
                if self.start_node == self.target_node:
                    print("🏆 Target Reached!")
                    return

            # If we finished the path without blocking, we are done
            if not path_blocked:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfinderApp(root)
    root.mainloop()