from KB.KB_query import jena_sparql_endpoint, question2sparql
import os

file_path = os.path.split(os.path.realpath(__file__))[0]


class QAInterface:
    def __init__(self):
        # TODO 连接Fuseki服务器。
        self.fuseki = jena_sparql_endpoint.JenaFuseki()
        # TODO 初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
        self.q2s = question2sparql.Question2Sparql([os.path.join(file_path, 'external_dict', 'movie_title.txt'),
                                                    os.path.join(file_path, 'external_dict', 'person_name.txt')])

    def answer(self, question: str):
        my_query = self.q2s.get_sparql(question)
        if my_query is not None:
            result = self.fuseki.get_sparql_result(my_query)
            value = self.fuseki.get_sparql_result_value(result)

            # TODO 判断结果是否是布尔值，是布尔值则提问类型是"ASK"，回答“是”或者“不知道”。
            if isinstance(value, bool):
                if value is True:
                    ans = "是的"
                else:
                    ans = "我还不知道这个问题的答案"
            else:
                # TODO 查询结果为空，根据OWA，回答“不知道”
                if len(value) == 0:
                    ans = "我还不知道这个问题的答案"
                elif len(value) == 1:
                    ans = value[0]
                else:
                    output = ''
                    for v in value:
                        output += v + u'、'
                    ans = output[0:-1]

        else:
            # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
            ans = "我不知道你表达的意思"

        return ans


if __name__ == '__main__':
    print("1. 某演员演了什么电影2. 某电影有哪些演员出演3. 演员A和演员B合作出演了哪些电影4. 某演员参演的评分大于X的电影有哪些5. 某演员出演过哪些类型的电影\n6. 某演员出演的XX类型电影有哪些。7. 某演员出演了多少部电影。8. 某演员是喜剧演员吗。9. 某演员的生日/出生地/英文名/简介10. 某电影的简介/上映日期/评分")
    qa_interface = QAInterface()
    while True:
        question = input(">> 请输入问题：")
        ans = qa_interface.answer(question)
        print(ans)
        print('#' * 100)
