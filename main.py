import tkinter as tk
import time
import random

# Configuration
ROWS, COLS = 20, 20
CELL_SIZE = 30
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Colors
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
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.state == "WALL"

class PathfinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GOOD PERFORMANCE TIME APP") # Requirement 
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        # Initialize Grid
        self.grid = [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]
        self.start_node = self.grid[0][0]
        self.start_node.state = "START"
        self.target_node = self.grid[ROWS-1][COLS-1]
        self.target_node.state = "TARGET"
        
        # Draw initial grid
        self.draw_grid()
        
        # Bind Mouse Click to toggle walls
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_grid(self):
        """Redraws the entire grid based on node states."""
        self.canvas.delete("all") # Clear canvas
        for r in range(ROWS):
            for c in range(COLS):
                node = self.grid[r][c]
                color = COLOR_EMPTY
                
                # Map state to color
                if node.state == "WALL": color = COLOR_WALL
                elif node.state == "START": color = COLOR_START
                elif node.state == "TARGET": color = COLOR_TARGET
                elif node.state == "FRONTIER": color = COLOR_FRONTIER
                elif node.state == "EXPLORED": color = COLOR_EXPLORED
                elif node.state == "PATH": color = COLOR_PATH
                
                # Draw Rectangle
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def handle_click(self, event):
        """Allows user to click to add walls manually for testing."""
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            node = self.grid[row][col]
            if node.state == "EMPTY":
                node.state = "WALL"
            elif node.state == "WALL":
                node.state = "EMPTY"
            self.draw_grid()

    def update_gui(self):
        """Call this function inside your search loops to animate."""
        self.draw_grid()
        self.root.update()  # Forces Tkinter to redraw immediately
        # time.sleep(0.05)  # Uncomment to slow down the search for visualization

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PathfinderApp(root)
    root.mainloop()