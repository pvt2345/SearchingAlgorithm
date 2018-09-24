import function
class FindingPatternAutomata:
    def __init__(self, pattern):
        # self.pattern = pattern
        self.P = list(set(pattern.split()))
        self.pattern = function.EncodePattern(pattern)
        # self.Q = function.CapSoCoNghia(pattern)
        self.Q = function.CapSoCoNghia_2(self.pattern)
        self.A = function.GetAlphabet(self.pattern)
        self.M = len(function.fact(self.pattern)) - 1
        with open('Character.txt', 'r') as f:
            self.Character = f.read().splitlines()
        self.BuildTFuzz()

    def BuildTFuzz(self):
        self.TFuzz = []
        for i in range(len(self.Q)):
            self.TFuzz.append([])

        for i in range(len(self.Q)):
            for j in range(len(self.A)):
                y = function.SuffixOfPrefix(self.pattern, self.Q[i][0], self.Q[i][1])
                v = function.lfact(y + self.A[j], self.pattern)
                # self.TFuzz[i].append(function.lid(v, self.pattern))
                a = function.lid_2(v, self.pattern)
                # self.TFuzz[i].append(function.lid_2(v, self.pattern))
                self.TFuzz[i].append(self.Q.index(a))


    def CharTrans(self, state, char):
        if char not in self.A:
            return self.Q[0]
        else:
            StateIndex = self.Q.index(state)
            CharIndex = self.A.index(char)
            return self.Q[self.TFuzz[StateIndex][CharIndex]]

    def StringTrans(self, string):
        CurrentState = self.Q[0]
        for char in string:
            CurrentState = self.CharTrans(CurrentState, char)
        return CurrentState

    def FindLongestCommonSubstring(self, string):
        LenMax = 0
        LF_P = 0 #vị trí kết thúc xuất hiện trên P
        LF_S = 0 #vị trí kết thúc xuất hiện trên S
        CurrentState = self.Q[0]
        f_max = 0
        for i in range(len(string)):
            d = CurrentState[1]
            CurrentState = self.CharTrans(CurrentState, string[i])
            if(CurrentState[0] > f_max):
                f_max = CurrentState[0]
            else:
                if(LenMax < f_max):
                    LenMax = f_max
                    LF_P = d
                    LF_S = i
                    f_max = CurrentState[0]
        return LF_P, LF_S, LenMax

    def Search(self, string):
        #tiền xử lý mẫu
        string_ = function.Encoding(string, self.P, self.Character)
        # print(string_)
        #search
        # print(self.pattern)
        n = len(string_)
        H = 0
        CurrentState = self.Q[0]
        a = []
        for i in range(0, n):
            CurrentState = self.CharTrans(CurrentState, string_[i])
            # print(CurrentState)
            # if(CurrentState[3] == 0) & (CurrentState[0] != 0):
            if(CurrentState[0] != 0):
                # print(CurrentState)
                a.append(i)
                H += CurrentState[2]*CurrentState[0]
            # print(CurrentState)
        # print(a)
        a_ = function.GetPosition(string, a)
        return H, a_


if __name__ == '__main__':
    pattern = 'thuế xuất nhập khẩu'
    # pattern_ = function.EncodePattern(pattern)
    # with open('Character.txt', 'r') as f:
    #     Character = f.read().splitlines()
    # f.close()
    # print(pattern_)
    # P = list(set(pattern.split()))
    #
    # #
    # with open("D:\CMC_TextMining\SearchingAlgorithm/testSearch/test1.txt", encoding='UTF-8-sig') as file:
    #     text = file.read()
    # file.close()
    # string = function.Encoding(text, P, Character)

    text = 'abc xyz thuế nhập bxsfe khẩu xuất'

    import time
    a = time.time()
    automata = FindingPatternAutomata(pattern)
    # print()
    # print(automata.A)
    # print(automata.Q)
    # print(automata.TFuzz)
    print(automata.Search(text))
    print(time.time() - a)
    # char = text.split()
    # print(char[188])
    print(text[13:18])
