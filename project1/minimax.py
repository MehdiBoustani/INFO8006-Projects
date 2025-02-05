from enum import Enum
import math

from pacman_module.game import Agent, Directions
from pacman_module.util import manhattanDistance


class Turn(Enum):
    PACMAN = 0
    GHOST = 1


class PacmanAgent(Agent):

    def __init__(self):
        super().__init__()
        self.game_closed = {}  # Visited during entire game
        self.closed = set()  # Visited during action

    def __key(self, state, turn):
        """Returns a key that uniquely identifies a Pacman game state.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A hashable key tuple.
        """
        pacman_pos = state.getPacmanPosition()
        ghost_info = state.getGhostPosition(1), state.getGhostDirection(1)
        food_info = tuple(state.getFood().asList()), tuple(state.getCapsules())

        return (
            turn,
            pacman_pos,
            ghost_info,
            food_info
        )

    def __is_terminal(self, state):
        """Determines whether the game is over or not.

        Arguments:
            state : A game state. See API or class `pacman.GameState`.

        Returns:
            True if gameover, False otherwise
        """
        return state.isWin() or state.isLose()

    def __utility(self, state):
        """Utility function used for the minimax algorithm.

        Arguments:
            state: A game state. See API or class `pacman.GameState`.

        Returns:
            The score of the state.
        """
        return state.getScore()

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A legal move as defined in `game.Directions`.
        """
        self.closed = set()
        _, action = self.minimax(state)

        return action or Directions.STOP

    def minimax(self, state):
        """Initiates the minimax algorithm by maximizing pacman's score,
            since pacman starts playing. Expands the full minimax tree.

        Arguments:
            state: A game state. See API or class `pacman.GameState`.

        Returns:
            A tuple (best_value, best_action), where:
                - best_value: The utility score of the best move.
                - best_action: The optimal action for Pacman to take.
        """
        return self.max_value(state)

    def max_value(self, state):
        """
        Evaluates the maximum utility value for Pacman, considering all
        possible moves available in the current game state.

        Arguments:
            state: The current game state.

        Returns:
            A tuple (best_value, best_action), where:
                - best_value: The highest utility score for pacman.
                - best_action: The pacman action corresponding to that score.
        """
        key = self.__key(state, Turn.PACMAN)
        # if key in self.game_closed:
        #     return self.game_closed[key]

        if self.__is_terminal(state):
            best_value, best_action = self.__utility(state), None
        else:
            best_value = -math.inf
            best_action = None

            successors = state.generatePacmanSuccessors()
            for next_state, action in successors:
                next_state_key = self.__key(next_state, Turn.GHOST)
                if next_state_key not in self.closed:
                    self.closed.add(next_state_key)
                    value = self.min_value(next_state)
                    self.closed.remove(next_state_key)

                    if value > best_value:
                        best_value = value
                        best_action = action

        self.game_closed[key] = best_value, best_action
        return best_value, best_action

    def min_value(self, state):
        """
        Evaluates the minimum utility value for the ghost.

        Arguments:
            state: The current game state.

        Returns:
            The minimum utility score for the ghost.
        """

        key = self.__key(state, Turn.GHOST)
        # if key in self.game_closed:
        #     return self.game_closed[key]

        if self.__is_terminal(state):
            worst_value = self.__utility(state)
        else:
            worst_value = math.inf

            successors = state.generateGhostSuccessors(1)

            for next_state, _ in successors:
                next_state_key = self.__key(next_state, Turn.PACMAN)
                if next_state_key not in self.closed:
                    self.closed.add(next_state_key)
                    value = self.max_value(next_state)[0]
                    self.closed.remove(next_state_key)

                    worst_value = min(worst_value, value)

        self.game_closed[key] = worst_value
        return worst_value
