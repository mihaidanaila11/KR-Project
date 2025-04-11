class state:
    def __init__(self, tabla: list, pieseAlbastre: int, pieseRosii: int, parent=None, turn=None):
        self.tabla = tabla
        self.pieseAlbastre = pieseAlbastre
        self.pieseRosii = pieseRosii
        self.parent = parent
        if turn is None:
            self.turn = 'x' if pieseAlbastre > pieseRosii else '0'
        else:
            self.turn = turn # x - MAX, 0 - MIN
        
        self.mori = [
                        [0, 1, 2], [3, 4, 5], [6, 7, 8],
                        [9,10,11], [12,13,14], [15,16,17],
                        [18,19,20], [21,22,23],
                        [0,9,21], [3,10,18], [6,11,15],
                        [1,4,7], [16,19,22], [8,12,17],
                        [5,13,20], [2,14,23]
                    ]
        
        self.connections = {
            0: [1, 9], 
            1: [0, 2, 4], 
            2: [1, 14],
            3: [4, 10], 
            4: [1, 3, 5, 7], 
            5: [4, 13],
            6: [7, 11], 
            7: [4, 6, 8], 
            8: [7, 12],
            9: [0, 10, 21], 
            10: [3, 9, 11, 18], 
            11: [6, 10, 15],
            12: [8, 13, 17], 
            13: [5, 12, 14, 20], 
            14: [2, 13, 23],
            15: [11, 16], 
            16: [15, 17, 19], 
            17: [12, 16],
            18: [10, 19], 
            19: [16, 18, 20, 22], 
            20: [13, 19],
            21: [9, 22], 
            22: [19, 21, 23], 
            23: [14, 22]
        }

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
    
    def _verificareMoara(self, index, tabla):
        for moara in self.mori:
            if index in moara and all(tabla[i] == self.turn for i in moara):
                return True
            
        return False
    
    def _manancaPiese(self, tabla):
        generated = []
        
        for i in range(len(tabla)):
            if tabla[i] != '' and tabla[i] != self.turn:
                if(not self._verificareMoara(i, tabla)):
                    #Pot sa o mananc
                    eatenTable = tabla.copy()
                    eatenTable[i] = ''
                    generated.append(state(eatenTable,
                                            self.pieseAlbastre,
                                            self.pieseRosii,
                                            self,
                                            '0' if self.turn == 'x' else 'x'))
                    
        return generated
                                
    
    def genSuccesori(self):
        generated = []

        if self.pieseAlbastre + self.pieseRosii != 0:
            #Etapa de plasare a pieselor
            # Verificam daca avem piese de pus pe tabla
            piese = self.pieseAlbastre if self.turn == 'x' else self.pieseRosii
            if piese == 0:
                return []
            
            for position in range(len(self.tabla)):
                newTable = self.tabla.copy()
                if newTable[position] != '': #Vrem sa plasam piese asa ca o sa cautam doar locuri goale
                    continue
                newTable[position] = self.turn #Plasam piesa
                
                # Verificam daca am facut moara
                eatenFlag = False
                if self._verificareMoara(position, newTable):
                    # Verificam daca putem sa mancam o piesa
                    eatenBoards = self._manancaPiese(newTable)
                    
                    for board in eatenBoards:
                        if self.turn == 'x':
                            board.pieseAlbastre -= 1
                        else:
                            board.pieseRosii -= 1
                            
                    generated += eatenBoards
                    eatenFlag = True
                    
                                
                if not eatenFlag:
                    # Nu am mancat nimic, adaugam nodul in lista
                    generated.append(state(newTable,
                                            self.pieseAlbastre - 1 if self.turn == 'x' else self.pieseAlbastre,
                                            self.pieseRosii - 1 if self.turn == '0' else self.pieseRosii,
                                            self,
                                            '0' if self.turn == 'x' else 'x'))
                    
        else:
            # Etapa de mutare a pieselor
            for position in range(len(self.tabla)):
                newTable = self.tabla.copy()
                if newTable[position] != self.turn:
                    continue
                
                pieseTabla = sum([1 for i in range(len(newTable)) if newTable[i] == self.turn])
                
                if pieseTabla > 3:
                    #Putem muta doar pe pozitiile adiacente
                    generated += self._movePiece(self.connections[position], newTable, position)
                else:
                    #putem muta oriunde
                    generated += self._movePiece(range(len(self.tabla)), newTable, position)

                
                
        return generated

    def _movePiece(self, loopRange, newTable, oldPosition):
        generated = []
        
        for newPosition in loopRange:
            if newTable[newPosition] != '':
                continue
            
            newMoveTable = newTable.copy()
            newMoveTable[newPosition] = self.turn
            newMoveTable[oldPosition] = ''
            
            # print(f"am mutat de la {position} la {newPosition}")
            
            #Verificam daca am facut moara
            eatenFlag = False
            
            if self._verificareMoara(newPosition, newMoveTable):
                eatenBoards = self._manancaPiese(newMoveTable)
                generated += eatenBoards
                eatenFlag = True
                
            if not eatenFlag:
                generated.append(state(newMoveTable,
                                        self.pieseAlbastre,
                                        self.pieseRosii,
                                        self,
                                        '0' if self.turn == 'x' else 'x'))
        
        return generated
    
    def isWinner(self, turn = None):
        if turn is None:
            turn = self.turn

        # Verificam daca mai avem mutari disponibile sau daca mai are piese pe tabla
        piese = 0
        for position in range(len(self.tabla)):
            if self.tabla[position] == turn:
                piese += 1
                for connection in self.connections[position]:
                    if self.tabla[connection] == '':
                        return False
        
        pieseDePus = self.pieseAlbastre if turn == 'x' else self.pieseRosii
        if piese <= 2 and pieseDePus == 0:
            return True
        
        return True
    
    def _morrisNumber(self):
        return sum(1 for moara in self.mori if all(self.tabla[i] == 'x' for i in moara)) - sum(1 for moara in self.mori if all(self.tabla[i] == '0' for i in moara))
    
    def _blockedOpps(self):
        def getBlockedPieces(turn):
            return sum(
            1
            for i in range(len(self.tabla))
            if self.tabla[i] == turn
            and all(self.tabla[neighbor] != "" for neighbor in self.connections[i])
        )

        
        return getBlockedPieces('0') - getBlockedPieces('x')
    
    def _piecesNumber(self):
        return sum([1 for i in range(len(self.tabla)) if self.tabla[i] == 'x']) - sum([1 for i in range(len(self.tabla)) if self.tabla[i] == '0'])
    
    def _twoPiecesConfig(self):
        def getTwoPiecesConfig(turn):
            return sum(
            1
            for moara in self.mori
            if sum(self.tabla[i] == turn for i in moara) == 2
            and any(self.tabla[i] == "" for i in moara)
            )
        
        return getTwoPiecesConfig('x') - getTwoPiecesConfig('0')
        
    def _threePiecesConfig(self):
        def getThreePiecesConfig(turn):
            return sum(
            1
            for moara in self.mori
            if sum(self.tabla[i] == turn for i in moara) == 2 and any(self.tabla[i] == '' for i in moara)
            )

        return getThreePiecesConfig('x') - getThreePiecesConfig('0')
        
        
    def _openMorris(self):

        return sum(
            1 for moara in self.mori
            if sum(self.tabla[i] == self.turn for i in moara) == 2 and any(self.tabla[i] == '' for i in moara)
        )
        
    def _doubleMorris(self):
        def getDoubleMorris(turn):
            double_morris_count = 0

            for position in range(len(self.tabla)):
                if self.tabla[position] == turn:
                    morrises_with_position = [
                        moara for moara in self.mori if position in moara
                    ]

                    formed_morrises = sum(
                        1 for moara in morrises_with_position if all(self.tabla[i] == turn for i in moara)
                    )

                    if formed_morrises >= 2:
                        double_morris_count += 1

            return double_morris_count
        
        return getDoubleMorris('x') - getDoubleMorris('0')
    
    
    def eval(self, moaraFormata = 0):
        # moaraFormata = 0 daca nicio moara nu s-a format
        # moaraFormata = 1 daca s-a format o moara pe tura jucatorului max
        # moaraFormata = 2 daca s-a format o moara pe tura jucatorului min
        if(self.pieseAlbastre + self.pieseRosii != 0):
            C1,C2,C3,C4,C5,C6 = (18, 26, 1, 6, 12, 7)
            
            return C1 * moaraFormata + C2 * self._morrisNumber() + C3 * self._blockedOpps() + C4 * self._piecesNumber() + C5 * self._twoPiecesConfig() + C6 * self._threePiecesConfig() 
            
        elif sum([1 for i in range(len(self.tabla)) if self.tabla[i] == self.turn]) > 3:
            C1,C2,C3,C4,C5,C6,C7 = (14, 43, 10, 8, 7, 42, 1086)
            
            return C1 * moaraFormata + C2 * self._morrisNumber() + C3 * self._blockedOpps() + C4 * self._piecesNumber() + C5 * self._openMorris() + C6 * self._doubleMorris() + C7 * (1 if self.isWinner('x') else (-1 if self.isWinner('0') else 0))
        else:
            C1,C2,C3,C4 = (10, 1, 16, 1190)

            return C1 * self._twoPiecesConfig + C2 * self._threePiecesConfig + C3 * moaraFormata + C4 * (1 if self.isWinner('x') else (-1 if self.isWinner('0') else 0))
        
    def __str__(self):
        t = self.tabla  # for convenience
    
        return (
            f"{t[0]}-----------{t[1]}-----------{t[2]}\n"
            f"|           |           |\n"
            f"|   {t[3]}-------{t[4]}-------{t[5]}   |\n"
            f"|   |       |       |   |\n"
            f"|   |   {t[6]}---{t[7]}---{t[8]}   |   |\n"
            f"|   |   |       |   |   |\n"
            f"{t[9]}---{t[10]}---{t[11]}       {t[12]}---{t[13]}---{t[14]}\n"
            f"|   |   |       |   |   |\n"
            f"|   |   {t[15]}---{t[16]}---{t[17]}   |   |\n"
            f"|   |       |       |   |\n"
            f"|   {t[18]}-------{t[19]}-------{t[20]}   |\n"
            f"|           |           |\n"
            f"{t[21]}-----------{t[22]}-----------{t[23]}\n"
            f"Albastre: {self.pieseAlbastre} | Rosu: {self.pieseRosii}\n"
            f"Turn: {self.turn}\n"
        )
    
    def __repr__(self):
        return f"{self.tabla}"
    
class minmax:
    def __init__(self, startNode: state, adancime: int, alpha: int, beta: int, algorithm):
        self.startNode = startNode
        self.adancime = adancime
        self.alpha = alpha
        self.beta = beta
        self.algorithm = True if algorithm == 'AlphaBeta' else False
        
    def __str__(self):
        return f"Adancime: {self.adancime}, Alpha: {self.alpha}, Beta: {self.beta}"
    
    def __repr__(self):
        return f"{self.startNode}"
    
    def minmax(self, position: state, adancime: int, alpha, beta, turn):
        if adancime == 0 or position.isWinner(turn) or position.vizitat():
            return position.eval()
        
        if turn == 'x':
            maxEval = float('-inf')
            bestMove = None
            for child in position.genSuccesori():
                eval = self.minmax(child, adancime - 1, alpha, beta, '0')
                if eval > maxEval:
                    maxEval = eval
                    bestMove = child

                if self.algorithm:
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            if adancime == self.adancime:
                print(f"Next best move:\n{bestMove}")
            return maxEval
        else:
            minEval = float('inf')
            bestMove = None
            for child in position.genSuccesori():
                eval = self.minmax(child, adancime - 1, alpha, beta, 'x')
                if eval < minEval:
                    minEval = eval
                    bestMove = child

                if self.algorithm:
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            if adancime == self.adancime:
                print(f"Next best move:\n{bestMove}")
            return minEval
state1 = state(['','','','','','x','','','0','','x','x','0','x','','','','0','x','0','x','','0',''], 3, 4 )

# test_state = state(
#     [
#         "x", "0", "x",     # 0  1  2
#         "0", "x", "0",     # 3  4  5
#         "x", "0", "x",     # 6  7  8
#         "0", "", "x",     # 9 10 11
#         "x", "", "",     #12 13 14
#         "0", "x", "",     #15 16 17
#         "0", "", "x",     #18 19 20
#         "", "0", "0 "      #21 22 23
#     ],
#     pieseAlbastre=0,
#     pieseRosii=0,
#     turn='0'
# )


test_state = state(
    ['','','','','','x','','','0','','x','x','0','x','','','','0','x','0','x','','0',''],
    pieseAlbastre=3,
    pieseRosii=4,
)
m = minmax(test_state, 3, float('-inf'), float('inf'), 'AlphaBeta')

print(test_state)

m.minmax(m.startNode, m.adancime, float('-inf'), float('+inf'), m.startNode.turn)