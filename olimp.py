class node:
    def __init__(self, infoNod, coordX, coordY, succesori=None, parent=None):
        self.coordX = coordX
        self.coordY = coordY
        self.infoNod = infoNod
        self.parent = parent
        self.g = float('inf')  # costul de la radacina la nodul curent
        self.h = None  # costul estimat de la nodul curent la nodul tinta
        self.f = float('inf')  # costul total (g + h)
        self.succesori = succesori

        self.expanded = False

    def drumRadacina(self):
        drum = []
        nodCurent = self
        while nodCurent != None:
            drum.append(nodCurent)
            nodCurent = nodCurent.parent

        drum.reverse()

        return drum
    
    def vizitat(self):
        return len([1 for nod in self.drumRadacina() if nod == self]) > 1
    
    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.f
    
    def __str__(self):
        return f"Node({self.infoNod}, {self.coordX}, {self.coordY})"
    
    def __repr__(self):
        return f"{self.infoNod}({self.f})"
    
import heapq


class graph:
    def __init__(self, startNode, goalNodes, nodesData, adjList):

        #Initializam nodurile din jurul Olimpului

        self.nodes = {info : node(info, coords[0], coords[1]) for info, coords in nodesData.items()}

        for info, succ_indices in adjList.items():
            self.nodes[info].succesori = [self.nodes[i] for i in succ_indices]


        self.goalNodes = [self.nodes[goal] for goal in goalNodes]
        self.startNode = self.nodes[startNode]
        self.startNode.g = 0
        self.startNode.h = self._heuristic(self.startNode)
        

    def _euclidian(self, node1, node2):
        dx = abs(node1.coordX - node2.coordX)
        dy = abs(node1.coordY - node2.coordY)
        return (dx * dx + dy * dy)**0.5

    def _heuristic(self, node):
        return min(self._euclidian(node, goalNode) for goalNode in self.goalNodes)

    def _isGoal(self, node):
        return node.infoNod in [goal.infoNod for goal in self.goalNodes]

    def AStar(self, pasi):
        openList = [self.startNode]
        closed = {}
        
        while openList:
            if pasi == 0:
                print(openList)
                return openList
            
            currentNode = heapq.heappop(openList)
            
            if currentNode.infoNod in closed and currentNode.g > closed[currentNode.infoNod]:
                continue
            closed[currentNode.infoNod] = currentNode.g
            
            if self._isGoal(currentNode):
                print(f"gasit {currentNode.infoNod}")
                return currentNode
            
            for successor in currentNode.succesori:
                newG = currentNode.g + self._euclidian(currentNode, successor)
                if successor.infoNod in closed and newG >= closed[successor.infoNod]:
                    continue
                newH = self._heuristic(successor)
                newF = newG + newH
                
                if newG < successor.g:
                    successor.g = newG
                    successor.h = newH
                    successor.f = newF
                    successor.parent = currentNode
                    heapq.heappush(openList, successor)
            pasi -= 1
        return None
    
    def IDAStar(self):
        def expandeaza(nodCurent: node, Limita):
            N_MAX = float('inf')
            f_curent = nodCurent.g + self._heuristic(nodCurent)
            nodCurent.f = f_curent
            if f_curent > Limita:
                return f_curent
            
            if self._isGoal(nodCurent):
                drum_solutie = nodCurent.drumRadacina()
                drumuri_afisate.append(nodCurent)
                print(f"Solutie gasita: {[nod.infoNod for nod in drum_solutie]}")
                return None
            
            LS = nodCurent.succesori
            if not LS:
                return N_MAX
            
            minim = N_MAX
            for succesor in LS:
                orig_g = succesor.g
                orig_parent = succesor.parent

                succesor.g = nodCurent.g + self._euclidian(nodCurent, succesor)
                succesor.parent = nodCurent

                Lim_succesor = expandeaza(succesor, Limita)
                if Lim_succesor is None:
                    return None
                if Lim_succesor < minim:
                    minim = Lim_succesor

                succesor.g = orig_g
                succesor.parent = orig_parent

            return minim if minim != float('inf') else float('inf')

        self.startNode.f = self.startNode.g + self._heuristic(self.startNode)
        Limita = self.startNode.f
        drumuri_afisate = []

        while True:
            Limita_noua = expandeaza(self.startNode, Limita)
            if Limita_noua is None or Limita_noua == float('inf'):
                break
            Limita = Limita_noua
        return drumuri_afisate
    
nodes_data = {
    1: (0, 0),
    2: (2, 0),
    3: (4, 0),
    4: (0, 2),
    5: (2, 2),
    6: (4, 2),
    7: (1, 3),
    8: (2, 3),
    9: (3, 3),
    10: (0, 4),
    11: (1, 4),
    12: (2, 4),
    13: (3, 4),
    14: (4, 4),
    15: (5, 4),
    16: (1, 5),
    17: (2, 5),
    18: (3, 5),
    19: (0, 6),
    20: (2, 6),
    21: (4, 6),
    22: (0, 8),
    23: (2, 8),
    24: (4, 8),
}

connections = {
    1: [2, 10],
    2: [1, 3, 5],
    3: [2, 15],
    4: [5, 11],
    5: [4,2,6,8],
    6: [5,14],
    7: [8,12],
    8: [7,5,9],
    9: [8,13],
    10: [1,22,11],
    11: [10,4,12,19],
    12: [7,11,16],
    13: [9,18,14],
    14: [13,6,21,15],
    15: [3,14,24],
    16: [12,17],
    17: [16,18,20],
    18: [13,17],
    19: [11,20],
    20: [19,17,21,23],
    21: [14,20],
    22: [10,23],
    23: [22,20,24],
    24: [23,15],
}

g = graph(7, [24], nodes_data, connections)

# g.IDAStar()

g.AStar(2)