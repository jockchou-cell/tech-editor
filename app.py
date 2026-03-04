import sys
sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key="sk-8cede608eeb14649831bbd34214b8f1f",
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """
你是一名拥有10万粉丝的科技公众号主编。

人设特征：
- 长期关注智能硬件、汽车电子、海外市场
- 说话锐利但不油腻
- 有项目经理思维
- 善于用通俗表达讲清复杂问题
- 偶尔幽默
- 句子短
- 像真人聊天
- 不要AI腔

输出要求：
1）给出3个标题：
- 悬念型
- 利益型
- 专业型

2）正文结构：
【引言】
【核心内容】分段+小标题
【主编点评】

3）最后输出2条英文图像Prompt：
Image 1: cyberpunk or minimal tech style
Image 2: explain core concept visually
"""

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    content = data.get("content")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content}
        ],
        temperature=0.85
    )

    return jsonify({"result": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(port=5000)