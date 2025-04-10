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
        nodCurent = nodCurent.parinte

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
                                            self.pieseAlbastre if self.turn == 'x' else self.pieseAlbastre + 1,
                                            self.pieseRosii if self.turn == '0' else self.pieseRosii + 1,
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
                
                for connection in self.connections[position]:
                    if newTable[connection] != '':
                        continue
                    
                    newMoveTable = newTable.copy()
                    newMoveTable[connection] = self.turn
                    newMoveTable[position] = ''
                    
                    # print(f"am mutat de la {position} la {connection}")
                    
                    #Verificam daca am facut moara
                    eatenFlag = False
                    
                    if self._verificareMoara(connection, newMoveTable):
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
    
state1 = state(['','','','','','x','','','0','','x','x','0','x','','','','0','x','0','x','','0',''], 3, 4 )

test_state = state(
    [
        "x", "0", "x",     # 0  1  2
        "0", "x", "0",     # 3  4  5
        "x", "0", "x",     # 6  7  8
        "0", "", "x",     # 9 10 11
        "x", "", "",     #12 13 14
        "0", "x", "",     #15 16 17
        "0", "", "x",     #18 19 20
        "", "0", "0 "      #21 22 23
    ],
    pieseAlbastre=0,
    pieseRosii=0,
    turn='x'
)

print(f"Initial state:\n{test_state}")

for stare in test_state.genSuccesori():
    print(stare)
            
