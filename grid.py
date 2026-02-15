class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = "EMPTY"  # States: EMPTY, WALL, START, TARGET, FRONTIER, EXPLORED, PATH
        self.parent = None    # To reconstruct the path later
        self.cost = float('inf') # For UCS

    def get_pos(self):
        return self.row, self.col

    def get_neighbors(self, grid, rows, cols):
        """
        Returns neighbors in the strict clockwise order:
        Up, Top-Right, Right, Bottom-Right, Bottom, Bottom-Left, Left, Top-Left.
        """
        neighbors = []
        # Directions: (Row Change, Col Change)
        # 1. Up (-1, 0)
        # 2. Top-Right (-1, 1)
        # 3. Right (0, 1)
        # 4. Bottom-Right (1, 1)
        # 5. Bottom (1, 0)
        # 6. Bottom-Left (1, -1)
        # 7. Left (0, -1)
        # 8. Top-Left (-1, -1)
        
        directions = [
            (-1, 0), (-1, 1), (0, 1), (1, 1), 
            (1, 0), (1, -1), (0, -1), (-1, -1)
        ]

        for dr, dc in directions:
            new_r, new_c = self.row + dr, self.col + dc

            # Check bounds and if it's not a wall
            if 0 <= new_r < rows and 0 <= new_c < cols:
                neighbor = grid[new_r][new_c]
                if neighbor.state != "WALL":
                    neighbors.append(neighbor)
        
        return neighbors