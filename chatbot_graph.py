from question_classifier import *
from question_parser import *
from answer_search import *
import contextlib
import textwrap

'''问答类'''

class ChatBotGraph:
    def __init__(self):
        #实体识别和问题分类，该部分完成数据的提取和导入
        self.classifier = QuestionClassifier()
        #针对特定问题的查询
        self.parser = QuestionPaser()
        #回答语句的构建
        self.searcher = AnswerSearcher()
    # 使用Flask时使用这段代码会有问题，故先注释掉
    # def chat_main(self, sent):
    #     answer = '抱歉，或许是数据库还未收纳您想要查询的信息，请尝试重新输入'
    #
    #     #返回的是实体及其类别，以及问题类型
    #     res_classify = self.classifier.classify(sent)
    #     if  res_classify=='':
    #         print(answer)
    #
    #     #print('类别：',res_classify)
    #
    #     #返回的是问题类型和对应的查询结果
    #     res_sql = self.parser.parser_main(res_classify)
    #     #print('sql语句',res_sql)
    #
    #     final_answers = self.searcher.search_main(res_sql)
    #     if final_answers=='':
    #         print(answer)
    def chat_main(self, sent):
        answer = '抱歉，小冰的数据库暂时没有收录，请先提问其他内容吧~'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer

        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if final_answers:
            return '\\n'.join(final_answers)
        else:
            return answer

if __name__ == '__main__':
    handler = ChatBotGraph()
    # 测试
    problems = [
        "卧虎藏龙和花样年华的评分",
        "饮食男女的上映时间",
        "霸王别姬这部电影的风格"
    ]
    for id, problem in enumerate(problems):
        print("第{0}个问题是{1}：".format(id + 1, problem))
        print("小冰：", end="")
        handler.chat_main(problem)
        print("\n")
    print("本次测试已结束，可以愉快的开始提问了")
    # 测试-end

    while 1:
        question = input('请输入问题:')
        if question.lower() in ('跪安', '退下', '结束', '退出', 'end'):
            print('本次问答到此结束，期待下次为您服务~~~')
            break
        print("小冰：", end="")
        # 使用一个临时文件来捕获 chat_main 方法的输出
        with open('temp_output.txt', 'w') as temp_file:
            with contextlib.redirect_stdout(temp_file):
                handler.chat_main(question)
        # 检查临时文件的内容来判断是否有输出
        with open('temp_output.txt', 'r') as temp_file:
            output = temp_file.read().strip()
            if output:
                print(output)
            else:
                print("小冰不知道哦，小冰会努力学习哒~")





