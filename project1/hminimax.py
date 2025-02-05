from pacman_module.game import Agent, Directions
from pacman_module.util import manhattanDistance, PriorityQueue

from enum import Enum
import math
from math import floor


class Turn(Enum):
    PACMAN = 0
    GHOST = 1


class PacmanAgent(Agent):

    def __init__(self):
        super().__init__()
        self.visited_positions = {}
        self.game_closed = {}
        self.closed = set()
        self.max_depth = 2

    def __get_food_info(self, state):
        pacman_pos = state.getPacmanPosition()
        num_food = state.getNumFood()
        food_pos = state.getFood().asList()

        nearest_food = min(food_pos, key=lambda pos: manhattanDistance(
            pacman_pos, pos), default=None)

        return num_food, nearest_food

    def __key(self, state, turn):
        """Returns a key that uniquely identifies a Pacman game state.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A hashable key tuple.
        """
        pacman_pos = state.getPacmanPosition()
        ghost_info = state.getGhostPosition(1)
        food_info = state.getFood()

        return (
            turn,
            pacman_pos,
            ghost_info,
            food_info
        )

    def __quiescence_test(self, state):
        _, nearest_food = self.__get_food_info(state)
        ghost_pos = state.getGhostPosition(1)
        pacman_pos = state.getPacmanPosition()

        walls = state.getWalls()
        px, py = floor(pacman_pos[0]), floor(pacman_pos[1])
        gx, gy = floor(ghost_pos[0]), floor(ghost_pos[1])

        walls_between = 0

        if px == gx:
            for y in range(min(py, gy), max(py, gy) + 1):
                if walls[px][y]:
                    walls_between += 1
        elif py == gy:
            for x in range(min(px, gx), max(px, gx) + 1):
                if walls[x][py]:
                    walls_between += 1

        nearest_food_dist = manhattanDistance(pacman_pos, nearest_food)
        ghost_dist = manhattanDistance(pacman_pos, ghost_pos)

        if walls_between > 0 and ghost_dist > 3:
            return True
        else:
            return nearest_food_dist < 5

    def __cutoff_test(self, state, depth):
        """Determines whether the game is over or not.

        Arguments:
            state : A game state. See API or class `pacman.GameState`.
            depth : the current depth

        Returns:
            True if gameover or max depth reached, False otherwise
        """
        if state.isWin() or state.isLose():
            return True

        if self.__quiescence_test(state):
            return depth >= self.max_depth
        else:
            return depth >= self.max_depth * 3

    def __evaluation_function(self, state):  # eval(s)
        """evaluationFunction function used for the hminimax algorithm.

        Arguments:
            state: A game state. See API or class `pacman.GameState`.

        Returns:
            The evaluation of state
        """
        if state.isLose():
            return float('-inf')

        if state.isWin():
            return float('inf')

        pacman_pos = state.getPacmanPosition()

        ghost_score = self.compute_mst(
            [state.getGhostPosition(1)], pacman_pos)

        food_score = self.compute_mst(
            state.getFood().asList(), pacman_pos) * 10

        looping_score = math.exp(
            self.visited_positions.get(pacman_pos, 0)) * 5

        return state.getScore() + ghost_score - food_score - looping_score

    def compute_mst(self, positions, init_pos):
        """Given a list of positions and an initial positions,
        returns the minimum spanning tree total cost,
        where the cost of moving from a position
        to another is the manhattan distance.

        Arguments:
            positions: a list of coordinates
            init_pos: the initial coordinate

        Returns:
            The total cost of the minimum spanning tree
        """
        coordinates = set(positions)
        visited = set()
        total_cost = 0
        fringe = PriorityQueue()
        fringe.push(init_pos, priority=0)

        while not fringe.isEmpty():
            cost, u = fringe.pop()

            if u in visited:
                continue

            visited.add(u)
            total_cost += cost

            for v in coordinates.difference(visited):
                dist = manhattanDistance(u, v)
                fringe.push(v, priority=dist)

        return total_cost

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A legal move as defined in `game.Directions`.
        """
        self.closed = set()
        _, action, next_state = self.hminimax(state)

        if next_state:
            next_pos = next_state.getPacmanPosition()
            self.visited_positions[next_pos] = self.visited_positions.get(
                next_pos, 0) + 1

        return action or Directions.STOP

    def hminimax(self, state):
        """Initiates the hminimax algorithm by maximizing pacman's score,
            since pacman starts playing. Expands the full hminimax tree.

        Arguments:
            state: A game state. See API or class `pacman.GameState`.

        Returns:
            A tuple (best_value, best_action), where:
                - best_value: The evaluationFunction score of the best move.
                - best_action: The optimal action for Pacman to take.
        """
        return self.max_value(state, 0)

    def max_value(self, state, depth):
        """
        Evaluates the maximum evaluationFunction value for Pacman, considering
        all possible moves available in the current game state.

        Arguments:
            state: The current game state.

        Returns:
            A tuple (best_value, best_action), where:
                - best_value: The highest evaluationFunction score for pacman.
                - best_action: The action taken by pacman using hminimax algo.
        """
        key = self.__key(state, Turn.GHOST), self.__evaluation_function(state)
        if key in self.game_closed:
            return self.game_closed[key]

        if self.__cutoff_test(state, depth):
            return self.__evaluation_function(state), None

        best_value = float('-inf')
        best_action = None
        best_state = None

        successors = state.generatePacmanSuccessors()
        for next_state, action in successors:
            next_state_key = self.__key(next_state, Turn.GHOST)
            if next_state_key not in self.closed:
                self.closed.add(next_state_key)
                value = self.min_value(next_state, depth + 1)
                self.closed.remove(next_state_key)

                if value > best_value:
                    best_value = value
                    best_action = action
                    best_state = next_state

        # save result to avoid recalculations.
        self.game_closed[key] = best_value, best_action, best_state

        return best_value, best_action, best_state

    def min_value(self, state, depth):
        """
        Evaluates the minimum evaluationFunction value for the ghost.

        Arguments:
            state: The current game state.

        Returns:
            The minimum evaluationFunction score for the ghost.
        """

        if self.__cutoff_test(state, depth):
            return self.__evaluation_function(state)

        value = float('inf')

        key = self.__key(state, Turn.PACMAN), self.__evaluation_function(state)
        if key in self.game_closed:
            return self.game_closed[key]

        successors = state.generateGhostSuccessors(1)

        for next_state, _ in successors:
            next_state_key = self.__key(next_state, Turn.PACMAN)
            if next_state_key not in self.closed:
                # Avoid cycles
                self.closed.add(next_state_key)

                value = min(value, self.max_value(next_state, depth + 1)[0])

                self.closed.remove(next_state_key)

        self.game_closed[key] = value
        return value
