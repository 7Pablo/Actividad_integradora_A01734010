# TC2008B
# M1 Actividad
#
# Juan Pablo Armendariz Salas		A01734010
#
# Descripcion: Programa que simula la interaccion de agentes robot que ordeanan un almacen lleno de cajas en pilas de cinco. La simulacion inicializa las posiciones iniciales de K cajas, en donde no hay cajas en pila. Ademas, todos los agentes empiezan en posicion aleatoria vacia, y se ejecutan en un tiempo especifico. 

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid as PathGrid
from pathfinding.finder.a_star import AStarFinder
import random

# 0 = Limit
# 1 = Space
# 2 = Box
# 3 = Pile

# Funcion que genera una matriz de un tamaño MxN, y la rellena de 1 y 0
# Complejidad: O(n*m)
def createMatrix(n, m):

  matrix = [[ 1 for i in range(n) ] for j in range(m)]

  for i in range(n):
    matrix[0][i] = 0
    matrix[m-1][i] = 0

  for i in range(m):
    matrix[i][0] = 0
    matrix[i][n-1] = 0

  return matrix

# Definicion del agente Robot, que simula los robots que ordenan. Este tiene los atributos de self, model, pos, y pile
class Robot(Agent):
  NOBOX = 0
  WITHBOX = 1

  def __init__(self, model, pos, pile):
        super().__init__(model.next_id(), model)
        self.condition = self.NOBOX
        self.pos = pos
        self.roaming = False
        self.objective = None
        self.endX = 1
        self.endY = 1
        self.pile = pile
        self.box = None
        self.stepsR = 0
        self.finished = False

  def step(self):
    # Se asgina una pila al robot
    if(self.pile == None):
      i = random.randint(0, len(self.model.piles) - 1)
      self.pile = self.model.piles[i]
      self.model.piles.remove(self.pile)

    pathGrid = PathGrid(matrix = self.model.matrix)

    # Se genera objetivo mediante un random del array de cajas
    if (self.roaming == False and self.objective == None and self.model.boxes != [] and self.pile.amount < 5):
      i = random.randint(0, len(self.model.boxes) - 1)
      self.objective = self.model.boxes[i]
      self.model.boxes.pop(i)

    # Se asigna objetivo al robot
    if (self.roaming == False and self.objective != None):
      self.endX = self.objective.pos[0]
      self.endY = self.objective.pos[1]
      self.roaming = True

    # El robot se encuentra sobre una caja
    if(self.model.matrix[self.pos[0]][self.pos[1]] == 2 and self.pos[0] == self.endX and self.pos[1] == self.endY):
      self.condition = self.WITHBOX
      self.model.takeBox(self.pos, self)
      self.box.holder = self

    # El robot se mueve hacia su objetivo actual dependiendo su estado
    if(self.pile.amount < 5):
      # El agente se dirige a una caja aleatoria del grid
      if(self.condition == self.NOBOX):
        start = pathGrid.node(self.pos[0], self.pos[1])
        finish = pathGrid.node(self.endX, self.endY)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, finish, pathGrid)

        if(len(path) > 1):
          newMove = path[1]
          self.model.grid.move_agent(self, newMove)
        else:
          self.roaming = False
          self.objective = None
      
        pathGrid.cleanup()  
      
      # El agente se dirige hacia su pila asignada 
      elif(self.condition == self.WITHBOX):

        self.endX = self.pile.pos[0]
        self.endY = self.pile.pos[1]
        start = pathGrid.node(self.pos[0], self.pos[1])
        finish = pathGrid.node(self.endX, self.endY)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, finish, pathGrid)

        if(len(path) > 1):
          newMove = path[1]
          self.model.grid.move_agent(self, newMove)
        else:
          self.roaming = False
          self.objective = None
          self.condition = self.NOBOX
          self.pile.amount += 1
          self.model.boxesInPile += 1
          self.box.holder = self.pile
    
        pathGrid.cleanup()

    elif (self.pile.amount == 5 and self.finished == False):
      self.stepsR = self.model.steps
      self.model.grid.move_agent(self, (self.endX + 1, self.endY))
      self.finished = True

# Definicion del agente Box, que simula las cajas   
class Box(Agent):
  def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.holder = None
  def step(self):
      if (self.holder != None):
        self.pos = self.holder.pos

# Definicion del agente MetalBlock, que simula las paredes
class MetalBlock(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

# Definicion del agente Pile, que simula las pilas
class Pile(Agent):
    def __init__(self, model, pos, amount):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.amount = amount

# Definicion del modelo WareHouse
class WareHouse(Model):
  def __init__(self):
        super().__init__()

        self.height = 20
        self.width = 20
        self.boxA = 25
        self.totalBoxes = 25
        self.robotN = 5
        self.pileN = 5
        self.boxes = []
        self.piles = []
        self.robots = []
        self.boxesInPile = 0
        self.over = False
        self.steps = 0

        # Se genera la matriz y el grid
        self.matrix = createMatrix(self.width, self.height)
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)
        
        # Se agregan las cajas al grid en base a boxA
        while(self.boxA > 0):
          box = Box(self, (self.random.randint(1, self.width-2), self.random.randint(1, self.height-2)))
          if (self.matrix[box.pos[0]][box.pos[1]] != 2 and self.matrix[box.pos[0]][box.pos[1]] != 3):
            self.grid.place_agent(box, box.pos)
            self.schedule.add(box)
            self.matrix[box.pos[0]][box.pos[1]] = 2
            self.boxes.append(box)
          else:
            self.boxA += 1
          self.boxA -= 1

        # Se agregan los robots al grid en base a robotN
        while (self.robotN > 0):
          robot = Robot(self, (self.random.randint(1, self.width-2), self.random.randint(1, self.height-2)), None)
          if (self.matrix[robot.pos[0]][robot.pos[1]] != 2 and self.matrix[robot.pos[0]][robot.pos[1]] != 3):
            self.grid.place_agent(robot, robot.pos)
            self.schedule.add(robot)
            self.robots.append(robot)
          else:
            self.robotN += 1
          self.robotN -= 1

        # Se agregan las pilas al grid en base a pileN
        while (self.pileN > 0):
          pile = Pile(self, (self.random.randint(1, self.width-2), self.random.randint(1, self.height-2)), 0)
          if (self.matrix[pile.pos[0]][pile.pos[1]] != 2 and self.matrix[pile.pos[0]][pile.pos[1]] != 3):
            self.grid.place_agent(pile, pile.pos)
            self.schedule.add(pile)
            self.matrix[pile.pos[0]][pile.pos[1]] = 3
            self.piles.append(pile)
          else:
            self.pileN += 1
          self.pileN -= 1

        # Se agregan las paredes
        for _,x,y in self.grid.coord_iter():
          if self.matrix[y][x] == 0:
            metalBlock = MetalBlock(self, (x, y))
            self.grid.place_agent(metalBlock, metalBlock.pos)
            self.schedule.add(metalBlock)
        
  def step(self):
      self.schedule.step()
      self.steps += 1

      if(self.over == True):
        for i in range (len(self.robots)):
          print("Total de pasos dados por robot: ", self.robots[i].stepsR)
        print("Tiempo total: ", self.steps)
        self.running = False

      if(self.boxesInPile > self.totalBoxes - 1):
        self.over = True          

  # Funcion que asigna al agente caja un robot
  # Complejidad: O(1)
  def assignRobot(self, box, robot):
    robot.box = box
    box.robot = robot

  # Funcion que cambia las caracteristicas de la celda en base a la posicion actual del robot
  # Complejidad: O(n)
  def takeBox(self, pos, robot):
      agents = self.grid.get_cell_list_contents(pos)
      for agent in agents:
        if(type(agent) == Box):
          self.grid.remove_agent(agent)
          agents.remove(agent)
          self.matrix[pos[1]][pos[0]] == 1
          self.assignRobot(agent, robot)

#Funcion de mesa que define las apariencias de los agentes
#Complejidad: O(1)
def agent_portrayal(agent):

  if(type(agent) == Robot):
    if(agent.condition == agent.NOBOX):
      return {"Shape": "robot.png", "Layer": 0}
    elif(agent.condition == agent.WITHBOX):
      return {"Shape": "robotBox.png", "Layer": 0}
  elif (type(agent) == Box):
    return {"Shape": "box.png", "Layer": 0}
  elif (type(agent) == MetalBlock):
    return {"Shape": "metalBlock.png", "Layer": 0}
  elif (type(agent) == Pile):
    return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Grey", "Layer": 0}

# Se definen las variables de grid y server
grid = CanvasGrid(agent_portrayal, 20, 20, 450, 450)

server = ModularServer(WareHouse, [grid], "Box collector", {})

server.port = 8522
server.launch()