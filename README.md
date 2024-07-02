# 自然语言处理NLP
### 基于电影知识图谱和大型语言模型（LLM）的KBQA问答机器人

# 项目流程：
### 1. 知识图谱构建：利用深度学习技术，从大量非结构化数据中自动提取实体和关系，构建一个高度结构化的知识图谱。图谱中包含电影、人物、电影类型等实体及其属性，以及它们之间的复杂关系。
### 2. 文本分类：采用基于深度学习的序列到序列模型，对用户提出的问题进行分类，确定问题的意图和查询对象；使用AC自动机进行实体识别，并根据疑问词和实体类别将问题分类。
### 3. 实体识别与关系抽取：利用迁移学习技术，对问题中的实体进行识别，并抽取实体之间的关联关系。同时，结合预训练语言模型，进一步提高实体识别和关系抽取的准确性。
### 4. 查询构建与优化：基于实体识别和关系抽取的结果，构建复杂的查询语句，并采用图查询优化技术，提高查询效率；根据问题类型和实体，生成Cypher查询语句，用于从Neo4j数据库中检索信息。
### 5. 知识推理与问答生成：在知识图谱的基础上，采用基于规则的推理和基于图神经网络的推理技术，生成准确的答案。同时，结合预训练语言模型，对答案进行自然语言生成，提高问答系统的交互性；使用Flask框架创建Web应用程序，处理用户的问题，并返回特定问题的LLM大语言模型的回复。
### 6. 用户界面设计：采用交互设计理念，设计一个简洁、直观的聊天界面，使用户能够轻松地与系统进行交互。

# 项目成果展示
<div align=center><img  src="https://github.com/Xiaoheizi2023/NLP_KBQA/blob/master/images/成果展示图1.png"/></div>
<p align="center">图1</p>

<div align=center><img  src="https://github.com/Xiaoheizi2023/NLP_KBQA/blob/master/images/成果展示图2.png"/></div>
<p align="center">图2</p>

<div align=center><img  src="https://github.com/Xiaoheizi2023/NLP_KBQA/blob/master/images/成果展示图3.png"/></div>
<p align="center">图3</p>

<div align=center><img  src="https://github.com/Xiaoheizi2023/NLP_KBQA/blob/master/images/成果展示图4.png"/></div>
<p align="center">图4</p>

<div align=center><img  src="https://github.com/Xiaoheizi2023/NLP_KBQA/blob/master/images/成果展示图5.png"/></div>
<p align="center">图5</p>

# KBQA问答机器人架构图
<div align=center><img  src="https://github.com/Xiaoheizi2023/NLP_KBQA/blob/master/images/KBQA问答机器人架构图.png"/></div>
<p align="center">图6</p>

# KBQA问答机器人的项目结构图
<div align=center><img  src="https://github.com/Xiaoheizi2023/NLP_KBQA/blob/master/images/KBQA问答机器人的项目结构图.png"/></div>
<p align="center">图7</p>

# 部分知识图谱展示
<div align=center><img  src="https://github.com/Xiaoheizi2023/NLP_KBQA/blob/master/images/部分知识图谱展示图.png"/></div>
<p align="center">图8</p>

# 项目结构描述
```
KBQA
├─ answer_search.py              # 包含搜索答案的函数和类
├─ app.py                        # 应用程序入口点，启动服务或运行程序的主要文件
├─ chatbot_graph.py              # 处理聊天机器人与知识图谱交互的逻辑
├─ genre.txt                     # 包含电影类型数据的文本文件
├─ movie.txt                     # 包含电影数据的文本文件
├─ person.txt                    # 包含人物数据的文本文件
├─ question_classifier.py        # 用于分类问题的代码
├─ question_parser.py            # 用于解析问题的代码
├─ README.md                     # 项目的说明文件
├─ requirements.txt              # 列出了项目所需的Python库和版本，本项目python版本3.8
├─ temp_output.txt               # 临时输出文件
├─ __init__.py                   # 初始化脚本，凑数的
├─ 建立关键词词表（字典）.py       # 用于建立关键词词表或字典的脚本
├─ 建立图谱.py                    # 用于建立知识图谱的脚本
├─ __pycache__                   # Python字节码缓存文件夹，通常在开发过程中不需要提交到版本控制
├─ templates
│  └─ index.html                 # Web应用程序的HTML模板文件
├─ static
│  └─ ico
│     └─ image.ico               # 网站图标文件
├─ data
│  ├─ genre.csv                  # 包含电影类型数据的CSV文件
│  ├─ movie.csv                  # 包含电影数据的CSV文件
│  ├─ person.csv                 # 包含人物数据的CSV文件
│  ├─ question
│  │  ├─ question_classification.txt
│  │  ├─ vocabulary.txt
│  │  ├─ 【0】评分.txt
│  │  ├─ 【10】某演员出演过哪些类型的电影.txt
│  │  ├─ 【11】演员A和演员B合作了哪些电影.txt
│  │  ├─ 【12】某演员一共演过多少电影.txt
│  │  ├─ 【13】演员出生日期.txt
│  │  ├─ 【1】上映.txt
│  │  ├─ 【2】风格.txt
│  │  ├─ 【3】剧情.txt
│  │  ├─ 【4】某电影有哪些演员出演.txt
│  │  ├─ 【5】演员简介.txt
│  │  ├─ 【6】某演员出演过的类型电影有哪些.txt
│  │  ├─ 【7】某演员演了什么电影.txt
│  │  ├─ 【8】演员参演的电影评分【大于】.txt
│  │  └─ 【9】演员参演的电影评分【小于】.txt
│  ├─ userdict3.txt
│  └─ vocabulary.txt             # 用于自然语言处理的词汇表
├─ .idea                         # IDE（如PyCharm）的配置文件夹，通常不需要提交到版本控制
├─ .git                          # 版本控制文件夹，包含项目的版本控制信息
├─ .gitignore                    # Git忽略文件，用于指定不被Git跟踪的文件和文件夹
└─ logs                          # Git日志文件夹，包含版本控制日志信息
```

# 流程：
## chatbot_graph(总控)->question_classifier（分类）->question_parser（构建查询语句）->answer_search（处理查询结果并输出）

# 项目改进：
### 添加了多轮对话功能，响应速度更快
### 在缺失部分的非结构化数据加入了LLM大模型回复，回复效果更好
### 解决了"args"键报错问题（查询不存在的人或者电影会报错该问题)
### 使用了Flask库作为后端，同时写了一个简单的前端Html用于实时交互

# 项目展望：
### 有很多逻辑上的问题没有时间进行修改，比如可以进一步完善对话回复逻辑，查询不到的问题返回给LLM进行查询
### 本文采用了基于规则的方法：通过关键字匹配或正则表达式来识别问题的类别；未来可尝试以下方法：
### 机器学习方法：使用文本分类算法，如朴素贝叶斯、支持向量机（SVM）、决策树等，对问题进行分类；
### 深度学习方法：使用卷积神经网络（CNN）、循环神经网络（RNN）或Transformer等模型进行文本分类。
