import tkinter as tk
import time
import heapq
from collections import deque

# --- IMPORT ALGORITHMS ---
# Make sure algorithms.py is in the same folder!
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
        Returns neighbors in strict clockwise order:
        Up, Top-Right, Right, Bottom-Right, Bottom, Bottom-Left, Left, Top-Left.
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

        # 2. Initialize Grid (CRITICAL STEP - DO NOT REMOVE)
        self.grid = [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]
        
        # 3. Setup Start and Target
        self.start_node = self.grid[0][0]
        self.start_node.state = "START"
        self.target_node = self.grid[ROWS-1][COLS-1]
        self.target_node.state = "TARGET"
        
        # 4. Draw initial grid
        self.draw_grid()
        
        # 5. Bind Inputs
        self.canvas.bind("<Button-1>", self.handle_click) # Mouse click
        self.root.bind("<Key>", self.handle_keypress)     # Keyboard press
        self.root.focus_set()

    def draw_grid(self):
        """Redraws the entire grid."""
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
        """Called by algorithms to animate."""
        self.draw_grid()
        self.root.update()
        # time.sleep(0.02) # Uncomment to slow down animation

    def reset_grid(self):
        """Clears search results but keeps walls."""
        for r in range(ROWS):
            for c in range(COLS):
                node = self.grid[r][c]
                if node.state in ["FRONTIER", "EXPLORED", "PATH"]:
                    node.state = "EMPTY"
                    node.parent = None
                    node.cost = float('inf')
        self.draw_grid()

    def handle_click(self, event):
        """Toggle walls with mouse."""
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
        """Run algorithms on key press."""
        print(f"Key pressed: {event.char}") # Debugging
        
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

# --- ENTRY POINT ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PathfinderApp(root)
    root.mainloop()