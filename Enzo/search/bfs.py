from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {}
        seen = {}

        # Add the node to the explored dictionary
        explored[node.state] = True

        # Create the frontier (FIFO policy, use queue)
        frontier = QueueFrontier()

        # Add first node to the frontier
        frontier.add(node)

        # Set maximum number of iterations to prevent infinite looping for debugging
        max_iterations = 40000
        iteration_count = 0

        while iteration_count < max_iterations:
            # Check if maximum number of iterations has been reached
            if frontier.is_empty():
                return NoSolution(explored)
                break

            # Proceed to take a node from the frontier according to the corresponding policy. Here, we first take the oldest nodes, which is why we use the queue structure
            node = frontier.remove()
            explored[node.state] = True

            if node.state == grid.end:
                return Solution(node, explored)
                break

            # Add adjacent cells to the frontier
            neighbours = grid.get_neighbours(node.state)
            for direction in neighbours.keys():
                new_state = neighbours[direction]
                new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                new_node.parent = node
                new_node.action = direction
                if not seen.get(new_state, False):
                    frontier.add(new_node)
                    seen[new_node.state] = True

            iteration_count += 1

        return NoSolution(explored)

