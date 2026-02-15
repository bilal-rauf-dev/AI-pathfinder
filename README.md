# AI Pathfinder: Uninformed Search Visualization

## Project Overview
This project is a Python-based **AI Pathfinder** designed to visualize how different "blind" (uninformed) search algorithms explore a grid environment.

Unlike standard static maze solvers, this application introduces a **Dynamic Environment**. The agent must navigate from a **Start Point (S)** to a **Target Point (T)** while avoiding static walls and **Dynamic Obstacles** that randomly spawn during runtime. If a path becomes blocked, the agent detects the change and triggers a **re-planning** sequence to calculate a new route.

## Features
* **6 Search Algorithms:** Implementation of fundamental uninformed search strategies.
* **Real-Time Visualization:** GUI that visually distinguishes between **Frontier Nodes** (queue/stack), **Explored Nodes** (visited), and the **Final Path**.
* **Dynamic Obstacles:** Random walls appear with a small probability during the search, forcing the agent to adapt.
* **Strict Movement Order:** Node expansion follows a specific clockwise & diagonal pattern (Up, Top-Right, Right, etc.).
* **Performance Metrics:** Visualizes the "flood" of the algorithm step-by-step.

## Algorithms Implemented
The following algorithms are implemented to navigate the grid:
1.  **Breadth-First Search (BFS)**
2.  **Depth-First Search (DFS)**
3.  **Uniform-Cost Search (UCS)**
4.  **Depth-Limited Search (DLS)**
5.  **Iterative Deepening DFS (IDDFS)**
6.  **Bidirectional Search**

## Installation & Dependencies
This project uses **Python** and requires a GUI library (e.g., Pygame, Matplotlib, or Tkinter).

### Prerequisites
* Python 3.x
* [Your Library Name, e.g., Pygame]

### Setup
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YourUsername]/AI_A1_22F_XXXX.git
    cd AI_A1_22F_XXXX
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    # OR manually
    pip install pygame
    ```

## How to Run
To launch the **"GOOD PERFORMANCE TIME APP"** and start the visualization:

```bash
python main.py
