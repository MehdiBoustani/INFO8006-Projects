from pacman_module.game import Agent, Directions
from pacman_module.util import PriorityQueue, manhattanDistance
from pacman_module.pacman import GameState


def key(state):
    """Returns a key that uniquely identifies a Pacman game state.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        A hashable key tuple.
    """

    return (
        state.getPacmanPosition(),
        state.getFood(),
        tuple(state.getCapsules())
    )


class PacmanAgent(Agent):
    """Pacman agent based on A*."""

    def __init__(self):
        super().__init__()

        self.moves = None

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Return:
            A legal move as defined in `game.Directions`.
        """

        if self.moves is None:
            self.moves = self.astar(state)

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP

    def compute_mst(self, positions, init_pos):
        """Given a list of positions and an initial positions,
        returns the minimum spanning tree toal cost,
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

    def astar(self, state: GameState):
        """Given a Pacman game state, returns a list of legal moves to solve
        the search layout.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A list of legal moves.
        """

        path = []
        fringe = PriorityQueue()
        fringe.push((state, path), priority=0)
        closed = set()
        initial_capsules = state.getCapsules()

        while True:
            if fringe.isEmpty():
                return []

            _, (current, path) = fringe.pop()

            if current.isWin():
                return path

            current_key = key(current)

            if current_key in closed:
                continue
            else:
                closed.add(current_key)

            food_positions = set(current.getFood().asList())
            for successor, action in current.generatePacmanSuccessors():
                pacman_pos = successor.getPacmanPosition()

                forward_cost = self.compute_mst(food_positions, pacman_pos)

                backward_cost = len(path) + 1 +\
                    5*((len(initial_capsules) - len(successor.getCapsules())))

                total_cost = forward_cost + backward_cost

                fringe.push((successor, path + [action]), priority=total_cost)
