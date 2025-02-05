# Pacman Adversarial Agent

## Description

This project implements adversarial search algorithms to maximize Pacman's score while avoiding a ghost in a grid-based environment. The implemented algorithms are:

- **Minimax Algorithm**: A standard adversarial search algorithm where Pacman and the ghost are the two players.
- **H-Minimax Algorithm**: An optimized version of Minimax that considers heuristics to improve efficiency.

## Files

- `minimax.py`: Contains the implementation of the Minimax algorithm, based on the `pacmanagent.py` template.
- `hminimax.py`: Contains the implementation of the H-Minimax algorithm, based on the `pacmanagent.py` template.

## Usage

To run the Minimax agent against the `dumby` ghost on the small layout, use the following command:

```console
$ python run.py --agent minimax --ghost dumby --layout small_adv
```

Different ghost strategies are available:

- `dumby`: Rotates counterclockwise until it can move left.
- `greedy`: Moves towards Pacman’s closest position.
- `smarty`: Chooses the shortest path towards Pacman.

You can change the game's random seed using:

```console
$ python run.py --agent minimax --ghost smarty --layout medium_adv --seed 42
```

## Implementation Details

- The agent only uses the provided API to retrieve game information.
- Capsules are not considered in this implementation.
- The Minimax agent does not need to handle `medium_adv` and `large_adv` layouts.

## Testing & Evaluation

The performance of the agent is evaluated based on:

- **Minimax Performance**: Measures optimality on different layouts.
- **H-Minimax Efficiency**: Evaluates score and number of expanded nodes.
- **Code Quality**: Ensures PEP-8 compliance.

To improve robustness, additional tests can be performed on custom layouts to handle edge cases.

## Grade

This project was graded **17.5/20**.
