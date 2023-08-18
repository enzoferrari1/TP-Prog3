from ..models.grid import Grid
from ..models.frontier import StackFrontier, PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty and a dictionary to store coords already added to the frontier
        explored = {} 
        seen = {}
        
        # Add the node to the explored dictionary
        explored[node.state] = True
        seen[node.state] = True
        frontier = PriorityQueueFrontier()
        frontier.add(node)
        counter = 0
        max_counter = 20000
        while counter < max_counter:
          if frontier.is_empty():
            return NoSolution(explored)
            break
          node = frontier.pop()
          explored[node.state] = True
          if node.state == grid.end:
            return Solution(node, explored)
            break

          neighbours = grid.get_neighbours(node.state)
          for direction in neighbours.keys():
            new_state = neighbours[direction]
            if not seen.get(new_state, False):
              new_node = Node('', new_state, node.cost + grid.get_cost(new_state))
              new_node.parent = node
              new_node.action = direction
              frontier.add(new_node, priority=grid.get_cost(new_state))
              seen[new_node.state] = True
              
          counter = counter + 1
        return NoSolution(explored)
