
from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = True
        # We declare the frontier using the stack class, because the LIFO policy fits the purposes of the dfs
        frontier = StackFrontier()
        frontier.add(node)
        counter = 0
        max_counter = 20000

        while counter < max_counter:
          if frontier.is_empty():
            return NoSolution(explored)
            break

          node = frontier.remove()
          explored[node.state] = True
          if node.state == grid.end:
            return Solution(node, explored)
            break
          
          # Explore frontier
          neighbours = grid.get_neighbours(node.state)
          for direction in neighbours.keys():
            new_state = neighbours[direction]
            if not (explored.get(new_state, False)):
              new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
              new_node.parent = node
              new_node.action = direction
              frontier.add(new_node)
          counter = counter + 1
            
        return NoSolution(explored)
