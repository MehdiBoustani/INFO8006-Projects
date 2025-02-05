# BFS and A* Algorithms

## Description
This project implements a Pacman agent using Breadth-First Search (BFS) and A* search algorithms to navigate through a maze, maximize the score, and collect food and capsules. The task involves implementing both algorithms based on the provided pacmanagent.py template.

## Files
- `bfs.py`: Implements the BFS algorithm for finding the shortest path in a maze
- `astar.py`: Implements the A* algorithm for finding the optimal path with heuristics

## Usage
Test the BFS implementation:
```bash
python run.py --agent bfs --layout medium
```

Test the A* implementation:
```bash
python run.py --agent astar --layout medium
```

## Implementation Details
- **BFS**: Explores all possible paths level by level, ensuring the shortest path is found
- **A***: Uses a heuristic to find the optimal path, reducing the number of expanded nodes compared to BFS

## Evaluation Criteria
The project was evaluated based on the following components:

- **BFS (20%)**: Correct implementation should return the same score and expand roughly the same number of nodes as the reference implementation
- **A\* (75%)**: The algorithm should return the optimal solution with the lowest number of expanded nodes. The quality of the heuristic is a key factor in scoring
- **Code Style (5%)**: The code should be PEP-8 compliant for readability and maintainability

## Grade
This project received a grade of **19/20**

## Authors
- [Mehdi Boustani](https://github.com/MehdiBoustani)
- [Antoine Kinable](https://github.com/AntoineKin)
