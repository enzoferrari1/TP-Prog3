from ..models.grid import Grid
from ..models.frontier import StackFrontier, PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

# Definimos una función heurística para la busqueda informada. En este caso optamos por la distancia Manhattan, aunque también podemos optar con distancia euclideana
def heuristic_func(node: Node, grid: Grid) -> int:
  delta_x = node.state[0] - grid.end[0]
  delta_y = node.state[1] - grid.end[1]
  dist = abs(delta_x) + abs(delta_y) # + grid.get_cost(node.state)
  return dist

class GreedyBestFirstSearch:
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

        # Initialize the explored dictionary to be empty
        explored = {} 
        seen = {}
        
        # Add the node to the explored dictionary
        explored[node.state] = True
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
              frontier.add(new_node, priority=heuristic_func(new_node, grid))
              seen[new_node.state] = True
          counter = counter + 1
        return NoSolution(explored)
