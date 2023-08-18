"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem
from node import Node
from random import choice
from time import time


# Definimos una clase para la lista tabú
class TabuList():
  def __init__(self, size: int) -> None:
    self.list = [] # Lista donde guardamos las acciones prohibidas
    self.size = size
  
  # Agregar una acción a la lista tabú (Decidimos mantener el largo de la lista quitando elementos de esta como criterio de parada)
  def add(self, action: tuple) -> None:
    self.list.append(action)
    if len(self.list) > self.size:
      self.list.pop(0)
  





class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init)) # problem.init crea el estado inicial, obj_val devuelve el valor del estado

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state) # Diferencia entre sucesor y los potenciales

            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local
            if diff[act] <= 0: # Si todas las diferencias son negativas, es decir, el sucesor es mas grande que todos los potenciales

                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end-start
                return

            # Sino, moverse a un nodo con el estado sucesor
            else:

                actual = Node(problem.result(actual.state, act),
                              actual.value + diff[act])
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Se crea un diccionario de las soluciones que se encuentran en cada reseteo
        solution_list = []

        # Se hacen una cantidad de reseteos en un bucle for
        for iteration in range(5):
            problem.random_reset()
            actual = Node(problem.init, problem.obj_val(problem.init))

            while True:
                # Determinar las acciones que se pueden aplicar
                # y las diferencias en valor objetivo que resultan
                diff = problem.val_diff(actual.state)  # Diferencia entre sucesor y los potenciales

                # Buscar las acciones que generan el mayor incremento de valor obj
                max_acts = [act for act, val in diff.items() if val == max(diff.values())]

                # Elegir una accion aleatoria
                act = choice(max_acts)

                # Retornar si estamos en un optimo local
                if diff[act] <= 0:  # Si todas las diferencias son negativas, es decir, el sucesor es mas grande que todos los potenciales
                    break

                # Sino, moverse a un nodo con el estado sucesor
                else:
                    actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                    self.niters += 1

            # Luego de que termine el while, agregar el estado actual a la lista de soluciones
            solution_list.append(actual)

        # Luego de que terminen todos los reseteos, elegir el estado con mayor valor
        final = max(solution_list, key=lambda x: x.value)
        self.tour = final.state
        self.value = final.value
        end = time()
        self.time = end - start
        return

class Tabu(LocalSearch):
    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init)) # problem.init crea el estado inicial, obj_val devuelve el valor del estado

        
        tabu_size = 20
        limit_niter = 1500
        # Crear lista Tabú
        tabu_list = TabuList(size = tabu_size)

        global_solution = actual

        while (self.niters < limit_niter):

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state) # Diferencia entre sucesor y los potenciales
            diff_tabu = {act: val for act, val in diff.items() if
                         ((act not in tabu_list.list and act[::-1] not in tabu_list.list) # Chequea que tanto la accion como su inversa no esté en la lista tabu
                         or problem.obj_val(problem.result(actual.state, act)) > global_solution.value)} # O la admite en el caso de que supere al máximo global
            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [act for act, val in diff_tabu.items() 
                        if val == max(diff_tabu.values())] # Elige el máximo

            # Elegir una accion aleatoria
            act = choice(max_acts)
            tabu_list.add(act)

            actual = Node(problem.result(actual.state, act), actual.value + diff[act])

            if actual.value > global_solution.value:
              global_solution = actual

            self.niters += 1

        # Luego de que se haya alcanzado el límite de iteraciones, devolver la mejor solución
        
        self.tour = global_solution.state
        self.value = global_solution.value
        end = time()
        self.time = end - start
        return


