#实体识别和问题分类
import os
import ahocorasick     #AC自动机模块
# 如果安装报错请使用 pip3 install pyahocorasick -i https://pypi.tuna.tsinghua.edu.cn/simple/
class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #join().split取当前文件路径，并以最后一个/分段，取后面部分，再加上前面join的'/'，就是当前文件夹的相对路径

        #　以下是特征词的路径：
        self.person_path = os.path.join(cur_dir, 'person.txt')
        self.movie_path = os.path.join(cur_dir, 'movie.txt')
        self.genre_path = os.path.join(cur_dir, 'genre.txt')

        # 加载特征词
        self.person_wds= [i.strip() for i in open(self.person_path,encoding="utf-8") if i.strip()]#encoding="utf-8"
        self.movie_wds= [i.strip() for i in open(self.movie_path,encoding="utf-8") if i.strip()]
        self.genre_wds= [i.strip() for i in open(self.genre_path,encoding="utf-8") if i.strip()]


        #构造字典树从而后面进行实体识别
        #对应的字典树的内容：
        self.region_words = set(
            self.person_wds + self.movie_wds + self.genre_wds)

        # 构造字典树，build_actree是字典树构建的通用函数，构造内容一般不变
        self.region_tree = self.build_actree(list(self.region_words))


        # 构建词典，确定实体的类别
        self.wdtype_dict = self.build_wdtype_dict()
        # 人为确定的问句疑问词
        #剧情和演员简介容易冲突
        # 评分
        self.q1_qwds = ['分数', '评分', '现象', '表现']#评分
        #上映
        self.q2_qwds = ['上映','首映', '上映时间', '首映时间', '首播', '观看', '上线', '影院', '放映', '时间']
        #风格
        self.q3_qwds = ['风格', '格调', '类型']
        #剧情
        self.q4_qwds = ['剧情', '内容', '故事', '简介', '情节', '梗概']
        #出演
        self.q5_qwds = ['演员', '演的', '出演', '演过', '哪些人']
        #演员简介
        self.q6_qwds = ['是谁', '介绍', '简介', '谁是', '详细信息','信息' ]
        #AB合作
        self.q7_qwds = ['合作', '一起']
        #A一共演过多时
        self.q8_qwds = ['一共', '总共', '多少部', '多少', '参演']
        #A的生日
        self.q9_qwds = ['出生日期', '生日', '出生', '生于']


        print('模型初始化完成......')

        return

    '''分类主函数'''
    def classify(self, question):
        # data存储数据，包含两部分，一个是识别出的实体及其类别，一个是问题的类别
        data = {}

        #进行实体识别，返回问题中的实体和对应的类别，识别失败时直接返回
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict

        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_

        #问题分类
        question_type = 'others'
        question_types = []

        #人为制订的问题模板，要求存在实体，并且问题收纳在模板中，才会对问题进行分类
        # 评分
        if self.check_words(self.q1_qwds, question) and ('movie' in types):
            question_type = 'pingfen'
            question_types.append(question_type)#考虑到提问时可能有多个问题
        #上映
        if self.check_words(self.q2_qwds, question) and ('movie' in types):
            question_type = 'shangying'
            question_types.append(question_type)
        # 风格
        if self.check_words(self.q3_qwds, question) and ('movie' in types):
            question_type = 'fengge'
            question_types.append(question_type)
        # 剧情
        if self.check_words(self.q4_qwds, question) and ('movie' in types):
            question_type = 'jvqing'
            question_types.append(question_type)
        # 出演
        if self.check_words(self.q5_qwds, question) and ('movie' in types):
            question_type = 'chuyan'
            question_types.append(question_type)


        # 演员简介
        if self.check_words(self.q6_qwds, question) and ('person' in types):
            question_type = 'yanyuanjianjie'
            question_types.append(question_type)
        # 合作出演
        if self.check_words(self.q7_qwds, question) and ('person' in types):
            question_type = 'hezuochuyan'
            question_types.append(question_type)
        # 总共
        if self.check_words(self.q8_qwds, question) and ('person' in types):
            question_type = 'zonggong'
            question_types.append(question_type)
        # 生日
        if self.check_words(self.q9_qwds, question) and ('person' in types):
            question_type = 'shengri'
            question_types.append(question_type)

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        #data包含两部分，一个是识别出的实体及其类别，一个是问题的类别
        return data


    '''构造实体对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.person_wds:
                wd_dict[wd].append('person')
            if wd in self.movie_wds:
                wd_dict[wd].append('movie')
            if wd in self.genre_wds:
                wd_dict[wd].append('gener')

        return wd_dict

    '''构建字典树，利用AC自动机实现实体识别'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''利用AC自动机实现问题中的实体识别'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词对问题进行分类，也就是确认问题的有效性'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)