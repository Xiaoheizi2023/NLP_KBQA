from flask import Flask, render_template, request, jsonify
import os
import sys
from flask_cors import CORS

# 添加当前目录到 sys.path，以便导入 chatbot_graph
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot_graph import ChatBotGraph

app = Flask(__name__)
CORS(app)

# 初始化模型
handler = ChatBotGraph()
print("模型初始化完成……")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    question = request.form['question']
    if question.lower() in ('跪安', '退下', '结束', '退出', 'end'):
        return jsonify({'answer': '本次问答到此结束，期待下次为您服务~~~'})

    answer = handler.chat_main(question)
    if answer:
        return jsonify({'answer': answer})
    else:
        return jsonify({'answer': "小冰不知道哦，小冰会努力学习哒~"})


if __name__ == '__main__':
    app.run(debug=True)
