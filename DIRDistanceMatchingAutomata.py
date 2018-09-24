import FiniteAutomata as FA
# from AutomataAndFormalLang import Convert_NFA_to_DFA, MinimizedDFA
def DIRDistanceMatchingAutomata(input, error_num = 1):
        if(error_num > len(input)):
            raise Exception('The number of errors must be less than or equal to the length of the pattern')
        else:
            n = len(input)
            NumOfStates = 0
            for i in range(error_num + 1):
                NumOfStates += n + 1 - i

            Q = list(range(NumOfStates))
            F = []
            F.append(n)
            for i in range(error_num):
                F.append(F[-1] + n - i)
            with open('D:/CMC_TextMining/SearchingAlgorithm/alphabet.txt', encoding='utf-8-sig') as f:
               A = f.read().splitlines()
            # A = alphabet
            f.close()
            # A.append('#')
            D = FA.NFADelta(NumberOfStates=NumOfStates, NumberOfSymbols=len(A), Rows=[], Epsilon=[])
            # print(D.Rows)
            # print(D.Epsilon)
            input = input.lower()
            input = [item for item in input]
            for k in range(0, error_num + 1):
                if(k == 0):
                    curr = 0
                    for j in range(k, n):
                        for i in range(len(A)):
                            if(input[j] == A[i]):
                                D.Rows[curr][i].append(curr + 1)
                                if(curr != 0):
                                    D.Rows[curr][i].append(curr + n - k)
                            else:
                                D.Rows[curr][i].append(curr + n - k + 1)
                                if(curr != 0):
                                     D.Rows[curr][i].append(curr + n - k)
                        D.Epsilon[curr].append(curr + n-k + 1)
                        curr += 1

                    # D.Rows[0][]
                else:
                    curr = k*n + sum(range(1, 1-k, -1))
                    for j in range(k, n):
                        for i in range(len(A)):
                            if(input[j] == A[i]):
                                D.Rows[curr][i].append(curr + 1)
                            elif(curr + n - k + 1 <= Q[-1]):
                                D.Rows[curr][i].append(curr + n - k + 1)
                                if(j != k):
                                    D.Rows[curr][i].append(curr + n - k)
                        if(curr + n - k + 1 <= Q[-1]):
                            D.Epsilon[curr].append(curr + n - k + 1)
                        curr += 1

            for i in range(len(A)):
                D.Rows[0][i].append(0)
            Automata = FA.NFA(Q = Q , F = F, q0 = 0, D = D, A = A)
            return Automata



if __name__ == '__main__':
    x = 'thuế xuaất nhậpp kẩu'
    pattern = x.split()

    automata = [DIRDistanceMatchingAutomata(item) for item in pattern]
    # automata_ = DIRDistanceMatchingAutomata('xuaất')

    y = 'Phí thẩm định cấp giấy chứng nhận đối với thực phẩm xuất khẩu theo yêu cầu của nước nhập khẩu'
    y = y.lower()
    dest = y.split()


    # result = [automata_.LastState(item)for item in dest]
    result = []
    for item in automata:
        result.append([item.LastState(item_) for item_ in dest])
    #result mảng chứa các trạng thái kết thúc của each kết thúc
    print(result)
    #result chứa các trạng thái kết thúc
    result_ = []
    #result chứa các list check hay không
    for item in automata:
        result_.append([])

    for k in range(len(result)):
        for i in range(len(result[k])):
            for j in range(len(result[k][i])):
                if(automata[k].F.__contains__(result[k][i][j])):
                    result_[k].append(True)
                    break
                if(j == len(result[k][i]) - 1):
                    result_[k].append(False)

    print(result_)
    # print(len(result))




    # result là mảng chứa check
    result_ = list(map(list, zip(*result_)))


    a = []
    for item in result_:
        a.append(any(item))

    # print(result)
    # print(automata[1].LastState('xuaất'))

    # a chứa vị trí xuất hiện của mẫu
    print(a)