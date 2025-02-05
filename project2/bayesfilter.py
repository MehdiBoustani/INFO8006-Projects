import math
from collections import deque

import numpy as np

from pacman_module.game import Agent, Directions, manhattanDistance
from pacman_module.util import Queue


class BeliefStateAgent(Agent):
    """Belief state agent.

    Arguments:
        ghost: The type of ghost (as a string).
    """

    def __init__(self, ghost):
        super().__init__()

        self.ghost = ghost

    def transition_matrix(self, walls, position):
        """Builds the transition matrix

            T_t = P(X_t | X_{t-1})

        given the current Pacman position.

        Arguments:
            walls: The W x H grid of walls.
            position: The current position of Pacman.

        Returns:
            The W x H x W x H transition matrix T_t. The element (i, j, k, l)
            of T_t is the probability P(X_t = (k, l) | X_{t-1} = (i, j)) for
            the ghost to move from (i, j) to (k, l).
        """
        W = walls.width
        H = walls.height

        fear = {
            'afraid': 1.0,
            'fearless': 0.0,
            'terrified': 3.0,
        }.get(self.ghost, 0.0)

        # 4D transition matrix
        T = np.zeros((W, H, W, H), dtype=np.float64)

        # Iterate over all possible positions
        for i in range(W):
            for j in range(H):
                if walls[i][j]:
                    continue

                # Store probabilities for moving from (i, j) to other positions
                transitions = []

                for k in range(W):
                    for l in range(H):

                        # Validity check before computing the probability
                        if walls[k][l] or \
                                manhattanDistance((i, j), (k, l)) > 1:
                            continue

                        # Compute the transition probability
                        prev_dist = manhattanDistance((i, j), position)
                        next_dist = manhattanDistance((k, l), position)
                        prob = 2**fear if next_dist >= prev_dist else 1
                        transitions.append(((k, l), prob))

                # Normalize probabilities
                total_prob = sum(prob for _, prob in transitions)
                for (k, l), prob in transitions:
                    T[i, j, k, l] = prob / total_prob if \
                        total_prob > 0 else 0.0

        return T

    def observation_matrix(self, walls, evidence, position):
        """Builds the observation matrix

            O_t = P(e_t | X_t)

        given a noisy ghost distance evidence e_t and the current Pacman
        position.

        Arguments:
            walls: The W x H grid of walls.
            evidence: A noisy ghost distance evidence e_t.
            position: The current position of Pacman.

        Returns:
            The W x H observation matrix O_t.
        """
        W = walls.width
        H = walls.height

        def compute_prob(i, j):
            """Computes the actual  P(E_t=e_t | X_t=x_t)"""
            z = evidence + 2 - manhattanDistance((i, j), position)

            # check invalid range
            if not (z == int(z)) or not 0 <= z <= 4:
                return 0

            # P(E_t=e_t | X_t=x_t) = P(Z = e_t+n*p - ||Pacman-x_t||_1)
            # with P(Z=z) = (n choose z) p^z*(1-p)^(n-z) = (4 choose z)/16
            return math.comb(4, z) / 16

        return np.array(
            [[compute_prob(i, j) for j in range(H)] for i in range(W)]
        )

    def update(self, walls, belief, evidence, position):
        """Updates the previous ghost belief state

            b_{t-1} = P(X_{t-1} | e_{1:t-1})

        given a noisy ghost distance evidence e_t and the current Pacman
        position.

        Arguments:
            walls: The W x H grid of walls.
            belief: The belief state for the previous ghost position b_{t-1}.
            evidence: A noisy ghost distance evidence e_t.
            position: The current position of Pacman.

        Returns:
            The updated ghost belief state b_t as a W x H matrix.
        """
        W = walls.width
        H = walls.height

        T = self.transition_matrix(walls, position)
        O = self.observation_matrix(walls, evidence, position)

        # converts WxH matrix to WH vector back and forth
        belief = (
            np.diag(O.reshape(W*H)) @
            T.reshape(W*H, W*H).T @
            belief.reshape(W*H)
        ).reshape(W, H)
        belief /= np.sum(belief)

        return belief

    def get_action(self, state):
        """Updates the previous belief states given the current state.

        ! DO NOT MODIFY !

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            The list of updated belief states.
        """

        walls = state.getWalls()
        beliefs = state.getGhostBeliefStates()
        eaten = state.getGhostEaten()
        evidences = state.getGhostNoisyDistances()
        position = state.getPacmanPosition()

        new_beliefs = [None] * len(beliefs)

        for i in range(len(beliefs)):
            if eaten[i]:
                new_beliefs[i] = np.zeros_like(beliefs[i])
            else:
                new_beliefs[i] = self.update(
                    walls,
                    beliefs[i],
                    evidences[i],
                    position,
                )

        return new_beliefs


class PacmanAgent(Agent):
    """Pacman agent that tries to eat ghosts given belief states."""

    def __init__(self):
        super().__init__()

        # current todo moves
        self.moves = None

    def get_best_path(self, walls, beliefs, eaten, position):
        """
        Breadth first search algorithm to compute path to chase ghost

        Arguments:
            walls: The W x H grid of walls.
            beliefs: The list of current ghost belief states.
            eaten: A list of booleans indicating which ghosts have been eaten.
            position: The current position of Pacman.

        Returns:
            An optimal path.
        """
        W = walls.width
        H = walls.height

        # Find positions with highest probability for each ghost
        ghost_positions = []
        for h, belief in enumerate(beliefs):
            if not eaten[h]:
                # Here, we use unravel_index to get the position of the max
                # More efficient, because we avoid nester loops
                best_pos_index = np.unravel_index(
                    belief.argmax(),
                    belief.shape
                )
                if not walls[best_pos_index[0]][best_pos_index[1]]:
                    ghost_positions.append(best_pos_index)

        def get_next_pos(pos):
            """
            Gives all next valid positions and related actions
            """
            x = pos[0]
            y = pos[1]

            possible_moves = [
                (Directions.STOP, (x, y)),
                (Directions.NORTH, (x, y+1)),
                (Directions.EAST, (x+1, y)),
                (Directions.SOUTH, (x, y-1)),
                (Directions.WEST, (x-1, y))
            ]
            return {
                action: pos
                for action, pos in possible_moves
                if 0 <= pos[0] < W and 0 <= pos[1] < H and
                not walls[pos[0]][pos[1]]
            }

        def compute_score(pos):

            # We can only eat a ghost if we are on the same position
            if not ghost_positions:
                return 0

            # Precomputing valid distances
            valid_distances = []

            for ghost_pos in ghost_positions:
                # Check if we can reach the ghost position using BFS
                fringe = deque([(pos, 0)])
                visited = {pos}

                while fringe:

                    position, dist = fringe.popleft()

                    if position == ghost_pos:
                        valid_distances.append(dist)
                        break

                    for _, next_pos in get_next_pos(position).items():
                        if next_pos not in visited:
                            visited.add(next_pos)
                            fringe.append((next_pos, dist + 1))

                # Path not found
                else:
                    valid_distances.append(float('inf'))

            return -min(valid_distances) if valid_distances else 0

        # Initialization of BFS
        best_path = []
        best_score = float('-inf')
        depth_limit = 3
        fringe = Queue()
        fringe.push((position, []))
        closed = set()

        # Main loop
        while not fringe.isEmpty():
            (position, path) = fringe.pop()

            if len(path) > depth_limit:
                continue

            key = (tuple(eaten), position)
            if key in closed:
                continue
            closed.add(key)

            current_score = compute_score(position)
            if current_score > best_score:
                best_score = current_score
                best_path = path

            for action, pos in get_next_pos(position).items():
                fringe.push((pos, path + [action]))

        return best_path

    def _get_action(self, walls, beliefs, eaten, position):
        """
        Arguments:
            walls: The W x H grid of walls.
            beliefs: The list of current ghost belief states.
            eaten: A list of booleans indicating which ghosts have been eaten.
            position: The current position of Pacman.

        Returns:
            A legal move as defined in `game.Directions`.
        """
        # If no more moves, computes more
        if not self.moves:
            self.moves = self.get_best_path(walls, beliefs, eaten, position)

        # Use computed moves
        if self.moves:
            move = self.moves.pop(0)
            return move

        return Directions.STOP

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        ! DO NOT MODIFY !

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A legal move as defined in `game.Directions`.
        """

        return self._get_action(
            state.getWalls(),
            state.getGhostBeliefStates(),
            state.getGhostEaten(),
            state.getPacmanPosition(),
        )
