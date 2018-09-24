def prefix(u : str):
    a = []
    for i in range (len(u) + 1):
        a.append(u[:i])

    return a

def suffix(u : str):
    a = []
    for i in range(len(u) + 1):
        a.append(u[i:])

    return a

def fact(u : str):
    a = []
    for item in suffix(u):
        for item_ in prefix(item):
            if(not a.__contains__(item_)):
                a.append(item_)
    return sorted(a, key=len)


#khúc cuối độ dài f của khúc đầu độ dài d
def SuffixOfPrefix(u : str, f, d):
    return(u[:d][-f:])

def lid(y : str, u : str):
    a = len(y)
    index = u.find(y)
    return a, index + a


def lid_2(y : str, u : str): #thêm tần suất xuất hiện
    if(len(y) == 0):
        # return [0, 0, 0, 0]
        return [0, 0, 0]
    else:
        a = len(y)
        index = u.find(y)
        count = u.count(y)
        # return [a, index + a, count, 0]
        return [a, index + a, count]



def lfact(v : str, u : str):
    a = list(set(suffix(v)).intersection(fact(u)))
    a_ = sorted(a,key=len)
    return a_[-1]

def CapSoCoNghia(u : str):
    a = []
    for item in fact(u):
        a.append(lid(item, u))
    return a

def CapSoCoNghia_2(u : str):
    a = []
    for item in fact(u):
        a.append(lid_2(item, u))
    return a


def GetAlphabet(u : str):
    a = []
    for item in u:
        if(not a.__contains__(item)):
            a.append(item)

    return a

def EncodePattern(pattern : str):
    with open('Character.txt', 'r') as f:
        Character = f.read().splitlines()
    f.close()
    P = list(set(pattern.split()))
    EncodedPattern = []
    for item in pattern.split():
        for i in range(len(P)):
            if (item == P[i]):
                EncodedPattern.append(Character[i])
    EncodedPattern = ''.join(EncodedPattern)
    return  EncodedPattern

def Encoding(S, P, Character):
        EncodedString = []
        for item in S.lower().split():
            for i in range(len(P)):
                if(item == P[i]):
                    EncodedString.append(Character[i])
                    break
                if(i == len(P) - 1):
                    EncodedString.append('#')

        EncodedString = ''.join(EncodedString)
        return EncodedString

def GetPosition(string, index):
    position_ = []
    for index_ in index:
        position = 0
        for i, word in enumerate(string.split()):
            position += (1 + len(word))
            if i >= index_:
                start = position - len(word) - 1
                position_.append((start, position))
                break

    return  position_


if __name__ == '__main__':
    # a = suffix('abc')
    # u = 'drabcgaba'
    # v = 'ghbacabc'
    # print(lid('ab', u))
    # print(lfact(v, u))

    P = 'aababc'
    print(CapSoCoNghia(P))