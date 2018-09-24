from DIRDistanceMatchingAutomata import DIRDistanceMatchingAutomata
import glob
class search_engine_foreachChar:
    def __init__(self, pattern, error_num = 1):
        self.pattern = pattern.lower().split() #từng từ trong mẫu
        self.Automata = [DIRDistanceMatchingAutomata(item, error_num) for item in self.pattern]


    def Search(self, string : str): #trả về độ mờ xuất hiện mẫu và vị trí xuất hiện của mẫu trong xâu
        dest = string.lower().split()
        result = []
        for item in self.Automata:
            result.append([item.LastState(item_) for item_ in dest])
        # result mảng chứa các trạng thái kết thúc của each automata
        # print(result)
        # result chứa các trạng thái kết thúc
        result_ = []
        # result_ chứa các list check hay không
        for item in self.Automata:
            result_.append([])
        for k in range(len(result)):
            for i in range(len(result[k])):
                for j in range(len(result[k][i])):
                    if (self.Automata[k].F.__contains__(result[k][i][j])):
                        result_[k].append(True)
                        break
                    if (j == len(result[k][i]) - 1):
                        result_[k].append(False)
        # print(result_)
        result_ = list(map(list, zip(*result_)))
        result__ = []
        for item in result_:
            result__.append(any(item))
        index_ = []
        for index, Bool in enumerate(result__):
            if(Bool):
                index_.append(index)
        position_ = []
        for index in index_:
            position = 0
            for i, word in enumerate(dest):
                position += (1 + len(word))
                if i >= index:
                    start = position - len(word) - 1
                    position_.append((start, position))
                    break
        result_ = list(map(list, zip(*result_)))

        s = []
        for item in self.Automata:
                s.append(item.F)

        # print(s)

        s__ = 0 #tổng độ mờ của tất cả các từ
        for i in range(len(result_)):
            s_ = 0 #s_ là tổng độ mờ của từ thứ i
            for j in range(len(result_[i])):
                if(result_[i][j] == True): #từ thứ j trên xâu trùng với từ thứ i trong mẫu
                    #tìm chung của result[i][j] và s[i] -> lấy index của chung trong s[i] đc k[j]
                    a = list(set(result[i][j]).intersection(s[i]))[0]
                    k = s[i].index(a) #k là độ mờ
                    s_ += (len(self.pattern[i]) - k) / (len(self.pattern[i]))
            # print(s_)
            s__ += s_

            #

        sum = s__ / len(string)
        # print(result_)
        #result[i] <=> result_[i] <=> automata[i]
        # print(result)
        return  sum , position_
        #position_ chứa các vị trí của xâu khớp với mẫu
        # for item in index_:
        #     print(dest[item])


if __name__ == '__main__':
    # import time
    # start_time = time.time()
    search_engine = search_engine_foreachChar(u'thuế xuaất nhậpp kẩu')
    # #
    # # with open("D:\CMC_TextMining\SearchingAlgorithm/test.txt", encoding='utf-8-sig') as f:
    # #     string = f.read()
    # # f.close()
    string = 'Phí thẩm định cấp giấy chứng nhận đối với thực phẩm xuất khẩu theo yêu cầu của nước nhập khẩu'

    search_engine.Search(string)
    pos = search_engine.Search(string)
    print(pos)
    # text_ = []
    # paths = glob.glob("D:\CMC_TextMining\SearchingAlgorithm/testSearch/*.txt")
    # for path in paths:
    #     with open(path, encoding='utf-8-sig') as file:
    #         text = file.read()
    #         text_.append(text)
    # #
    # a = [search_engine.Search(item) for item in text_]
    # print(a)
    #
    # print(time.time() - start_time)
    # import codecs
    # a = u"ỏ"
    # with open("D:\CMC_TextMining\SearchingAlgorithm/testSearch/test1.txt", encoding='UTF-8-sig') as file:
    #     text = file.read()
    # file.close()

    # print(search_engine.Search(text))
    #     text = te
    # print(len(u"ỏ"))

    # print('ỏ'.encode('utf-8'))
    # print('ỏ'.encode())

    # des = string.split()