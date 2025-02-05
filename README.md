# Pacman AI Projects

This repository contains three projects implementing various AI algorithms to control Pacman agents in different scenarios. Each project focuses on specific AI techniques, from pathfinding to adversarial search and probabilistic reasoning.

## Projects Overview

### Project 0: BFS and A* Pathfinding (19/20)
Implements basic pathfinding algorithms to navigate Pacman through mazes:
- Breadth-First Search (BFS) for shortest path finding
- A* algorithm with heuristics for optimal pathfinding

### Project 1: Adversarial Search (17.5/20)
Implements adversarial search algorithms for ghost avoidance:
- Minimax algorithm for basic strategy
- H-Minimax with heuristics for improved efficiency

### Project 2: Bayes Filter (15/20)
Implements probabilistic reasoning to locate and capture ghosts:
- Bayes filter algorithm for ghost position inference
- Handles multiple ghost behaviors (afraid, fearless, terrified)

## Project Structure

```
├── Project0/
│   ├── bfs.py
│   ├── dfs.py
│   ├── astar.py
│   ├── humanagent.py
|   ├── pacmanagent.py
|   ├── run.py
│   └── README.md
├── Project1/
│   ├── minimax.py
│   ├── hminimax.py
│   ├── humanagent.py
|   ├── pacmanagent.py
|   ├── run.py
│   └── README.md
├── Project2/
│   ├── bayesfilter.py
│   ├── run.py
│   └── README.md
└── README.md
```

## Implementation Details

Each project implements specific algorithms:

- **Project 0**: Path optimization using graph search algorithms
- **Project 1**: Strategic decision-making in adversarial environments
- **Project 2**: Probabilistic reasoning with noisy sensor inputs

## Evaluation Results

| Project | Grade | Main Components |
|---------|--------|-----------------|
| BFS & A* | 19/20 | BFS (20%), A* (75%), Code Style (5%) |
| Adversarial | 17.5/20 | Minimax (45%), H-Minimax (50%), Code Style (5%) |
| Bayes Filter | 15/20 | Transition Matrix (25%), Observation Matrix (25%), Update Function (25%), Pacman Controller (20%), Code Style (5%) |

## Requirements

- Python 3.x

## License

This project was developed as part of a university course. Please check with the authors for usage permissions.

## Course Reference
These projects were completed as part of the [Introduction to Artificial Intelligence (INFO8006)](https://github.com/glouppe/info8006-introduction-to-ai) course.

## Authors

- [Mehdi Boustani](https://github.com/MehdiBoustani)
- [Antoine Kinable](https://github.com/AntoineKin)
- [Abdelkader Albashityalshaier](https://github.com/AbdelkaderULG)
