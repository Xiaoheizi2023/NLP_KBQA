from py2neo import Graph
from zhipuai import ZhipuAI
# 此处api_key到智谱开放平台自行获取，新用户赠送现时一个月500万tokens，地址：https://open.bigmodel.cn/
client = ZhipuAI(api_key="")

def get_chatglm_response(prompt):
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": ""
                     "user", "content": prompt},
        ],
        stream=False,
    )
    return response.choices[0].message.content

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"), name='neo4j')
        self.num_limit = 20

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []

            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)

            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        #十面埋伏和功夫的评分（测试完成，单个和多个）
        #可以完成多个电影查询评分，取第一个评分，不知道为啥返回好多评分。。。
        if question_type == 'pingfen':
            l_ = []
            for i in answers:
                if i['m.title'] not in l_:
                    l_.append(i['m.title'])
                    final_answer = '{0}的评分是：{1}'.format(i['m.title'], i['m.rating'])
                    print(final_answer)
        # 十面埋伏和功夫的上映时间（测试完成，单个和多个）
        elif question_type == 'shangying':
            l_ = []
            for i in answers:
                if i['m.title'] not in l_:
                    l_.append(i['m.title'])
                    final_answer = '{0}的上映时间是：{1}'.format(i['m.title'], i['m.releasedate'])
                    print(final_answer)
        # 十面埋伏和功夫的风格（测试完成，单个和多个）
        elif question_type == 'fengge':
            dict_ = {}
            for i in answers:
                if i['m.title'] not in dict_:
                    dict_[i['m.title']] = i['b.name']
                else:
                    dict_[i['m.title']] += ("、" + i['b.name'])
            for i in dict_:
                print("{0}的类型是：{1}".format(i, dict_[i]))
        # 十面埋伏和功夫的简介（测试完成，单个和多个）
        elif question_type == 'jvqing':
            l_ = []
            for i in answers:
                if i['m.title'] not in l_:
                    l_.append(i['m.title'])
                    if i['m.introduction']:
                        final_answer = '{0}的剧情是：{1}'.format(i['m.title'], i['m.introduction'])
                        print(final_answer)
                    else:
                        prompt = f"请为电影{i['m.title']}写一段剧情简介。"
                        introduction = get_chatglm_response(prompt)
                        final_answer = '{0}的剧情是：{1}'.format(i['m.title'], introduction)
                        print("（本回复基于GLM大模型）: " + final_answer)
        # 十面埋伏和功夫的演员（测试完成，单个和多个）
        elif question_type == 'chuyan':
            dict_ = {}
            for i in answers:
                if i['m.title'] not in dict_:
                    dict_[i['m.title']] = i['n.name']
                else:
                    dict_[i['m.title']] += ("、" + i['n.name'])
            for i in dict_:
                print("{0}的演员名单是：{1}".format(i, dict_[i]))
        # 李连杰和成龙的简介（测试完成，单个和多个）
        elif question_type == 'yanyuanjianjie':
            l_ = []
            for i in answers:
                if i['n.name'] not in l_:
                    l_.append(i['n.name'])
                    if i['n.biography']:
                        final_answer = '{0}的介绍是：{1}'.format(i['n.name'], i['n.biography'])
                        print(final_answer)
                    else:
                        prompt = f"请为演员{i['n.name']}写一段简介，包括他的出生地、主要作品、成就等。"
                        introduction = get_chatglm_response(prompt)
                        final_answer = '{0}的介绍是：{1}'.format(i['n.name'], introduction)
                        print("（本回复基于GLM大模型）: " + final_answer)
        # 成龙和李连杰和周星驰合作的电影（多人测试完成）
        elif question_type == 'hezuochuyan':
            dict_ = {}
            l_ = []
            for i in answers:
                if i['m.title'] not in l_:
                    l_.append(i['m.title'])
                if i['n.name'] not in dict_:
                    dict_[i['n.name']] = []
                    dict_[i['n.name']].append(i['m.title'])
                else:
                    dict_[i['n.name']].append(i['m.title'])
            name = ''
            for i in dict_:
                name += (i + "、")
                l_ = list(set(l_).intersection(set(dict_[i])))
            s = ''
            for i in l_:
                s += (i + '、')

            if s == '':
                print("{0}没有共同出演的电影有：{1}".format(name[:-1]))
            else:
                print("{0}共同出演的电影有：{1}".format(name[:-1], s[:-1]))
        # 成龙和李连杰和周星驰总共的电影
        elif question_type == 'zonggong':
            dict_ = {}
            for i in answers:
                if i['n.name'] not in dict_:
                    dict_[i['n.name']] = []
                    dict_[i['n.name']].append(i['m.title'])
                else:
                    dict_[i['n.name']].append(i['m.title'])
            for i in dict_:
                print("{0}总共演过的电影有：{1}部".format(i, len(dict_[i])))
        # 周星驰和李连杰的生日？
        elif question_type == 'shengri':
            l_ = []
            for i in answers:
                if i['n.name'] not in l_:
                    l_.append(i['n.name'])
                    if i['n.birth']:
                        final_answer = '{0}的生日是：{1}'.format(i['n.name'], i['n.birth'])
                        print(final_answer)
                    else:
                        prompt = f"请为演员{i['n.name']}提供他的生日信息。"
                        birth = get_chatglm_response(prompt)
                        final_answer = '{0}的生日是：{1}'.format(i['n.name'], birth)
                        print("（本回复基于GLM大模型）: " + final_answer)

        return final_answer

if __name__ == '__main__':
    searcher = AnswerSearcher()
