# Pathfinding Visualizer

A visualizer built in Python using Pygame to demonstrate various graph search algorithms. You can draw walls, place start and end nodes, and watch these search algorithms explore the grid in real-time.

## Features
- **Breadth-First Search (BFS)** (Unweighted): Explores equally in all directions, guaranteeing the shortest path.
- **Depth-First Search (DFS)** (Unweighted): Shoots down a single path until it hits a dead end. Does not guarantee the shortest path.
- **Dijkstra's Algorithm** (Weighted/Unicost): Finds the shortest path efficiently, building off node costs point-to-point.
- **A* Search** (Weighted): Uses the Manhattan distance heuristic to guide it straight towards the target node point, generally executing faster than Dijkstra.
- **Greedy Best-First Search** (Weighted): Uses the Euclidean (direct straight line) distance as a heuristic. Extremely fast but does not guarantee the absolute shortest path depending on obstacles.

## Installation

This application requires Python and the `pygame` library. From your terminal, type:

```bash
# If using pip
pip install pygame

# Optional/Alternative (depending on setup)
python -m pip install pygame
```

## Running the Application

Simply navigate to the folder with `main.py` and execute the program via terminal:

```bash
python main.py
```

## Controls

- **Left Click**: Draw Start Node (Green). Second click draws End Node (Red). Further clicks draw Walls (Black).
- **Hold Left Click & Drag**: Easily populate large amounts of walls.
- **Right Click / Drag**: Erase nodes turning them back into plain open tiles.
- **Algo Button (Bottom Left)**: Click to toggle between algorithms (`BFS`, `DFS`, `Dijkstra`, `A*`, `Greedy`)
- **Start Search (Bottom Middle)**: Tell the algorithm to execute and discover the path!
- **Reset (Bottom Right)**: Wipe the entire grid and start from a blank canvas.