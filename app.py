from flask import Flask, render_template, request, jsonify
import os
import sys
import contextlib
import io
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加当前目录到 sys.path，以便导入 chatbot_graph
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot_graph import ChatBotGraph

app = Flask(__name__)

# 初始化模型
handler = ChatBotGraph()

@app.route('/')
def index():
    logger.info("访问主页")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    question = request.form['question']
    logger.info(f"收到问题: {question}")

    if question.lower() in ('跪安', '退下', '结束', '退出', 'end'):
        logger.info("结束对话")
        return jsonify({'answer': '本次问答到此结束，期待下次为您服务~~~'})

    try:
        # 使用StringIO对象来捕获chat_main方法的输出
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            handler.chat_main(question)

        answer = output.getvalue().strip()
        logger.info(f"生成的答案: {answer}")

        if answer:
            return jsonify({'answer': answer})
        else:
            logger.warning("未生成答案")
            return jsonify({'answer': "小冰不知道哦，小冰会努力学习哒~"})
    except Exception as e:
        logger.error(f"处理问题时发生错误: {str(e)}", exc_info=True)
        return jsonify({'answer': "抱歉，处理您的问题时出现了错误。请稍后再试。"})

@app.route('/test', methods=['GET'])
def test():
    logger.info("开始测试")
    problems = [
        "卧虎藏龙和花样年华的评分",
        "饮食男女的上映时间",
        "霸王别姬这部电影的风格"
    ]
    results = []
    for id, problem in enumerate(problems):
        logger.info(f"测试问题 {id+1}: {problem}")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            handler.chat_main(problem)
        answer = output.getvalue().strip()
        logger.info(f"测试问题 {id+1} 的答案: {answer}")
        results.append({
            'question': f"第{id + 1}个问题是{problem}：",
            'answer': answer if answer else "小冰不知道哦，小冰会努力学习哒~"
        })
    logger.info("测试完成")
    return jsonify(results)

if __name__ == '__main__':
    logger.info("启动应用")
    app.run(debug=True)