import numpy as np

class FA:
    def __init__(self, TransitionTable='', Q=[], A=[], D=[], q0=0, F=[]):
        self.Q = Q  # States
        self.A = A  # Alphabet
        self.D = D  # Transition function
        self.q0 = q0  # Starting state
        self.F = F  # Set of final states
        self.StateToPos = {}  # Save the position of each State in FA
        self.SymbolToPos = {}  # Save the position of each Symbol in Alphabet

        if TransitionTable != '':
            self.Build(TransitionTable)
        else:
            # Index states and symbols
            self.IndexStatesAndSymbols()

    def Build(self, TransitionTable):
        # Get alphabet
        for i in range(1, len(TransitionTable[0])):
            if str.isalnum(TransitionTable[0][i]):
                self.A.append(TransitionTable[0][i])
        # Get states
        for i in range(1, len(TransitionTable)):
            temp = ''
            for symbol in TransitionTable[i]:
                if str.isdigit(symbol):
                    temp += symbol
                elif symbol == '|':
                    self.Q.append(int(temp))
                    break
        # Get starting state and set of final states
        for i in range(1, len(TransitionTable)):
            for symbol in TransitionTable[i]:
                if symbol == '>':
                    # Is starting state
                    self.q0 = int(self.Q[i - 1])
                    break
                elif symbol == '*':
                    # Is final state
                    self.F.append(int(self.Q[i - 1]))
                    break
                elif symbol == '@':
                    # Is either starting or final state
                    self.q0 = int(self.Q[i - 1])
                    self.F.append(int(self.Q[i - 1]))
                    break
        # Index states and symbols
        self.IndexStatesAndSymbols()

    def IndexStatesAndSymbols(self):
        # Save the position of each State in FA
        for i in range(len(self.Q)):
            self.StateToPos[self.Q[i]] = i
        # Save the position of each Symbol in Alphabet
        for i in range(len(self.A)):
            self.SymbolToPos[self.A[i]] = i

class DFA(FA):
    def __init__(self, TransitionTable='', Q=[], A=[], D=[], q0=0, F=[]):
        super().__init__(TransitionTable, Q, A, D, q0, F)
        if TransitionTable != '':
            self.BuildTransitionFunction(TransitionTable)

    def BuildTransitionFunction(self, TransitionTable):
        # Initialize transition function
        self.D = DFADelta(len(self.Q), len(self.A))
        for i in range(1, len(TransitionTable)):
            flag = False
            temp = ''
            num = 0
            j = 1
            while j < len(TransitionTable[i]):
                if flag:
                    if str.isdigit(TransitionTable[i][j]):
                        temp += TransitionTable[i][j]
                    elif TransitionTable[i][j] == '|':
                        flag = False
                        self.D.Rows[i - 1][num] = int(temp)
                        temp = ''
                        num += 1
                        j -= 1
                else:
                    if TransitionTable[i][j] == '|':
                        flag = True
                j += 1
            if temp != '':  # Get the final value left in current row
                self.D.Rows[i - 1][num] = int(temp)

    def Move(self, q, a):
        return self.D.Rows[self.StateToPos[q]][self.SymbolToPos[a]]

    def EliminateUnreachableStates(self):
        # Find unreachable states
        ReachableStates = []
        CurrentStates = []
        ReachableStates.append(self.q0)
        CurrentStates.append(self.q0)

        while len(CurrentStates) > 0:
            temp = []
            for state in CurrentStates:
                for symbol in self.A:
                    s = self.Move(state, symbol)
                    if s not in temp:
                        temp.append(s)

            for state in ReachableStates:
                if state in temp:
                    temp.remove(state)
            CurrentStates = temp

            for state in CurrentStates:
                ReachableStates.append(state)

        # Eliminate unreachable states
        # NewDelta = []
        # for state in self.Q:
        #     if state not in ReachableStates:
        #         self.Q.remove(state)
        #     else:
        #         NewDelta.append(self.D.Rows[self.StateToPos[state]])
        # self.D.Rows = NewDelta

        # Eliminate unreachable states and return result
        NewStates = []
        NewDelta = DFADelta(Rows=[])
        NewFinalStates = []
        for state in self.Q:
            if state in ReachableStates:
                NewStates.append(state)
                NewDelta.Rows.append(self.D.Rows[self.StateToPos[state]])
        for state in self.F:
            if state in ReachableStates:
                NewFinalStates.append(state)
        result = DFA(Q=NewStates, A=self.A, D=NewDelta, q0=self.q0, F=NewFinalStates)
        return result

    def Check(self, Text):
        # Checking whether a string is accepted or rejected
        CurrentState = self.q0
        for item in Text:
            CurrentState = self.Move(CurrentState, item)
        if CurrentState in self.F:
            return True
        else:
            return False

    def CheckArray(self, Text):
        a = np.uint8(np.zeros([len(Text),]))
        CurrentState = self.q0
        for i in range (len(Text)):
            CurrentState = self.Move(CurrentState, Text[i])
            a[i] = CurrentState

        return a

    def Print(self, FileName=''):
        TransitionTable = []
        MaxSizeOfCols = []
        _Rows = np.array(self.D.Rows)
        _Q = np.array(self.Q)

        # Find the max size of the first column (state column)
        MaxSizeOfCols.append(str(_Q.max()).__len__() + 2)
        # Find the max sizes of the remaining columns
        for col in range(len(self.A)):
            CurrentCol = _Rows[:, col]
            MaxVal = CurrentCol.max()
            MaxSizeOfCols.append(str(MaxVal).__len__() + 2)

        tempStr = ''
        # Create the first line
        tempStr += ('{0:' + str(MaxSizeOfCols[0]) + '}').format('')
        for i in range(self.A.__len__()):
            tempStr += ('{0}{1:^' + str(MaxSizeOfCols[i + 1]) + '}').format('|', self.A[i])
        TransitionTable.append(tempStr)
        tempStr = ''
        # Create the remaining lines
        for i in range(len(self.Q)):
            if self.Q[i] == self.q0 and self.Q[i] in self.F: # is both starting and final state
                tempStr += ('{0}{1:<' + str(MaxSizeOfCols[0] - 1) + '}').format('@', self.Q[i])
            elif self.Q[i] == self.q0: # is starting state
                tempStr += ('{0}{1:<' + str(MaxSizeOfCols[0] - 1) + '}').format('>', self.Q[i])
            elif self.Q[i] in self.F: # is final state
                tempStr += ('{0}{1:<' + str(MaxSizeOfCols[0] - 1) + '}').format('*', self.Q[i])
            else:
                tempStr += ('{0}{1:<' + str(MaxSizeOfCols[0] - 1) + '}').format(' ', self.Q[i])            
            
            for j in range(self.A.__len__()):
                tempStr += ('{0}{1:^' + str(MaxSizeOfCols[j + 1]) + '}').format('|', _Rows[i][j])            
            
            TransitionTable.append(tempStr)
            tempStr = ''

        if FileName == '': # Not print to file, just print to console
            for row in TransitionTable:
                print(row)
        else: # Print to file
            output = open(FileName, 'w')
            for row in TransitionTable:
                output.write(row)
                output.write('\n')
            output.close()

class NFA(FA):
    def __init__(self, TransitionTable='', Q=[], A=[], D=[], q0=0, F=[]):
        super().__init__(TransitionTable, Q, A, D, q0, F)
        if TransitionTable != '':
            self.BuildTransitionFunction(TransitionTable)

    def BuildTransitionFunction(self, TransitionTable):
        self.D = NFADelta(len(self.Q), len(self.A))
        row = 1
        while row < len(TransitionTable):
            bReadEpsiTran = False
            CheckPoint = 0
            j = 1
            while j < len(TransitionTable[row]):
                if bReadEpsiTran:
                    CheckPoint = j
                    break
                if TransitionTable[row][j] == ' ':
                    j += 1
                    continue
                if (TransitionTable[row][j] == '|') and (not bReadEpsiTran):
                    k = j + 1
                    while k < len(TransitionTable[row]):
                        if TransitionTable[row][k] == ' ':
                            k += 1
                            continue
                        if TransitionTable[row][k] == '-':
                            j = k
                            bReadEpsiTran = True
                            break
                        elif TransitionTable[row][k] == '{':
                            tempNum = ''
                            for h in range(k + 1, len(TransitionTable[row])):
                                if TransitionTable[row][h] == '}':
                                    j = h
                                    self.D.Epsilon[row - 1].append(int(tempNum))
                                    tempNum = ''
                                    bReadEpsiTran = True
                                    break
                                if TransitionTable[row][h] == ' ':
                                    h += 1
                                    continue
                                if TransitionTable[row][h] == ',':
                                    self.D.Epsilon[row - 1].append(int(tempNum))
                                    tempNum = ''
                                    h += 1
                                    continue
                                if str.isdigit(TransitionTable[row][h]):
                                    tempNum += TransitionTable[row][h]
                            break

                        k += 1

                j += 1

            tempNumChar = 0
            j = CheckPoint
            while j < len(TransitionTable[row]):
                if TransitionTable[row][j] == ' ':
                    j += 1
                    continue
                if TransitionTable[row][j] == '|':
                    k = j + 1
                    while k < len(TransitionTable[row]):
                        if TransitionTable[row][k] == ' ':
                            k += 1
                            continue
                        if TransitionTable[row][k] == '-':
                            j = k
                            tempNumChar += 1
                            break
                        elif TransitionTable[row][k] == '{':
                            tempNum = ''
                            h = k + 1
                            while h < len(TransitionTable[row]):
                                if TransitionTable[row][h] == '}':
                                    j = h
                                    self.D.Rows[row - 1][tempNumChar].append(int(tempNum))
                                    tempNum = ''
                                    tempNumChar += 1
                                    break
                                if TransitionTable[row][h] == ' ':
                                    h += 1
                                    continue
                                if TransitionTable[row][h] == ',':
                                    self.D.Rows[row - 1][tempNumChar].append(int(tempNum))
                                    tempNum = ''
                                    h += 1
                                    continue
                                if str.isdigit(TransitionTable[row][h]):
                                    tempNum += TransitionTable[row][h]
                                h += 1
                            break
                        k += 1

                j += 1

            row += 1

    def Move(self, q, a):
        # print(a)
        return self.D.Rows[self.StateToPos[q]][self.SymbolToPos[a]]

    def MoveFromASetOfStates(self, S, a):
        result = set()

        for state in S:
            temp = self.Move(state, a)
            for item in temp:
                result.add(item)

        return list(result)

    def EpsiMove(self, q):
        return self.D.Epsilon[self.StateToPos[q]]

    def EpsiClosureOfAState(self, q):
        tempStack = []
        result = set()
        tempStack.append(q)
        result.add(q)

        while len(tempStack) > 0:
            top = tempStack.pop()
            epsiState = self.EpsiMove(top)
            for state in epsiState:
                if state not in result:
                    result.add(state)
                    tempStack.append(state)

        return list(result)

    def EpsiClosureOfASetOfStates(self, S):
        tempStack = []
        result = set()

        for state in S:
            result.add(state)
            tempStack.append(state)

        while len(tempStack) > 0:
            top = tempStack.pop()
            epsiState = self.EpsiMove(top)
            for state in epsiState:
                if state not in result:
                    result.add(state)
                    tempStack.append(state)

        return list(result)

    # def AllChecked(self, Sets, Monitor):
    #     for Set in Sets:
    #         if Monitor[Sets.index(Set)] == False:
    #             return False
    #     return True

    # def IsIncludeFinalStateOfNFA(self, S):
    #     for state in S:
    #         if state in self.F:
    #             return True
    #     return False

    # def ConvertNFAtoDFA(self):

    #     DFAsRows = [] # Save the result
    #     temp = [self.EpsiClosureOfAState(self.q0)]

    #     NewSets = [temp[0]]
    #     SetsMonitor = [False]
    #     NumOfSetsMonitor = [0]
    #     FinalStatesMonitor = []
    #     if self.IsIncludeFinalStateOfNFA(temp[0]):
    #         FinalStatesMonitor.append(NumOfSetsMonitor[NewSets.index(temp[0])])
    #     StateNum = 1
    #     HasDeadState = False # False means our DFA hasn't had a dead state yet

    #     while not self.AllChecked(temp, SetsMonitor):
    #         for Set in temp:
    #             if SetsMonitor[NewSets.index(Set)] == False:
    #                 SetsMonitor[NewSets.index(Set)] = True
    #                 DFAsRows.append([])
    #                 for symbol in self.A:
    #                     U = self.EpsiClosureOfASetOfStates(self.MoveFromASetOfStates(Set, symbol))
    #                     if U != []:
    #                         if U not in temp:
    #                             temp.append(U)
    #                             NewSets.append(U)
    #                             SetsMonitor.append(False)
    #                             NumOfSetsMonitor.append(StateNum)
    #                             StateNum += 1
    #                             if self.IsIncludeFinalStateOfNFA(U):
    #                                 FinalStatesMonitor.append(NumOfSetsMonitor[NewSets.index(U)])
    #                         DFAsRows[-1].append(NumOfSetsMonitor[NewSets.index(U)])
    #                     else: # U == [] so we need a dead state
    #                         DFAsRows[-1].append(-1)
    #                         HasDeadState = True
    #     # Check for dead state
    #     if HasDeadState:
    #         DeadState = StateNum
    #         for row in DFAsRows:
    #             i = 0
    #             while i < len(self.A):
    #                 if row[i] == -1:
    #                     row[i] = DeadState
    #                 i += 1
    #         # Create a dead state
    #         DFAsRows.append([])
    #         for item in self.A:
    #             DFAsRows[-1].append(DeadState)
    #         NumOfSetsMonitor.append(DeadState)

    #     result = DFA(Q=NumOfSetsMonitor, A=self.A, q0=NumOfSetsMonitor[0], D=DFADelta(Rows=DFAsRows), F=FinalStatesMonitor)
    #     return result

    def EliminateUnreachableStates(self):
        # Find unreachable states
        ReachableStates = self.EpsiClosureOfAState(self.q0)
        CurrentStates = self.EpsiClosureOfAState(self.q0)

        while len(CurrentStates) > 0:
            temp = []
            for state in CurrentStates:
                for symbol in self.A:
                    MyState = self.EpsiClosureOfASetOfStates(self.Move(state, symbol))
                    for item in MyState:
                        if item not in temp:
                            temp.append(item)

            for state in ReachableStates:
                if state in temp:
                    temp.remove(state)
            CurrentStates = temp

            for state in CurrentStates:
                ReachableStates.append(state)

        # Eliminate unreachable states and return result
        NewStates = []
        NewDelta = NFADelta(Rows=[], Epsilon=[])
        NewFinalStates = []
        for state in self.Q:
            if state in ReachableStates:
                NewStates.append(state)
                NewDelta.Rows.append(self.D.Rows[self.StateToPos[state]])
                NewDelta.Epsilon.append(self.D.Epsilon[self.StateToPos[state]])
        for state in self.F:
            if state in ReachableStates:
                NewFinalStates.append(state)
        result = NFA(Q=NewStates, A=self.A, D=NewDelta, q0=self.q0, F=NewFinalStates)
        return result

    def Check(self, Text):
        # Checking whether a string is accepted or rejected
        CurrentSetOfStates = self.EpsiClosureOfAState(self.q0)
        
        for item in Text:
            CurrentSetOfStates = self.EpsiClosureOfASetOfStates(self.MoveFromASetOfStates(CurrentSetOfStates, item))             
        for state in CurrentSetOfStates:
            if state in self.F:
                return True
        return False

    def LastState(self, Text):
        CurrentSetOfStates = self.EpsiClosureOfAState(self.q0)
        for item in Text:
            CurrentSetOfStates = self.EpsiClosureOfASetOfStates(self.MoveFromASetOfStates(CurrentSetOfStates, item))

        return CurrentSetOfStates
    def Print(self, FileName=''):
        TransitionTable = []
        MaxSizeOfCols = []
        _Rows = np.array(self.D.Rows)
        _Q = np.array(self.Q)

        # Find the max size of the first column (state column)
        MaxSizeOfCols.append(str(_Q.max()).__len__() + 2)
        # Find the max size of the second column (epsilon column)
        epsiMax = 0
        MaxNumItem = 0
        temp = ''
        for row in self.D.Epsilon:
            if row == []:
                if epsiMax < 3:
                    epsiMax = 3
            else:
                for item in row:
                    temp += str(item)
                    MaxNumItem += 1            
                tempLen = temp.__len__() + 2 + 2*MaxNumItem
                if tempLen > epsiMax:
                    epsiMax = tempLen
                temp = ''
                MaxNumItem = 0
        MaxSizeOfCols.append(epsiMax)

        # Find the max sizes of the remaining columns
        for col in range(len(self.A)):
            CurrentCol = _Rows[:, col]

            MaxVal = 0
            MaxNumItem = 0
            temp = ''
            for row in CurrentCol:
                if row == []:
                    if MaxVal < 3:
                        MaxVal = 3
                else:
                    for item in row:
                        temp += str(item)
                        MaxNumItem += 1            
                    tempLen = temp.__len__() + 2 + 2*MaxNumItem
                    if tempLen > MaxVal:
                        MaxVal = tempLen
                    temp = ''
                    MaxNumItem = 0
            MaxSizeOfCols.append(MaxVal)

        tempStr = ''
        # Create the first line
        tempStr += ('{0:' + str(MaxSizeOfCols[0]) + '}').format('')
        tempStr += ('{0}{1:^' + str(MaxSizeOfCols[1]) + '}').format('|', '$')
        for i in range(self.A.__len__()):
            tempStr += ('{0}{1:^' + str(MaxSizeOfCols[i + 2]) + '}').format('|', self.A[i])
        TransitionTable.append(tempStr)
        tempStr = ''
        # Create the remaining lines
        for i in range(len(self.Q)):
            if self.Q[i] == self.q0 and self.Q[i] in self.F: # is both starting and final state
                tempStr += ('{0}{1:<' + str(MaxSizeOfCols[0] - 1) + '}').format('@', self.Q[i])
            elif self.Q[i] == self.q0: # is starting state
                tempStr += ('{0}{1:<' + str(MaxSizeOfCols[0] - 1) + '}').format('>', self.Q[i])
            elif self.Q[i] in self.F: # is final state
                tempStr += ('{0}{1:<' + str(MaxSizeOfCols[0] - 1) + '}').format('*', self.Q[i])
            else:
                tempStr += ('{0}{1:<' + str(MaxSizeOfCols[0] - 1) + '}').format(' ', self.Q[i])            
            
            if self.D.Epsilon[i].__len__() == 0:
                tempStr += ('{0}{1:^' + str(MaxSizeOfCols[1]) + '}').format('|', '-')
            else:
                tempSet = '{' + str(self.D.Epsilon[i][0])
                j = 1
                while j < self.D.Epsilon[i].__len__():
                    tempSet += ', ' + str(self.D.Epsilon[i][j])
                    j += 1
                tempSet += '}'
                tempStr += ('{0}{1:^' + str(MaxSizeOfCols[1]) + '}').format('|', tempSet)

            for j in range(self.A.__len__()):
                # tempStr += ('{0}{1:^' + str(MaxSizeOfCols[j + 2]) + '}').format('|', _Rows[i][j])
                if self.D.Rows[i][j].__len__() == 0:
                    tempStr += ('{0}{1:^' + str(MaxSizeOfCols[j + 2]) + '}').format('|', '-')
                else:
                    tempSet = '{' + str(self.D.Rows[i][j][0])
                    k = 1
                    while k < self.D.Rows[i][j].__len__():
                        tempSet += ', ' + str(self.D.Rows[i][j][k])
                        k += 1
                    tempSet += '}'
                    tempStr += ('{0}{1:^' + str(MaxSizeOfCols[j + 2]) + '}').format('|', tempSet)   
            
            TransitionTable.append(tempStr)
            tempStr = ''

        if FileName == '': # Not print to file, just print to console
            for row in TransitionTable:
                print(row)
        else: # Print to file
            output = open(FileName, 'w')
            for row in TransitionTable:
                output.write(row)
                output.write('\n')
            output.close()

class DFADelta:
    def __init__(self, NumberOfStates=0, NumberOfSymbols=0, Rows=[]):
        self.Rows = Rows
        if self.Rows == []:
            for i in range(NumberOfStates):
                self.Rows.append([])
                for j in range(NumberOfSymbols):
                    self.Rows[i].append(-1)

class NFADelta:
    def __init__(self, NumberOfStates=0, NumberOfSymbols=0, Rows=[], Epsilon=[]):
        self.Rows = Rows
        self.Epsilon = Epsilon
        if self.Rows == []:
            for i in range(NumberOfStates):
                self.Rows.append([])
                self.Epsilon.append([])
                for j in range(NumberOfSymbols):
                    self.Rows[i].append([])