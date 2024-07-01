# NLP练习
### 基于知识图谱的问答系统

# 相关流程：
### 1、建立图谱（结构化的，详见代码；非结构化的需要的NLP特别多）
### 2、构建类别判定（可以基于机器学习方法或者深度学习方法的文本分类或者是基于关键字的规则方法）（本文为规则方法）
### 3、提取问题中的实体
### 4、根据类别和实体构建查询语句并查询
### 5、根处理查询结果并输出
# 部分知识图谱展示
<div align=center><img  src="https://github.com/renhongjie/NLP_process/blob/main/images/电影问答系统1.png"/></div>
<p align="center">图1</p>


### 项目结构描述
```
├── README.md       // 描述文件
├── 建立词表.py     // 建立词表的程序文件
├── 建立图谱.py     // 建立知识图谱的程序文件
├── chatbot_graph.py     // 聊天系统主函数文件/运行文件
├── question_classifier.py        // 聊天系统问题分类函数 
├── question_parser.py        // 聊天系统问题转换函数 
├── answer_search.py        // 聊天系统问题回复函数
├── genre.txt        // 建立的词表 
├── movie.txt        // 建立的词表  
├── person.txt        // 建立的词表  
└── data   //数据文件
    └── genre.csv               // 图谱数据集之一
    └── movie_to_genre.csv               // 图谱数据集之一
    └── movie.csv               // 图谱数据集之一
    └── person_to_movie.csv               // 图谱数据集之一
    └── person.csv               // 图谱数据集之一
    └── userdict3.txt               // 图谱数据集之一
    └── vocabulary.txt              // 图谱数据集之一
    └── question              // 问题模版（项目中未用，但参考了）
        └── ...              // 16个问题模版

```


# 流程：
#### chatbot_graph(总控)->question_classifier（分类）->question_parser（构建查询语句）->answer_search（处理查询结果并输出）

## 基本规则写的，后期优化：加一些深度学习方法和多轮问答功能，存在一点小问题，每次都回答不知道，后期再改改

## 改进
 添加多轮对话
 
 用神经网络替换规则
